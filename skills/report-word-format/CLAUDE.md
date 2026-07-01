# Claude Code Instructions

Use this folder as the source of truth when working on Chinese research report Markdown and Word generation.

## Required Reading

Before editing content:

1. Read `SKILL.md`.
2. Read `WRITING_SPEC.md`.
3. If citations or bibliography are involved, read `REFERENCE_RULES.md`.
4. If Word output or formatting is involved, read `WORD_FORMAT_SPEC.md`.

## Workflow

1. Edit Markdown only.
2. Keep report images in `media/` next to the Markdown file.
3. Check references:

```bash
python3 scripts/check_references.py /path/to/report.md
```

4. Build Word:

```bash
scripts/build_docx.sh /path/to/report.md
```

5. Tell the user to open Word and run `Ctrl+A -> F9`.

## Constraints

- Do not directly edit `.docx` body content.
- Do not use `--number-sections`.
- Do not use `--toc` unless explicitly requested.
- Do not use image alt text as captions.
- Do not keep uncited bibliography entries.
- Do not renumber references manually in only one place; body and bibliography must be consistent.
