#!/usr/bin/env python3
"""Check Chinese research report numeric references.

Validates:
- body citations have matching bibliography entries;
- bibliography entries are cited;
- bibliography numbers are contiguous;
- bibliography heading is plain text.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


CITE = re.compile(r"\[([\d,\-–]+)\]")
REF_ENTRY = re.compile(r"^\[(\d+)\]", re.M)


def expand_citation(text: str) -> list[int]:
    nums: list[int] = []
    for part in text.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part or "–" in part:
            bits = re.split(r"[-–]", part)
            if len(bits) == 2 and bits[0].isdigit() and bits[1].isdigit():
                a, b = int(bits[0]), int(bits[1])
                step = 1 if b >= a else -1
                nums.extend(range(a, b + step, step))
                continue
        if part.isdigit():
            nums.append(int(part))
    return nums


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: check_references.py <report.md>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 2

    text = path.read_text(encoding="utf-8")
    marker = "\n参考文献\n"
    if marker not in text:
        print("ERROR: missing plain-text bibliography heading: 参考文献")
        return 1
    if "\n# 参考文献" in text or "\n## 参考文献" in text:
        print("ERROR: 参考文献 must be plain text, not a Markdown heading")
        return 1

    body, refs = text.split(marker, 1)
    cited: list[int] = []
    for match in CITE.finditer(body):
        cited.extend(expand_citation(match.group(1)))

    ref_nums = [int(match.group(1)) for match in REF_ENTRY.finditer(refs)]
    cited_set = set(cited)
    ref_set = set(ref_nums)

    errors: list[str] = []
    if not ref_nums:
        errors.append("No bibliography entries found.")
    else:
        missing_contiguous = [n for n in range(1, max(ref_nums) + 1) if n not in ref_set]
        if missing_contiguous:
            errors.append(f"Bibliography numbers are not contiguous: {missing_contiguous[:20]}")

    missing_refs = sorted(cited_set - ref_set)
    if missing_refs:
        errors.append(f"Citations without bibliography entries: {missing_refs[:50]}")

    uncited_refs = sorted(ref_set - cited_set)
    if uncited_refs:
        errors.append(f"Uncited bibliography entries: {uncited_refs[:50]}")

    separated_ranges = re.findall(r"\[\d+\]\s*[-–]\s*\[\d+\]", body)
    if separated_ranges:
        errors.append("Use [n-m], not [n]-[m], in Markdown source.")

    if errors:
        print("REFERENCE CHECK FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("REFERENCE CHECK OK")
    print(f"- citations: {len(cited_set)} unique")
    print(f"- bibliography entries: {len(ref_nums)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
