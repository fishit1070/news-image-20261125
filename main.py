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


def main() -> None:
    here = Path(__file__).resolve().parent
    source = here / "art.png"
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    dest = out_dir / "entry.png"

    # First copy: the deliverable.
    size, digest = copier.copy_entry(source, dest)
    assert copier.verify_entry(dest, size, digest), "entry.png failed verification"

    # Second copy to a temp name: hashes must match the first run.
    repeat = out_dir / "entry.repeat.tmp.png"
    size2, digest2 = copier.copy_entry(source, repeat)
    assert (size2, digest2) == (size, digest), "repeat copy differs"
    assert copier.verify_entry(repeat, size, digest), "repeat copy failed verification"
    repeat.unlink()

    print(f"entry.png: {size} bytes sha256={digest[:16]}… verified")


if __name__ == "__main__":
    main()
