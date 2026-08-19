# Install

These are plain skill folders. There is no build step and no package manager.

## Into an agent's skills directory

Most coding agents load skills from a directory of `SKILL.md` files. Copy the folder:

```sh
cp -r skills/<name> ~/.claude/skills/
cp -r skills/<name> ~/.codex/skills/
```

Substitute the agent's skills path. Known paths on this machine: `~/.claude/skills`, `~/.codex/skills`, `~/.omp/agent/skills`.

## omp

The omp harness loads the live set from `~/.omp/agent/skills`. To change what runs, edit there. To keep a versioned copy, edit here and sync.

## Adding a new skill

1. Create `skills/<name>/SKILL.md` with `name` and `description` in the frontmatter.
2. Add a `.skill-lock.json` entry with the source, or leave it out for local-only skills.
3. Commit.

## Removing a skill

Delete the folder and its lock entry. The repo is private; deletions are recoverable from git history.
