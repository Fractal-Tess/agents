# Agent skills

What I keep in `~/.agents`: skills for coding agents, plus the install registry.

## What's here

- `skills/<name>/SKILL.md` — one folder per skill, standard layout. Point your agent at it or copy it into its own skills directory.
- `.skill-lock.json` — the install registry: which skill came from where, and when it was installed.

The `unslop` skill came from [poteto/noodle](https://github.com/poteto/noodle). The rest are the skills the omp harness loads at `~/.omp/agent/skills`; this repo is a durable copy, not the live source.

## Installing a skill

Copy the folder into your agent's skills directory:

```sh
cp -r skills/unslop ~/.claude/skills/
```

Or, for agent CLIs that support it, point at the repo path directly.

## Notes

- Keep the lock file in sync when you add or remove skills.
- The harness resolves `skill://` names from `~/.omp/agent/skills`, not from this repo. Edit there if you want a skill to change live; edit here if you want the change versioned.
