from pathlib import Path

PROMPT_TEMPLATES_DIR = Path(__file__).resolve().parents[2] / "assets" / "prompt_templates"


def load_prompt_template(name: str, templates_dir: Path = PROMPT_TEMPLATES_DIR) -> str:
    """Return `assets/prompt_templates/<name>.md`. Raises KeyError if unknown."""
    path = templates_dir / f"{name}.md"
    if not path.is_file() or path.resolve().parent != templates_dir.resolve():
        raise KeyError(name)
    return path.read_text().strip()
