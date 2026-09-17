---
name: gitadel
description: >-
  Use when working with Gitadel, the user's self-hosted Git forge: managing
  repositories, collaborators, organizations, SSH keys, instance settings,
  storage, backups, or its NixOS deployment. Covers the gtd CLI, portable login,
  runtime SOPS credentials, and the instance on neo.netbird.cloud.
---

# Gitadel

Use `gtd` to manage the running instance. The executable was renamed in v0.7.0;
there is no `gitadel-cli` executable alias. The Cargo package, Nix package/app,
and NixOS module/options still use `gitadel-cli`.

Use ordinary Git for clone, fetch, and push. GitHub tools do not manage Gitadel
repositories.

## Instance and credentials

The production instance runs on Neo:

- HTTP origin: `http://neo.netbird.cloud:3030`
- Git SSH endpoint: `ssh://git@neo.netbird.cloud:2222/<namespace>/<repository>.git`
- Health endpoint: `http://neo.netbird.cloud:3030/healthz`
- vd, Kiwi, and Neo have the CLI and shared SOPS credentials configured.

The NixOS client module wraps `gtd` with default environment values. It does
not set session-wide variables or read the secret during a Nix build:

```nix
programs.gitadel-cli = {
  enable = true;
  serverUrl = "http://neo.netbird.cloud:3030";
  tokenFile = config.sops.secrets.gitadel_api_token.path;
};
```

On these hosts the runtime token file is `/run/secrets/gitadel_api_token`,
owned by `fractal-tess`, group `users`, mode `0600`. No login is needed:

```sh
gtd --version
gtd auth status
gtd me profile
```

To test the installed wrapper without inherited overrides:

```sh
env -u GITADEL_SERVER -u GITADEL_TOKEN -u GITADEL_TOKEN_FILE \
  /run/current-system/sw/bin/gtd auth status
```

Do not ask the user to paste the token into chat. Never print the secret file,
put its contents in command arguments, embed credentials in URLs, or write
plaintext credentials into Nix configuration, the Nix store, logs, or
documentation.

## Endpoint and credential selection

Server precedence is `--server`, then `GITADEL_SERVER`, then the saved server,
then `http://127.0.0.1:3000`. The Nix wrapper supplies `GITADEL_SERVER` only as
a default; inherited environment values override it. A valid `--server` also
overrides a malformed environment value. Servers must be HTTP(S) origins,
without credentials or URL paths.

```sh
GITADEL_SERVER=http://neo.netbird.cloud:3030 gtd auth status
gtd --server http://neo.netbird.cloud:3030 auth status
gtd --server http://neo.netbird.cloud:3030 \
  --token-file /run/secrets/gitadel_api_token auth status
```

Token precedence is an explicit token flag, then `GITADEL_TOKEN`, then
`GITADEL_TOKEN_FILE`, then the saved login. Explicit token sources are mutually
exclusive. A stale `GITADEL_TOKEN` can override the SOPS file; check whether it
is set without displaying its value. Prefer a file or stdin to `--token`,
which exposes the value in process arguments.

Saved credentials are used only for their matching origin. Environment
credentials paired with `GITADEL_SERVER` are withheld when `--server` selects
another origin, or when that environment origin is invalid. An explicit token
flag deliberately selects credentials for the chosen server.

## Portable login

On a machine without the NixOS wrapper, install the client and log in:

```sh
nix profile install github:Fractal-Tess/gitadel#gitadel-cli
gtd --server http://neo.netbird.cloud:3030 auth login
gtd auth status
```

Nix is optional; a standalone `gtd` binary uses the same login flow. Bare
`gtd auth login` prompts for the server and token. Token entry is hidden, and
login verifies the token before replacing the saved login. Noninteractive
login needs a token source; it does not prompt.

The client remembers one login in the platform's per-user configuration
directory. On Linux and WSL this is `$XDG_CONFIG_HOME/gitadel/auth.json`,
normally `~/.config/gitadel/auth.json`. Tokens are stored unencrypted. Unix
permissions are `0700` for the directory and `0600` for the file. Do not commit
or sync this file into the skills or dotfiles repository.

To save a reference to a managed token file instead of copying the token:

```sh
gtd --server http://neo.netbird.cloud:3030 \
  --token-file /run/secrets/gitadel_api_token auth login
```

