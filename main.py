"""Entry point for the news-image-20261125 submission.

Copies the shipped newspaper page image (``art.png``, stored next
to this file) to ``entry.png`` in the output directory, verifies
the copy by size and SHA-256, and repeats the copy under a temp
name to prove both runs write identical bytes.
Standard library only.
"""

import os
from pathlib import Path

import copier


def verify_dimensions(path: Path, expected: int = 1024) -> tuple[int, int]:
    """Return the (width, height) of the PNG at ``path`` from its header.

    Parses the 8-byte PNG signature and the IHDR chunk directly:
    width and height are big-endian uint32 at byte offsets 16 and 20.
    Exits non-zero unless the image is exactly ``expected`` square.
    """
    with path.open("rb") as fh:
        header = fh.read(24)
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit(f"{path.name}: not a PNG file (bad signature)")
    width = int.from_bytes(header[16:20], "big")
    height = int.from_bytes(header[20:24], "big")
    if (width, height) != (expected, expected):
        raise SystemExit(
            f"{path.name}: expected {expected}x{expected}, got {width}x{height}"
        )
    return width, height


def main() -> None:
    here = Path(__file__).resolve().parent
    source = here / "art.png"
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    dest = out_dir / "entry.png"

    # First copy: the deliverable.
    size, digest = copier.copy_entry(source, dest)
    assert copier.verify_entry(dest, size, digest), "entry.png failed verification"

    # The deliverable must also be a 1024x1024 PNG, checked by header.
    width, height = verify_dimensions(dest)

    # Second copy to a temp name: hashes must match the first run.
    repeat = out_dir / "entry.repeat.tmp.png"
    size2, digest2 = copier.copy_entry(source, repeat)
    assert (size2, digest2) == (size, digest), "repeat copy differs"
    assert copier.verify_entry(repeat, size, digest), "repeat copy failed verification"
    repeat.unlink()

    print(f"entry.png: {size} bytes sha256={digest[:16]}… verified, {width}x{height}")


if __name__ == "__main__":
    main()
