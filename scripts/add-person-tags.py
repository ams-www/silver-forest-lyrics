#!/usr/bin/env python3
"""Add contributor/person tags to Hugo lyric pages before building."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PERSONS_FILE = ROOT / "persons.txt"
LYRICS_DIR = ROOT / "content" / "lyrics"

TAG_RE = re.compile(r"^(tags:\s*\[)(.*?)(\]\s*)$", re.MULTILINE)
FRONT_MATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", re.DOTALL)
QUOTED_RE = re.compile(r'"([^"]*)"|\'([^\']*)\'')

CREDIT_LINE_RE = re.compile(
    r"^\s*(?:"
    r"lyrics?|vocal|vocals?|arrange|arranger|composer|composition|music|"
    r"remix|chorus|guitar|bass|drums?|piano|"
    r"歌|作詞|作曲|編曲|コーラス|コーラス＆CV|CV"
    r")\s*[:：]\s*(.+?)\s*$",
    re.IGNORECASE,
)

TOKEN_SPLIT_RE = re.compile(r"[\s,，、;；/／&＆+＋()（）\[\]【】「」・]+")


def load_persons() -> list[str]:
    return [
        line.strip()
        for line in PERSONS_FILE.read_text(encoding="utf-8-sig").splitlines()
        if line.strip()
    ]


def extract_tags(front_matter: str) -> list[str]:
    match = TAG_RE.search(front_matter)
    if not match:
        return []
    return [first or second for first, second in QUOTED_RE.findall(match.group(2))]


def detect_persons(body: str, persons: list[str]) -> list[str]:
    found: list[str] = []

    for line in body.splitlines():
        match = CREDIT_LINE_RE.match(line)
        if not match:
            continue

        tokens = [token for token in TOKEN_SPLIT_RE.split(match.group(1)) if token]
        for person in persons:
            if person in tokens and person not in found:
                found.append(person)

    return found


def update_page(path: Path, persons: list[str]) -> bool:
    text = path.read_text(encoding="utf-8-sig")

    front_match = FRONT_MATTER_RE.match(text)
    if not front_match:
        return False

    front_matter = front_match.group(1)
    body = text[front_match.end():]

    existing = extract_tags(front_matter)
    detected = detect_persons(body, persons)
    tags = existing + [person for person in detected if person not in existing]

    if tags == existing:
        return False

    tag_line = "tags: [" + ", ".join(f'"{tag}"' for tag in tags) + "]"

    if TAG_RE.search(front_matter):
        new_front = TAG_RE.sub(tag_line, front_matter, count=1)
    else:
        title_match = re.search(r"^title:\s*.*$", front_matter, re.MULTILINE)
        if title_match:
            new_front = (
                front_matter[:title_match.end()]
                + "\n"
                + tag_line
                + front_matter[title_match.end():]
            )
        else:
            new_front = tag_line + "\n" + front_matter

    new_text = "---\n" + new_front.rstrip("\n") + "\n---\n" + body.lstrip("\n")
    path.write_text(new_text, encoding="utf-8")
    return True


def main() -> None:
    persons = load_persons()
    changed = 0

    for path in sorted(LYRICS_DIR.glob("*.md")):
        if update_page(path, persons):
            changed += 1

    print(f"Updated person tags in {changed} lyric pages.")


if __name__ == "__main__":
    main()
