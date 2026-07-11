"""Preview changes to generated repository documents without writing files."""

from __future__ import annotations

import argparse
from difflib import unified_diff
from pathlib import Path

from .cli import generated_documents


def generated_document_diffs(root: Path | str = ".") -> list[str]:
    """Return unified diffs for generated documents that are missing or stale."""
    project_root = Path(root)
    diffs: list[str] = []
    for document in generated_documents(project_root):
        path = project_root / document.path
        current = path.read_text(encoding="utf-8") if path.is_file() else ""
        expected = document.render()
        if current == expected:
            continue
        fromfile = document.path if path.is_file() else "/dev/null"
        lines = unified_diff(
            current.splitlines(),
            expected.splitlines(),
            fromfile=fromfile,
            tofile=document.path,
            lineterm="",
        )
        diffs.append("\n".join(lines))
    return diffs


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Preview generated-document changes without writing files.")
    parser.add_argument("--root", type=Path, default=Path("."), help="Repository root.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    diffs = generated_document_diffs(args.root)
    if not diffs:
        print("Generated documentation is current.")
        return 0
    print("\n\n".join(diffs))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
