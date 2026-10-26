# assets/

Static files used by the app.

```
assets/
├── prompt_templates/<agent>.md   the prompt of each agent
└── skills/<name>/SKILL.md        skills: YAML frontmatter (name, description) + instructions
```

Each agent has its prompt in `prompt_templates/`: an agent sets `prompt_template = "<agent>"` (default
`default`; `ChatAgent` uses `chat`) and `BaseAgent` loads it through `src/modules/agents/prompts.py`.
A missing template raises `KeyError` when the agent is built. To add an agent prompt, create
`prompt_templates/<agent>.md`.

Current skills: `summarize`, `answer-with-sources`.

Skills belong to agents, not to a separate module. `BaseAgent` (`src/modules/agents/base.py`) takes a
list of skill names, loads each `SKILL.md` through `src/modules/agents/skills.py`, and appends the bodies
(frontmatter removed) to its prompt template as `system_prompt`. An unknown skill name raises `KeyError`
when the agent is built.

```python
agent = ChatAgent(skills=["summarize"])
```

Add a skill by creating `skills/<name>/SKILL.md`, then list it in the agent that should use it.
