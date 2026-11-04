#!/usr/bin/env python3
"""Package both role skills with local copies of the shared rules.

Usage: python3 scripts/package_skills.py --output /absolute/path/to/new-directory

The output contains two sibling skill directories, each with its own shared
resources. It can be installed as a pair without the source package's shared/
directory. Sources and existing output directories are never overwritten.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import shutil
import tempfile


SOURCE_ROOT = Path(__file__).resolve().parent.parent
ROLE_NAMES = ("chinese-expression", "chinese-expression-review")
MARKDOWN_LINK = re.compile(r"(?P<label>!?\[[^\]]*\])\((?P<target>[^)]+)\)")


def local_target(file: Path, target: str) -> Path | None:
    if target.startswith("#") or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
        return None
    path = target.split("#", 1)[0]
    return (file.parent / path).resolve()


def check_links(root: Path, files: list[Path]) -> None:
    for file in files:
        for match in MARKDOWN_LINK.finditer(file.read_text(encoding="utf-8")):
            target = local_target(file, match["target"])
            if target is None:
                continue
            if not target.is_relative_to(root.resolve()) or not target.is_file():
                raise ValueError(f"Invalid local reference in {file}: {match['target']}")


def prepare_bundle(destination: Path) -> None:
    shared = SOURCE_ROOT / "shared"
    if not shared.is_dir() or not list(shared.glob("*.md")):
        raise ValueError("The source package has no shared Markdown rules.")

    role_dirs = [SOURCE_ROOT / "skills" / name for name in ROLE_NAMES]
    for role in role_dirs:
        if not (role / "SKILL.md").is_file():
            raise ValueError(f"Missing role entrypoint: {role / 'SKILL.md'}")
    source_files = [file for role in role_dirs for file in role.rglob("*.md")]
    check_links(SOURCE_ROOT, source_files + list(shared.rglob("*.md")))

    with tempfile.TemporaryDirectory(
        prefix="chinese-expression-bundle-", dir=destination.parent
    ) as temporary:
        staged = Path(temporary) / "bundle"
        staged.mkdir()
        for role in role_dirs:
            packaged_role = staged / role.name
            shutil.copytree(role, packaged_role)
            packaged_shared = packaged_role / "references" / "shared"
            shutil.copytree(shared, packaged_shared)
            license_file = SOURCE_ROOT / "LICENSE"
            if license_file.is_file():
                shutil.copy2(license_file, packaged_role / "LICENSE")

            for original in role.rglob("*.md"):
                packaged = packaged_role / original.relative_to(role)

                def rewrite(match: re.Match[str]) -> str:
                    target = local_target(original, match["target"])
                    if target is None or not target.is_relative_to(shared.resolve()):
                        return match.group(0)
                    local_copy = packaged_shared / target.relative_to(shared.resolve())
                    reference = os.path.relpath(local_copy, packaged.parent)
                    suffix = match["target"].partition("#")[2]
                    if suffix:
                        reference += "#" + suffix
                    return f"{match['label']}({reference})"

                text = MARKDOWN_LINK.sub(rewrite, original.read_text(encoding="utf-8"))
                packaged.write_text(text, encoding="utf-8")

        check_links(staged, list(staged.rglob("*.md")))
        if destination.exists():
            raise ValueError(f"Output directory already exists: {destination}")
        staged.rename(destination)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", "-o", required=True, type=Path)
    args = parser.parse_args()
    destination = args.output.expanduser().resolve()
    if destination.exists() or destination.is_relative_to(SOURCE_ROOT):
        parser.error("Use a new output directory outside the source package.")
    if not destination.parent.is_dir():
        parser.error("The output directory's parent must already exist.")
    try:
        prepare_bundle(destination)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    print(f"Packaged both role skills: {destination}")


if __name__ == "__main__":
    main()
