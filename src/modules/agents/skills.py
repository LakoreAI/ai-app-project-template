from pathlib import Path

SKILLS_DIR = Path(__file__).resolve().parents[2] / "assets" / "skills"


def list_skills(skills_dir: Path = SKILLS_DIR) -> list[str]:
    return sorted(p.parent.name for p in skills_dir.glob("*/SKILL.md"))


def load_skill(name: str, skills_dir: Path = SKILLS_DIR) -> str:
    """Return a skill body (frontmatter removed). Raises KeyError if unknown."""
    path = skills_dir / name / "SKILL.md"
    if not path.is_file() or path.resolve().parent.parent != skills_dir.resolve():
        raise KeyError(name)
    text = path.read_text()
    if text.startswith("---"):
        text = text.split("---", 2)[2]
    return text.strip()
