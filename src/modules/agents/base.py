from src.modules.agents.prompts import load_prompt_template
from src.modules.agents.skills import load_skill
from src.modules.base import BaseModules


class BaseAgent(BaseModules):
    """An agent owns a prompt template (assets/prompt_templates/<name>.md) plus its skills
    (assets/skills/<name>/SKILL.md)."""

    prompt_template: str = "default"
    skills: tuple[str, ...] = ()

    def __init__(self, skills: list[str] | None = None):
        super().__init__()
        if skills is not None:
            self.skills = tuple(skills)
        # load eagerly so a missing template or skill fails when the agent is built
        self.base_prompt = load_prompt_template(self.prompt_template)
        self._skill_texts = [load_skill(name) for name in self.skills]

    @property
    def system_prompt(self) -> str:
        return "\n\n".join([self.base_prompt, *self._skill_texts])

    def execute(self, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement this method.")

    async def aexecute(self, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement this method.")
