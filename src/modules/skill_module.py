from pathlib import Path

from src.modules.base import BaseModules

SKILLS_DIR = Path(__file__).resolve().parent.parent / "assets" / "skills"


class SkillModule(BaseModules):
    """Loads prompt skills from `assets/skills/<name>/SKILL.md`."""

    def __init__(self, skills_dir: Path = SKILLS_DIR) -> None:
        super().__init__()
        self.skills_dir = skills_dir

    def list(self) -> list[str]:
        return sorted(p.parent.name for p in self.skills_dir.glob("*/SKILL.md"))

    def load(self, name: str) -> str:
        """Return the skill body (frontmatter removed). Raises KeyError if unknown."""
        path = self.skills_dir / name / "SKILL.md"
        if not path.is_file() or path.resolve().parent.parent != self.skills_dir.resolve():
            raise KeyError(name)
        text = path.read_text()
        if text.startswith("---"):
            text = text.split("---", 2)[2]
        return text.strip()