This stores the absolute file path, preserves rotating SOPS symlinks, and
rereads the file on each invocation. Explicit `--token-stdin` or
`--token-file -` reads stdin; login with either stores the token itself.
`GITADEL_TOKEN_FILE` always names a file, not stdin.

`gtd auth logout` removes only the saved login. It does not revoke the server
token, delete an external token file, or disable environment/Nix credentials.
Use Account settings → Access to revoke a token.

HTTP here is confined to the encrypted NetBird mesh. Use HTTPS for deployments
outside an encrypted private network. Do not weaken SSH host-key verification.

## Repository work

Inspect before changing:

```sh
gtd repo list
gtd repo view fractal-tess/gitadel
gtd repo create --help
```

For a requested new repository, substitute the actual namespace and name:

```sh
gtd repo create <namespace>/<repository> --private \
  --description 'Repository description'
```

Creation defaults to public, so use `--private` unless public visibility was
requested. Object format defaults to SHA-1; use `--object-format sha256` only
when requested and compatible with the intended clients.

Use `repo control` for settings and `repo collaborators` for access. Read the
specific subcommand's `--help` before constructing a mutation. For Git traffic,
inspect the repository's clone information and existing remotes; do not replace
an existing GitHub remote or push to every remote without authorization.

`repo delete` is a soft delete; `repo restore` restores within the recovery
period. `repo purge` is permanent. Confirm the exact target and user intent
before destructive operations. Do not invent confirmation flags.

## Other API work

Discover installed commands rather than guessing flags:

```sh
gtd me ssh-keys --help
gtd org --help
gtd admin --help
gtd admin storage --help
gtd admin backup --help
```

Typed commands cover instance settings, authentication/OIDC, integrity,
storage, backups, and audit history. Prefer them to raw API calls. For an
endpoint without a typed command, inspect the current API schema or server
routes before using `api`. Paths are relative to `/api/v1`:

```sh
gtd api user
```

JSON commands write JSON to stdout, errors to stderr, and return nonzero on
failure. Use `--body-file` for supported JSON requests; `--body-file -` reads
stdin and cannot share stdin with a token source. Do not guess mutation bodies.

Token scopes matter: reads require `read`; repository, organization, and admin
mutations require `write`; SSH-key changes require `ssh_keys`. Admin commands
also require an administrator account. A token does not bypass permissions or
browser-only account-security and restore requirements.

Backup downloads use `admin backup download <provider-id> <backup-key>
--output <path>`. They replace the output only after a complete transfer.
Backup and storage progress commands emit JSON Lines; wait for successful
completion rather than treating an operation ID as success.

## Deployment and troubleshooting

The NixOS configuration is in `~/nixos`. Use the user's update script, which
pulls, stages changes, rebuilds, and commits/pushes local changes on success:

```sh
env NIXOS_UPDATE_NO_GIT=0 NIXOS_UPDATE_HOST=neo \
  fish ~/nixos/scripts/nixos/update
```

Run that script on each requested host, replacing `neo` with that host's
hostname (`vd`, `neo`, or `kiwi`). Review the intended local changes first
because the script stages all changes. Do not bypass it with a separate
activation or commit workflow. Shared client settings live in
`modules/nixos/applications/default.nix`, SOPS definitions in
`modules/nixos/services/sops/default.nix`, the encrypted token in
`secrets/gitadel.json`, and Neo's server configuration in `hosts/neo/gitadel.nix`.

Check disk headroom before rebuilding Neo. Build dependencies can exhaust its
root filesystem even when the final runtime closure is smaller. When needed,
prebuild on vd, measure the missing runtime closure against Neo's free space,
and copy it before running Neo's update script. Never delete generations,
archives, or application data, or change filesystem reserves without approval.

After deployment, verify `/run/current-system/sw/bin/gtd --version` and
`gtd auth status` from each affected client, `systemctl is-active gitadel` on
Neo, and `/healthz` reporting both `status` and `database` as `ok`.
`auth status` should show the intended server and user; with the fleet's Nix
defaults its token source is `environment-file`. `/health` can return the frontend HTML and is not a health
check. For connection errors, check the selected server, NetBird reachability,
and proxy environment before changing configuration. A 401/403 calls for
credential, scope, and account-permission checks, not secret disclosure.

The Gitadel checkout is normally `~/dev/gitadel`. Read its current `INSTALL.md`
for API/client behavior and its loaded repository instructions before source
work. The server's offline `gitadel lfs` migration commands require stopping
Gitadel; they are not interchangeable with the remote `gtd`.
