"""Entry point for the news-image-20261125 make.fun submission.

Delivers the finished front-page image (art.png, stored beside this
file) to the grader output directory as entry.png, verified by size
and SHA-256, with a repeat copy to prove determinism. Standard
library only.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Make the sibling module importable even under `python3 -P -s`,
# where the script's own directory is not added to sys.path.
_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

import copier

_PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def png_size(path) -> tuple[int, int]:
    """Return the (width, height) of a PNG, requiring 1024x1024.

    Reads only the first 24 bytes: the 8-byte PNG signature followed
    by the IHDR chunk header, whose width and height fields are
    big-endian uint32 values at byte offsets 16 and 20.
    """
    with Path(path).open("rb") as handle:
        header = handle.read(24)

    if len(header) < 24 or header[:8] != _PNG_SIGNATURE:
        raise SystemExit(f"{path}: not a PNG file (bad signature)")

    width = int.from_bytes(header[16:20], "big")
    height = int.from_bytes(header[20:24], "big")
    if (width, height) != (1024, 1024):
        raise SystemExit(
            f"{path}: expected 1024x1024 image, got {width}x{height}"
        )
    return width, height


def main() -> None:
    source = _HERE / "art.png"
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    destination = output_dir / "entry.png"

    size, digest = copier.copy_verified(source, destination)
    assert copier.matches(destination, size, digest), (
        "entry.png failed verification after the first copy"
    )
    width, height = png_size(destination)

    # A second copy to a temporary sibling proves the process is
    # deterministic: same size, same digest, same verification.
    repeat = output_dir / "entry.repeat.tmp.png"
    repeat_size, repeat_digest = copier.copy_verified(source, repeat)
    assert (repeat_size, repeat_digest) == (size, digest), (
        "repeat copy diverged from the first copy"
    )
    assert copier.matches(repeat, size, digest), (
        "repeat copy failed verification"
    )
    repeat.unlink()

    print(f"entry.png: {size} bytes, {width}x{height}, sha256 {digest[:16]}")


if __name__ == "__main__":
    main()
