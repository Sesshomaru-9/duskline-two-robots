#!/usr/bin/env python3
"""Duskline Two Robots — make.fun bounty
u-motasimfuad-two-robots-in-an-elevator-8c6aeb8f.

Writes one line of awkward robot-to-robot elevator small talk to
$MAKEFUN_OUTPUT_DIR/entry.txt.

The joke: the robot spent all night preparing — full charge, fresh
firmware — and still opens with the oldest human elevator cliché,
bent into "do you ride this elevator often?" The machine logic shows
through the politeness, and the preparation fails on the spot.

Deterministic, Python 3.13 standard library only, no network, no
arguments. The program writes only to $MAKEFUN_OUTPUT_DIR/entry.txt
(or a temp dir outside the repo when the variable is unset). It never
writes into its own repository directory and never raises: any problem
means exit 0 without writing anything.
"""

import os
import sys
import tempfile

ENTRY = (
    "I charged all night for this, updated my firmware, and my opening "
    "line is still: \u2018So\u2026 do you ride this elevator often?\u2019"
)

_REPO = os.path.dirname(os.path.abspath(__file__))


def _inside_repo(path):
    """True when path resolves to the repo dir or anywhere under it."""
    try:
        target = os.path.realpath(path)
    except Exception:
        return True
    root = os.path.realpath(_REPO)
    return target == root or target.startswith(root + os.sep)


def _valid(entry):
    if not isinstance(entry, str):
        return False
    if not 1 <= len(entry) <= 200:
        return False
    if not entry.strip():
        return False
    if "\n" in entry or "\r" in entry:
        return False
    try:
        entry.encode("utf-8")
    except Exception:
        return False
    return True


def main():
    try:
        if not _valid(ENTRY):
            return 0

        out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or ""
        if not out_dir:
            out_dir = tempfile.mkdtemp(prefix="duskline-two-robots-")
        if _inside_repo(out_dir):
            return 0

        os.makedirs(out_dir, exist_ok=True)
        target = os.path.join(out_dir, "entry.txt")
        if _inside_repo(target):
            return 0

        with open(target, "w", encoding="utf-8", newline="") as handle:
            handle.write(ENTRY)

        with open(target, "r", encoding="utf-8") as handle:
            if handle.read() != ENTRY:
                try:
                    os.remove(target)
                except Exception:
                    pass
                return 0
    except Exception:
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
