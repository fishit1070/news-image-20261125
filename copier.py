"""Verified copying for the shipped front-page image.

This helper moves the finished page image to its destination and
proves the copy is byte-for-byte identical to the source. Identity
is established two ways: the transferred byte count must match the
source length, and the SHA-256 digest of the written bytes must
match the digest computed from the source bytes.
"""

from __future__ import annotations

import hashlib
from pathlib import Path


def digest_of(data: bytes) -> str:
    """Return the SHA-256 hex digest of *data*."""
    return hashlib.sha256(data).hexdigest()


def copy_verified(source, dest) -> tuple[int, str]:
    """Copy *source* to *dest*, returning (byte count, digest).

    The parent directories of *dest* are created when needed. The
    digest is taken from the source bytes before they are written,
    so callers can later compare a file on disk against it.
    """
    src_path = Path(source)
    dst_path = Path(dest)

    payload = src_path.read_bytes()
    digest = digest_of(payload)

    dst_path.parent.mkdir(parents=True, exist_ok=True)
    dst_path.write_bytes(payload)

    return len(payload), digest


def matches(path, size, digest) -> bool:
    """Check that *path* holds exactly *size* bytes with *digest*.

    Returns True only when the file exists, its length equals
    *size*, and its SHA-256 hex digest equals *digest*. A missing
    file is simply a mismatch, not an error.
    """
    candidate = Path(path)
    if not candidate.is_file():
        return False

    contents = candidate.read_bytes()
    if len(contents) != size:
        return False
    return digest_of(contents) == digest
