"""Preview changes to generated repository documents without writing files."""

from __future__ import annotations

import argparse
import json
from difflib import unified_diff
from pathlib import Path

from .cli import generated_documents


def generated_document_diffs(root: Path | str = ".") -> list[dict[str, str]]:
    """Return structured diffs for generated documents that are missing or stale."""
    project_root = Path(root)
    diffs: list[dict[str, str]] = []
    for document in generated_documents(project_root):
        path = project_root / document.path
        exists = path.is_file()
        current = path.read_text(encoding="utf-8") if exists else ""
        expected = document.render()
        if current == expected:
            continue
        fromfile = document.path if exists else "/dev/null"
        lines = unified_diff(
            current.splitlines(),
            expected.splitlines(),
            fromfile=fromfile,
            tofile=document.path,
            lineterm="",
        )
        diffs.append(
            {
                "path": document.path,
                "status": "stale" if exists else "missing",
                "diff": "\n".join(lines),
            }
        )
    return diffs


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Preview generated-document changes without writing files.")
    parser.add_argument("--root", type=Path, default=Path("."), help="Repository root.")
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format. JSON is useful for automation.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    diffs = generated_document_diffs(args.root)
    if args.format == "json":
        print(json.dumps({"current": not diffs, "documents": diffs}, indent=2))
        return 0 if not diffs else 1
    if not diffs:
        print("Generated documentation is current.")
        return 0
    print("\n\n".join(item["diff"] for item in diffs))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())