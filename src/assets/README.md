# assets/

Static files used by the app.

```
assets/
└── skills/<name>/SKILL.md   prompt skills: YAML frontmatter (name, description) + instructions
```

Current skills: `summarize`, `answer-with-sources`.

Skills are loaded by `SkillModule` (`src/modules/skill_module.py`): `list()` returns the names and
`load(name)` returns the body without the frontmatter. `POST /chat` with `"skill": "<name>"` uses that
body as the system prompt; an unknown name returns 404. Add a skill by creating
`skills/<name>/SKILL.md`.
