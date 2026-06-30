# Codex Instructions

This project generates unified-format Chinese research report Word documents from Markdown.

## First Step

Read:

- `SKILL.md`
- `WRITING_SPEC.md`
- `REFERENCE_RULES.md`
- `WORD_FORMAT_SPEC.md`

## Edit Rules

- Edit `.md` source files only.
- Preserve Chinese report tone: factual survey, not implementation proposal.
- Use `#`, `##`, `###`, `####` for heading levels exactly as specified.
- Use `图 3-2-X-Y 标题` and `表 3-2-X-Y 标题`.
- Use empty image alt text: `![](media/xxx.png)`.
- Keep `参考文献` as plain text, not a Markdown heading.
- Keep blank lines between bibliography entries.

## Build Commands

```bash
python3 scripts/check_references.py /path/to/report.md
scripts/build_docx.sh /path/to/report.md
```

If `pandoc` is missing, ask the user to install it.

## Expected Output

The default Word output is:

```text
/path/to/output/<report-name>-导出.docx
```

After generation, remind the user:

```text
Open Word, press Ctrl+A, then F9 to update fields.
```
