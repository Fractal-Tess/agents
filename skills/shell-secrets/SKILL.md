---
name: shell-secrets
description: Which API keys and secrets are loaded into the user's shell on every host, under which environment variable names, and how to add a new one. Use before asking the user for an API key or token, when a tool or script needs a credential (OpenRouter, Dokploy, fal.ai, MiniMax, Z.ai, Moonshot, OpenCode, React Bits), when an expected variable is empty, or when adding a secret to the NixOS config.
---

# Shell secrets

> **Keep this skill current.** Whenever a secret is added, removed, renamed,
> or its variable changes in `~/nixos` (`secrets/*.json` or
> `modules/nixos/services/sops/`), update the table below in the same change.

All secrets are SOPS-encrypted in `~/nixos/secrets/*.json` and rendered by
the modules in `~/nixos/modules/nixos/services/sops/`. Every module is on by
default, so **all hosts (vd, kiwi, neo) get the same set**. API keys meant for
the shell are rendered to `~/.secrets.d/<name>.fish` (mode 0600), and fish
sources every file there at startup.

## What is exported

| Variable | Source secret | Module | Also available as a file |
| --- | --- | --- | --- |
| `OPENROUTER_API_KEY` | `secrets/openrouter.json` | `default.nix` | `~/.config/secrets/openrouter_api_key` |
| `MOONSHOT_API_KEY` | `secrets/moonshot.json` | `default.nix` | `~/.config/secrets/moonshot_ai` |
| `DOKPLOY_API_KEY`, `DOKPLOY_URL` | `secrets/dokploy-fractal-tess.json` (`API_KEY`) | `dokploy.nix` | – |
| `FAL_AI`, `FAL_KEY` | `secrets/fal-ai.json` | `fal-ai.nix` | – |
| `MINIMAX_API_KEY` | `secrets/minimax.json` | `minimax.nix` | `~/.config/secrets/minimax/apikey` |
| `ZAI_API_KEY` | `secrets/z-ai.json` | `z-ai.nix` | `~/.config/secrets/z-ai/apikey` |
| `OPENCODE_VGFRACTAL`, `OPENCODE_VILIAN_GERDJIKOV` | `secrets/opencode.json` | `opencode.nix` | – |
| `REACTBITS_LICENSE_KEY` | `secrets/reactbits.json` | `reactbits.nix` | – |

Not exported, on purpose: Gitadel (`gtd` reads `/run/secrets/gitadel_api_token`
itself), Syncthing and SSH material (files), and service-only secrets
(clip-sync, shadoword, cliproxyapi; Supermemory's LLM router reads the
CLIProxyAPI client key as a systemd credential). `secrets/hermes-agent.json`
and `secrets/supermemory.json` (the old OpenRouter key) are not wired up
anywhere. `secrets/bitwarden.json` (`bitwarden_master_password`)
is a file only (`/run/secrets/bitwarden_master_password`), read by `bw-agent`
to unlock the vault; never read it directly. Account logins (website
usernames, passwords, 2FA codes) are not shell secrets: they come from
Bitwarden through `bw-agent`, see the `bitwarden` skill.

This table can drift. The live truth, names only:

```sh
grep -ho 'set -gx [A-Z_]*' ~/.secrets.d/*.fish | cut -d' ' -f3 | sort
```

## Using a key from an agent shell

Agent shells are often zsh/bash and do not source fish files. Check the
variable, then fall back to the rendered file. Never print the value.

```sh
[ -n "$OPENROUTER_API_KEY" ] || OPENROUTER_API_KEY=$(sed -n 's/^set -gx OPENROUTER_API_KEY "\(.*\)"$/\1/p' ~/.secrets.d/*.fish)
```

If a variable is missing on a host, the host has not been rebuilt since the
module changed. Rebuild with the update script (`nixos` skill), then open a
new shell.

## Adding a key

1. Encrypt it: `cd ~/nixos && sops secrets/<name>.json` (age key
   `~/.config/sops/age/keys.txt`, recipients in `.sops.yaml`).
2. Copy `modules/nixos/services/sops/dokploy.nix`: a
   `sops.secrets.<name>` (`key = "<json field>"` when the field name
   differs) and a `sops.templates."<name>.fish"` with
   `path = "/home/${username}/.secrets.d/<name>.fish"` and
   `set -gx VAR "${config.sops.placeholder.<name>}"`. Make `enable` default to
   `true` (`mkEnableOption "…" // { default = true; }`). Do not add per-host
   toggles: hosts only set `modules.services.sops.enable = true`.
3. Import it in `modules/nixos/services/sops/default.nix`.
4. Add a row to the table above (and remove or edit rows when a secret is
   removed or renamed).
5. Rebuild all hosts with the update script.
