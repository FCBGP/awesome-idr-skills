# Research Report Word Skill

This folder is a portable skill/workflow for generating unified-format Chinese research report Word documents from Markdown.

It is designed for Cursor, Claude Code, Codex, or other coding agents.

## What It Does

The workflow converts a Markdown report into a Word document with:

- fixed heading styles;
- body text font and line spacing;
- figure/table captions;
- centered three-line tables;
- Word-native bibliography numbering;
- clickable cross-references from body citations to bibliography;
- inline code/API text restored to body font.

## Folder Layout

```text
research-report-word-skill/
├── SKILL.md
├── README.md
├── CLAUDE.md
├── CODEX.md
├── WRITING_SPEC.md
├── WORD_FORMAT_SPEC.md
├── REFERENCE_RULES.md
├── examples.md
└── scripts/
    ├── build_docx.sh
    ├── check_references.py
    ├── prepare_reference_docx.py
    └── postprocess_docx.py
```

## Dependencies

- `python3`
- `pandoc`

On macOS:

```bash
brew install pandoc
```

## Quick Start

Put the report Markdown and `media/` folder in the same working directory, then run:

```bash
cd research-report-word-skill
python3 scripts/check_references.py /path/to/report.md
scripts/build_docx.sh /path/to/report.md
```

Default output:

```text
/path/to/output/report-导出.docx
```

After opening Word, run `Ctrl+A -> F9` to update bibliography fields and cross-references.

## Agent Instructions

For Claude Code, read `CLAUDE.md`.

For Codex, read `CODEX.md`.

For Cursor Agent Skills, read `SKILL.md`.
