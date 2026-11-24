"""Validate Markdown links, prohibited wording, and the required M00 roadmap sections."""

import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SKIP = {".git", ".next", ".venv", "node_modules", "__pycache__", ".mypy_cache", ".ruff_cache"}
DOCUMENT_ENDINGS = {
    ".md",
    ".py",
    ".yml",
    ".yaml",
    ".txt",
    ".svg",
    ".json",
    ".ts",
    ".tsx",
    ".mjs",
    ".css",
    ".excalidraw",
}
BANNED = (
    "hack" + "athon",
    "compe" + "tition",
    "ju" + "dge",
    "PS" + "-07",
    "PS" + "07",
    "Uni" + "sys",
    "Code" + "Red",
)
LINK = re.compile(r"!?\[[^\]]*\]\(([^\s)]+)(?:\s+\"[^\"]*\")?\)")
HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$", re.MULTILINE)
REQUIRED = {
    "Objective",
    "Why it matters",
    "Prerequisites and dependencies",
    "Detailed task checklist",
    "Deliverables",
    "Acceptance criteria",
    "Test plan",
    "Risks and mitigations",
    "Exit checklist",
    "Related docs",
}


def heading_ids(text):
    seen = {}
    for heading in HEADING.findall(text):
        slug = re.sub(r"[^\w\s-]", "", heading.lower()).replace(" ", "-")
        count = seen.get(slug, 0)
        seen[slug] = count + 1
        yield f"{slug}-{count}" if count else slug


def main():
    files = [
        p
        for p in ROOT.rglob("*")
        if p.is_file()
        and not SKIP.intersection(p.relative_to(ROOT).parts)
        and p.suffix in DOCUMENT_ENDINGS
    ]
    docs = [p for p in files if p.suffix == ".md"]
    errors = []
    for path in files:
        if path.is_symlink():
            continue
        contents = path.read_text(encoding="utf-8")
        match = re.search(r"\b(?:" + "|".join(BANNED) + r")\w*\b", contents, re.I)
        if match:
            errors.append(f"{path.relative_to(ROOT)}: restricted terminology")
        if path.suffix != ".md":
            continue
        for link in LINK.findall(contents):
            if link.startswith(("http://", "https://", "mailto:")):
                continue
            parts = urlsplit(link.strip("<>"))
            target = (path.parent / unquote(parts.path)).resolve() if parts.path else path
            if not target.is_file() and not target.is_dir():
                errors.append(f"{path.relative_to(ROOT)}: broken link {link}")
            elif (
                parts.fragment
                and target.suffix == ".md"
                and unquote(parts.fragment) not in set(heading_ids(target.read_text()))
            ):
                errors.append(f"{path.relative_to(ROOT)}: broken anchor {link}")
    roadmap = ROOT / "docs/roadmap"
    index = (ROOT / "docs/diagrams/README.md").read_text()
    for i in range(12):
        steps = list(roadmap.glob(f"M{i:02d}-*.md"))
        if len(steps) != 1 or not REQUIRED.issubset(HEADING.findall(steps[0].read_text())):
            errors.append(f"M{i:02d}: missing milestone or required heading")
    roadmap_text = "\n".join(p.read_text() for p in roadmap.glob("*.md"))
    for i in range(1, 7):
        assets = list((ROOT / "docs/diagrams/img").glob(f"R{i:02d}-*.svg"))
        if len(assets) != 1 or assets[0].name not in index or assets[0].name not in roadmap_text:
            errors.append(f"R{i:02d}: missing, unindexed, or unembedded figure")
    if errors:
        raise SystemExit("\n".join(errors))
    print(
        f"Checked {len(docs)} Markdown files, 12 milestones, 6 roadmap diagrams, and terminology."
    )


if __name__ == "__main__":
    main()
