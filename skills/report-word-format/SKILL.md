---
name: research-report-word
description: Generate Chinese research report Markdown and Word documents with fixed headings, figure/table captions, bibliography numbering, cross-references, three-line tables, and body-font inline code. Use when writing 调研报告, editing Markdown report sections, merging new content, fixing references, or converting Markdown to Word.
---

# Research Report Word

## Use This Skill When

- Writing or revising Chinese `调研报告` Markdown.
- Merging new section content into an existing report.
- Converting Markdown to Word with the project format.
- Fixing heading levels, figure/table numbering, references, captions, tables, or inline code fonts.

## Required Workflow

1. Read `WRITING_SPEC.md` before editing report content.
2. Read `REFERENCE_RULES.md` before adding, deleting, or moving citations.
3. Edit Markdown only. Do not directly edit generated `.docx` body text.
4. Keep images in a `media/` folder next to the report Markdown.
5. Validate references before export:

```bash
python3 scripts/check_references.py path/to/report.md
```

6. Generate Word:

```bash
scripts/build_docx.sh path/to/report.md
```

7. Tell the user to open Word and run `Ctrl+A -> F9` to update fields.

## Non-Negotiable Rules

- Markdown is the only content source.
- `参考文献` is plain text, not `# 参考文献`.
- Every bibliography entry is separated by a blank line.
- References are ordered by first appearance in body text.
- Only cited bibliography entries remain in the final document.
- Figure captions use `图 3-2-X-Y 标题`; table captions use `表 3-2-X-Y 标题`.
- Images use empty alt text: `![](media/xxx.png)`.
- Figure captions go below images; table captions go above tables.
- Markdown tables are plain tables; Word three-line formatting is handled by `postprocess_docx.py`.
- Inline code/API paths may use backticks in Markdown; Word output restores them to body font.

## Supporting Files

- `WRITING_SPEC.md`: Markdown structure, section style, figure/table rules.
- `REFERENCE_RULES.md`: citation and bibliography rules.
- `WORD_FORMAT_SPEC.md`: Word formatting and postprocess behavior.
- `examples.md`: common editing and export examples.
- `scripts/build_docx.sh`: one-command Markdown to Word export.
- `scripts/prepare_reference_docx.py`: generates Pandoc reference docx.
- `scripts/postprocess_docx.py`: fixes Word features after Pandoc.
