<p align="center">
  <img src="assets/logo.png" alt="Agent skills" width="320" />
</p>

<p align="center">
  <a href="https://github.com/Fractal-Tess/agents"><img src="https://img.shields.io/badge/github-Fractal_Tess%2Fagents-181717?logo=github&logoColor=white" alt="GitHub"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-22c55e" alt="MIT license"></a>
  <a href="skills/"><img src="https://img.shields.io/badge/skills-18-f97316" alt="18 skills"></a>
</p>

# Agent skills

Agent skills for coding assistants, kept in `~/.agents` and versioned here.

This repo holds what I run my agents with: one folder per skill in the standard `skills/<name>/SKILL.md` layout, plus `.skill-lock.json`, which records where each skill came from and when it was installed. The skills here are the same set the omp harness loads, so the repo works as a durable, diffable copy.

- `unslop` (from [poteto/noodle](https://github.com/poteto/noodle)) de-AIs prose: cuts em dashes, AI vocabulary, significance inflation, and chatbot filler
- `ft-readme-style` and `ft-visual-style` keep project READMEs and image prompts in a consistent voice
- the rest are the omp session skills: agent-browser, impeccable, design-taste-frontend, research, react-bits-pro, scorch, svelte, rust, and utility skills

## Fastest way in

Clone it into `~/.agents`. Most harnesses pick up skills from there automatically:

```sh
git clone git@github.com:Fractal-Tess/agents.git ~/.agents
```

## Install

Full setup, per-agent paths, and sync instructions: [INSTALL.md](INSTALL.md)

## License

MIT. See [LICENSE](LICENSE). The skills inside are third-party where noted; their terms apply to that content.
