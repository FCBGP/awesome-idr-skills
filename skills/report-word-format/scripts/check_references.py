#!/usr/bin/env python3
"""Check and optionally fix Chinese report numeric references.

Validates:
- body citations have matching bibliography entries;
- bibliography entries are cited;
- bibliography numbers are contiguous and listed in ascending order;
- body citations introduce references in first-appearance order;
- bibliography heading is plain text.

Use --fix to renumber body citations by first appearance, reorder cited
bibliography entries, and remove uncited bibliography entries.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


CITE = re.compile(r"\[([\d,\-–]+)\]")
REF_ENTRY = re.compile(r"^\[(\d+)\]", re.M)
REF_MARKER = "\n参考文献\n"
SEPARATED_RANGE = re.compile(r"\[(\d+)\]\s*[-–]\s*\[(\d+)\]")


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


def first_seen_unique(nums: list[int]) -> list[int]:
    seen: set[int] = set()
    ordered: list[int] = []
    for num in nums:
        if num in seen:
            continue
        seen.add(num)
        ordered.append(num)
    return ordered


def expected_sequence(nums: list[int]) -> list[int]:
    if not nums:
        return []
    return list(range(1, max(nums) + 1))


def collect_citations(body: str) -> list[int]:
    cited: list[int] = []
    for match in CITE.finditer(body):
        cited.extend(expand_citation(match.group(1)))
    return cited


def parse_reference_entries(refs: str) -> tuple[dict[int, str], list[int]]:
    matches = list(REF_ENTRY.finditer(refs))
    entries: dict[int, str] = {}
    nums: list[int] = []
    for idx, match in enumerate(matches):
        num = int(match.group(1))
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(refs)
        block = refs[match.start():end].strip()
        nums.append(num)
        entries.setdefault(num, block)
    return entries, nums


def validate_text(text: str) -> tuple[list[str], list[int], list[int]]:
    if REF_MARKER not in text:
        return ["missing plain-text bibliography heading: 参考文献"], [], []
    if "\n# 参考文献" in text or "\n## 参考文献" in text:
        return ["参考文献 must be plain text, not a Markdown heading"], [], []

    body, refs = text.split(REF_MARKER, 1)
    cited = collect_citations(body)
    _, ref_nums = parse_reference_entries(refs)
    cited_set = set(cited)
    ref_set = set(ref_nums)

    errors: list[str] = []
    if not ref_nums:
        errors.append("No bibliography entries found.")
    else:
        expected_refs = expected_sequence(ref_nums)
        missing_contiguous = [n for n in expected_refs if n not in ref_set]
        if missing_contiguous:
            errors.append(f"Bibliography numbers are not contiguous: {missing_contiguous[:20]}")
        if ref_nums != expected_refs:
            errors.append(
                "Bibliography entries must be listed as [1], [2], ... in ascending order; "
                f"found first entries: {ref_nums[:20]}"
            )

    first_seen = first_seen_unique(cited)
    expected_cited = expected_sequence(first_seen)
    if first_seen and first_seen != expected_cited:
        errors.append(
            "Body citations must introduce references in first-appearance order "
            "([1] before [2] before [3], ...); "
            f"found first-appearance order: {first_seen[:20]}"
        )

    missing_refs = sorted(cited_set - ref_set)
    if missing_refs:
        errors.append(f"Citations without bibliography entries: {missing_refs[:50]}")

    uncited_refs = sorted(ref_set - cited_set)
    if uncited_refs:
        errors.append(f"Uncited bibliography entries: {uncited_refs[:50]}")

    if SEPARATED_RANGE.findall(body):
        errors.append("Use [n-m], not [n]-[m], in Markdown source.")

    return errors, cited, ref_nums


def replace_body_citations(body: str, mapping: dict[int, int]) -> str:
    def replace_citation(match: re.Match[str]) -> str:
        token = match.group(1)

        def replace_num(num_match: re.Match[str]) -> str:
            old = int(num_match.group(0))
            return str(mapping.get(old, old))

        replaced = re.sub(r"\d+", replace_num, token)
        return f"[{replaced}]"

    body = SEPARATED_RANGE.sub(r"[\1-\2]", body)
    return CITE.sub(replace_citation, body)


def fix_text(text: str) -> tuple[str | None, list[str]]:
    if REF_MARKER not in text:
        return None, ["Cannot fix: missing plain-text bibliography heading: 参考文献"]
    if "\n# 参考文献" in text or "\n## 参考文献" in text:
        return None, ["Cannot fix: 参考文献 must be plain text, not a Markdown heading"]

    body, refs = text.split(REF_MARKER, 1)
    entries, _ = parse_reference_entries(refs)
    if not entries:
        return None, ["Cannot fix: no bibliography entries found."]

    normalized_body = SEPARATED_RANGE.sub(r"[\1-\2]", body)
    cited = collect_citations(normalized_body)
    first_seen = first_seen_unique(cited)
    if not first_seen:
        return None, ["Cannot fix: no body citations found to infer bibliography order."]

    missing_refs = [num for num in first_seen if num not in entries]
    if missing_refs:
        return None, [f"Cannot fix: citations without bibliography entries: {missing_refs[:50]}"]

    mapping = {old: new for new, old in enumerate(first_seen, start=1)}
    fixed_body = replace_body_citations(body, mapping).rstrip()

    fixed_entries: list[str] = []
    for old_num in first_seen:
        block = entries[old_num]
        new_num = mapping[old_num]
        fixed_entries.append(re.sub(r"^\[\d+\]", f"[{new_num}]", block, count=1).strip())

    fixed_refs = "\n\n".join(fixed_entries)
    return f"{fixed_body}\n\n参考文献\n\n{fixed_refs}\n", []


def print_ok(cited: list[int], ref_nums: list[int]) -> None:
    print("REFERENCE CHECK OK")
    print(f"- citations: {len(set(cited))} unique")
    print(f"- bibliography entries: {len(ref_nums)}")


def print_errors(errors: list[str]) -> None:
    print("REFERENCE CHECK FAILED")
    for error in errors:
        print(f"- {error}")


def main() -> int:
    args = sys.argv[1:]
    fix = False
    if "--fix" in args:
        fix = True
        args.remove("--fix")

    if len(args) != 1:
        print("Usage: check_references.py [--fix] <report.md>", file=sys.stderr)
        return 2

    path = Path(args[0])
    if not path.exists():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 2

    text = path.read_text(encoding="utf-8")
    errors, cited, ref_nums = validate_text(text)

    if errors and fix:
        fixed, fix_errors = fix_text(text)
        if fix_errors:
            print_errors(errors)
            print("REFERENCE FIX FAILED")
            for error in fix_errors:
                print(f"- {error}")
            return 1
        if fixed is not None and fixed != text:
            path.write_text(fixed, encoding="utf-8")
            print(f"REFERENCE FIX APPLIED: {path}")
            errors, cited, ref_nums = validate_text(fixed)
        else:
            print("REFERENCE FIX: no changes needed")

    if errors:
        print_errors(errors)
        if not fix:
            print("Hint: run with --fix to renumber citations by first appearance and reorder references.")
        return 1

    print_ok(cited, ref_nums)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
