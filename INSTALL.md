# Install

Skills live in `skills/<name>/SKILL.md`. Standard layout, no build step.

## Get the repo

Clone it (private, SSH):

```sh
git clone git@github.com:Fractal-Tess/agents.git ~/.agents
```

To update, pull:

```sh
git -C ~/.agents pull
```

This repo is the source of truth. The copy on disk is whatever the latest commit has; `git pull` is the only update path that keeps both in sync.

## Automatic loading

These harnesses load skills from `.agents/skills` (project) and `~/.agents/skills` (user) with no setup:

| Harness | Reads `.agents`? | Source |
|---|---|---|
| Codex CLI | yes, project + `~/.agents/skills` | learn.chatgpt.com/docs/build-skills |
| Gemini CLI | yes, `.agents/skills` beats `.gemini/skills` | geminicli.com/docs/cli/skills |
| Cursor | yes, project + `~/.agents/skills` | cursor.com/docs/skills.md |
| Windsurf (Devin Desktop) | yes, cross-agent compat | docs.devin.ai/desktop/cascade/skills.md |
| Amp | yes, project + `~/.agents/skills` | ampcode.com/manual/agent-skills.md |
| OpenCode | yes, project + `~/.agents/skills` | opencode.ai/docs/skills |
| Roo Code | yes, project + `~/.agents/skills` | docs.roocode.com/features/skills |
| Cline | yes, in source; undocumented | cline/cline, apps/vscode/src/core/storage/skill-directories.ts |
| omp | yes, native `.agents/skills`, `.agents/rules` | embedded in omp binary |

If yours is in this list, clone into `~/.agents` or use the repo as the project `.agents/` directory and you are done. Skills are picked up on the next session.

## Harnesses that do not load .agents

- **Claude Code** — reads only `.claude/skills` and `~/.claude/skills`; the docs contain no `.agents` path. It also does not read AGENTS.md (docs say "Claude Code reads CLAUDE.md, not AGENTS.md"). Fix: symlink the skills in once:

  ```sh
  ln -s ~/.agents/skills/* ~/.claude/skills/
  ```

  Symlinked skill dirs are followed. Sources: code.claude.com/docs/en/skills, code.claude.com/docs/en/memory.

- **Qwen Code** — scans `.qwen/skills` and `~/.qwen/skills` only. Shared dirs need explicit config: set `"skills.directories": ["~/.agents/skills"]` in settings.json. Source: qwenlm.github.io/qwen-code-docs, weekly update 2026-07-30.

- **JetBrains Junie** — scans `.junie/skills` (project) and `~/.junie/skills` (user). It detects other agents' skill dirs only to suggest an import, never loads them. Fix: `ln -s ~/.agents/skills/* ~/.junie/skills/`. Source: junie.jetbrains.com/docs/agent-skills.html.

- **Aider** — no skills system at all. Load a conventions file explicitly with `/read` or `--read`. Source: aider.chat/docs/usage/conventions.html.

## Removing a skill

Delete the folder and its `.skill-lock.json` entry, then commit. The repo is the durable copy; git history is the undo.
