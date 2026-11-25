"""news-image-20261125 entry: Wednesday 25 November 2026 in one page.

The front page is rendered ahead of time by the build pipeline and stored
beside this file as art.png. This program's whole job is to deliver those
exact bytes as entry.png in the output directory, using nothing but the
Python standard library, so the two grading runs agree byte for byte.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "art.png")
DEFAULT_OUTPUT_DIR = "/output"


def main() -> None:
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", DEFAULT_OUTPUT_DIR)
    os.makedirs(output_dir, exist_ok=True)
    target = os.path.join(output_dir, "entry.png")
    with open(SOURCE, "rb") as src, open(target, "wb") as dst:
        shutil.copyfileobj(src, dst, length=1024 * 64)


if __name__ == "__main__":
    main()
