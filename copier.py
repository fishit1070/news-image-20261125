"""Copy helper for the news-image entry.

The entry image is shipped in the repository as data (``art.png``).
This module copies it to the output location and proves, by size
and SHA-256, that the bytes written are exactly the bytes shipped.
Only the Python standard library is used.
"""

import hashlib
from pathlib import Path


def sha256_of(data: bytes) -> str:
    """Return the hex SHA-256 digest of *data*."""
    return hashlib.sha256(data).hexdigest()


def copy_entry(source: Path, dest: Path) -> tuple[int, str]:
    """Copy *source* to *dest*, creating parent directories.

    Returns a ``(size, sha256)`` tuple describing the bytes copied,
    so callers can verify the copy without re-reading the source.
    """
    data = source.read_bytes()
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    return len(data), sha256_of(data)


def verify_entry(path: Path, expected_size: int, expected_sha256: str) -> bool:
    """Re-read *path* and check its size and SHA-256.

    Returns True only when both the byte count and the digest of
    the file on disk match the expected values exactly.
    """
    if not path.is_file():
        return False
    data = path.read_bytes()
    return len(data) == expected_size and sha256_of(data) == expected_sha256
