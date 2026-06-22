#!/usr/bin/env python3

from pathlib import Path
import re

ROOT = Path(".")
LYRICS_DIR = ROOT / "Lyrics"
PERSONS_FILE = ROOT / "persons.txt"


def load_persons():
    return [
        line.strip()
        for line in PERSONS_FILE.read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    ]


def detect_people(text, persons):
    found = []

    lower = text.lower()

    for person in persons:
        if person.lower() in lower:
            found.append(person)

    return sorted(set(found))


def parse_frontmatter(text):
    if not text.startswith("---\n"):
        return None, text

    parts = text.split("---\n", 2)

    if len(parts) < 3:
        return None, text

    return parts[1], parts[2]


def build_frontmatter(old_frontmatter, people):

    lines = []

    if old_frontmatter:

        skip = False

        for line in old_frontmatter.splitlines():

            if line.startswith("related_people:"):
                skip = True
                continue

            if skip:
                if line.startswith("  - "):
                    continue
                skip = False

            lines.append(line)

    lines.append("related_people:")

    for person in people:
        lines.append(f"  - {person}")

    return "\n".join(lines)


def process_file(path, persons):

    text = path.read_text(encoding="utf-8")

    people = detect_people(text, persons)

    if not people:
        return False

    frontmatter, body = parse_frontmatter(text)

    new_frontmatter = build_frontmatter(
        frontmatter,
        people
    )

    new_text = (
        "---\n"
        + new_frontmatter
        + "\n---\n"
        + body.lstrip()
    )

    if new_text != text:

        path.write_text(
            new_text,
            encoding="utf-8"
        )

        print(
            f"updated: {path} ({len(people)} people)"
        )

        return True

    return False


def main():

    persons = load_persons()

    changed = 0

    for md in LYRICS_DIR.rglob("*.md"):

        if process_file(md, persons):
            changed += 1

    print(
        f"\nFinished. {changed} files changed."
    )


if __name__ == "__main__":
    main()
