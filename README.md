<p align="center">
  <img src="assets/logo.png" alt="Agent skills" width="160" />
</p>

# Agent skills

Agent skills for coding assistants, kept in `~/.agents` and versioned here.

This repo holds what I run my agents with: one folder per skill in the standard `skills/<name>/SKILL.md` layout, plus `.skill-lock.json`, which records where each skill came from and when it was installed. The skills here are the same set the omp harness loads, so the repo works as a durable, diffable copy.

- `unslop` (from [poteto/noodle](https://github.com/poteto/noodle)) de-AIs prose: cuts em dashes, AI vocabulary, significance inflation, and chatbot filler
- `ft-readme-style` and `ft-visual-style` keep project READMEs and image prompts in a consistent voice
- the rest are the omp session skills: agent-browser, impeccable, design-taste-frontend, research, react-bits-pro, scorch, svelte, rust, and utility skills

## Fastest way in

Copy one skill into your agent's skills directory:

```sh
cp -r skills/unslop ~/.claude/skills/
```

## Install

Full setup, per-agent paths, and sync instructions: [INSTALL.md](INSTALL.md)

## License

No license yet. This is a personal repo; ask before reusing the skill text.
