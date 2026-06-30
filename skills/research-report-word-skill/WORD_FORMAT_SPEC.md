# Word Format Spec

## Build Pipeline

```text
Markdown source
  -> prepare_reference_docx.py
  -> pandoc
  -> postprocess_docx.py
  -> final Word docx
```

`crop_media_images.py` is intentionally not part of this skill.

## Page and Body

- Page size: A4.
- Body font: 宋体 小四 12pt.
- Body alignment: justified.
- Body first-line indent: 1.77 characters.
- Body line spacing: 1.5.
- Paragraph before/after: 0.
- Document grid is patched so 1.5 line spacing looks vertically balanced.

## Title and Headings

| Markdown | Word Style | Format |
|---|---|---|
| first line report title | Title | 黑体 22pt, centered |
| `#` | Heading 1 | 黑体 14pt, black, not bold, no indent |
| `##` | Heading 2 | 黑体 14pt, black, not bold, no indent |
| `###` | Heading 3 | 黑体 14pt, black, not bold, no indent |
| `####` | Heading 4 | 黑体 12pt, black, not bold, not italic, no indent |

All headings use:

- 6pt before;
- 6pt after;
- single line spacing;
- justified alignment.

## Figures and Tables

`postprocess_docx.py` detects figure/table captions and applies:

- centered;
- 黑体 五号 10.5pt;
- no indent;
- single line spacing.

Image paragraphs are centered and no-indent.

Tables are converted to:

- centered table;
- three-line table;
- no vertical borders;
- no extra inside horizontal borders except header bottom;
- cells use 五号, centered horizontally and vertically;
- cell paragraphs have no indent and single line spacing.

## Inline Code

Pandoc normally renders backtick text in an equal-width code font. `postprocess_docx.py` normalizes inline code runs:

- removes `Code` / `VerbatimChar` styling;
- removes Consolas/Courier/Menlo style fonts;
- sets 宋体 小四 12pt.

This applies to API addresses, fields, command parameters, and similar inline code in body text.

## Bibliography

Bibliography entries use:

- 宋体 五号 10.5pt;
- justified alignment;
- hanging indent 0.78 cm;
- 1.5 line spacing;
- paragraph before/after 0;
- no grid snapping.

`postprocess_docx.py` converts manual `[n]` prefixes into Word-native automatic numbering and cross-reference bookmarks.

## Script Responsibilities

`prepare_reference_docx.py`:

- generates `调研报告-reference.docx`;
- patches base Word styles;
- sets heading/body/bibliography fonts and spacing;
- sets page size and margins.

`postprocess_docx.py`:

- applies title style;
- fixes merged bibliography blocks;
- converts bibliography entries to Word numbering;
- converts body citations to cross-reference fields;
- formats figure/table captions;
- centers images;
- formats tables as centered three-line tables;
- normalizes inline code font;
- disables widow control;
- injects document grid;
- patches numbering definitions.
