"""The Long Roast entry: write one fixed satirical sentence to /output/entry.txt.

The roast is a fixed string literal. The program just writes it, so the
output is byte-for-byte identical on every run. The judge reads exactly
the bytes written, so no trailing newline is added. Before writing, the
line is validated fail-closed (exactly one sentence, 1-320 characters);
a violation exits non-zero and writes nothing.

Standard library only. No network access, no randomness, no arguments.
Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
from pathlib import Path

LINE = (
    'The committee that will decide what your AI may say spent three hours '
    'in a hearing titled "How to Save As PDF" \u2014 and adjourned without '
    "saving anything."
)


def validate_line(line: str) -> None:
    """Fail closed: the roast must be exactly one sentence, 1-320 chars.

    Runs BEFORE anything is written. Raises SystemExit (non-zero exit,
    no file created or modified) on any violation, so a bad line can
    never reach /output/entry.txt.
    """
    if not line:
        raise SystemExit("refusing to write: roast line is empty")
    if not 1 <= len(line) <= 320:
        raise SystemExit(
            f"refusing to write: roast line is {len(line)} characters, "
            "must be 1-320"
        )
    terminators = sum(1 for ch in line if ch in ".!?")
    if terminators != 1:
        raise SystemExit(
            "refusing to write: roast line has "
            f"{terminators} sentence-terminating marks, must be exactly 1"
        )


def main() -> None:
    validate_line(LINE)
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    dest = output_dir / "entry.txt"
    dest.write_text(LINE, encoding="utf-8")
    # Guard against a truncated or partial write: the file must be the
    # exact bytes of the line.
    if dest.read_text(encoding="utf-8") != LINE:
        dest.unlink(missing_ok=True)
        raise SystemExit("entry.txt does not match the roast line")
    print(f"wrote {dest} ({dest.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
