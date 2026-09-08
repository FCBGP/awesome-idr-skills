# Tutorial — Documents (8 skills)

This category covers working with office document formats — PDFs, Word, PowerPoint, Excel, Markdown conversion, local parsing, and Chinese research-report Word generation. Use these when files are the input or output of a task.

---

## 1. `pdf`

**What it does.** Read, create, merge/split, OCR, fill forms, and manipulate **PDF files** — extracting text/tables, combining PDFs, splitting, rotating, watermarking, encrypting/decrypting, extracting images, and OCR on scans.

**Use it when** you need to do anything with a `.pdf` file — read it, merge/split it, fill a form, or make a scanned PDF searchable.

**Example scenario.** An analyst needs to consolidate several reports:
> "Merge these **10 quarterly PDF reports** into one, split out the appendix pages, and OCR the scanned ones so they're searchable."

---

## 2. `docx`

**What it does.** Create, read, and edit **Word documents** (.docx) with rich formatting — tables of contents, headings, page numbers, letterheads, images, find-and-replace, tracked changes, and comments.

**Use it when** you need a Word deliverable — a report, memo, letter, template, or any formatted `.docx` document.

**Example scenario.** A consultant needs a polished client memo:
> "Use **docx** to create a formatted **client memorandum** with a table of contents, headings, and page numbers from my draft outline."

---

## 3. `pptx`

**What it does.** Create, read, and edit **PowerPoint presentations** — slide decks, pitch decks, reading/parsing `.pptx` text, editing/updating slides, combining/splitting, working with templates, layouts, speaker notes, and comments.

**Use it when** any `.pptx` file is involved — as input, output, or both — or you need to make or modify a slide deck.

**Example scenario.** A program manager wants to update a quarterly deck:
> "Use **pptx** to edit my quarterly review deck — update the revenue slide, split the appendix into a separate deck, and add speaker notes."

---

## 4. `xlsx`

**What it does.** Create, edit, analyze, or convert **Excel spreadsheets** (.xlsx/.xlsm) where the workbook is the primary deliverable — formulas, formatting, financial models, multi-sheet workbooks, and tabular cleanup. Also applies to `.csv`/`.tsv` when spreadsheet output is wanted.

**Use it when** the deliverable is an Excel workbook, or you need a CSV cleaned into spreadsheet form.

**Example scenario.** A finance team wants a model built from raw data:
> "Use **xlsx** to build a **multi-sheet financial model** from this raw revenue data — one sheet for inputs, one for calculations, one for the executive summary, with formulas."

---

## 5. `markitdown`

**What it does.** Converts files and office documents to **Markdown** — PDF, DOCX, PPTX, XLSX, images (OCR), audio (transcription), HTML, CSV, JSON, XML, ZIP, YouTube URLs, EPubs, and more.

**Use it when** you need content from a document converted into Markdown for use by an agent or in a RAG pipeline.

**Example scenario.** A knowledge-base builder wants to ingest documents:
> "Convert this **PPTX** and **DOCX** into Markdown via **markitdown** so I can feed them into my RAG pipeline for retrieval."

---

## 6. `liteparse`

**What it does.** Local document and PDF parsing with **spatial text and bounding boxes** — extract text from PDFs/DOCX/Office files/images, OCR on scans, layout-preserved JSON for RAG, batch-ingesting paper folders, or page screenshots for multimodal agents. All processing is local (no cloud API).

**Use it when** you need bounding boxes, fast local parsing, PNG page renders, or layout-preserved JSON — prefer it over MarkItDown for these cases, and over the `pdf` skill for merge/split/forms.

**Example scenario.** A multimodal agent workflow wants page-level structure:
> "Use **liteparse** to parse this paper folder — OCR the scans, return **layout-preserved JSON with bounding boxes** for each page, and render page PNGs."

---

## 7. `report-word-format`

**What it does.** Generates **Chinese research report** (调研报告) Markdown and Word documents with fixed headings, figure/table captions, bibliography numbering, cross-references, three-line tables, and body-font inline code.

**Use it when** you're writing or revising a Chinese `调研报告` Markdown, merging new content, fixing references, or converting Markdown to Word in the project's fixed format.

**Example scenario.** A research assistant needs a standardized Chinese report:
> "Use **report-word-format** to write my Chinese 调研报告 in the fixed heading/numbering/caption format, then convert it to a Word document."

---

## 8. `research-report-word-skill`

**What it does.** The same Chinese research-report (调研报告) generation and Markdown-to-Word conversion as `report-word-format`, with the fixed formatting spec (WRITING_SPEC and REFERENCE_RULES).

**Use it when** you're producing a Chinese research report Word document and want the standardized structure — headings, captions, bibliography numbering, three-line tables, and inline-code fonts.

**Example scenario.** A student wants a thesis-style 调研报告 Word file:
> "Use **research-report-word-skill** to convert my research report Markdown into a **Word document** with the correct heading levels, numbered bibliography, and three-line tables."

> 💡 **Note:** `report-word-format` and `research-report-word-skill` are near-duplicates (same `research-report-word` skill name). Prefer one consistently; if both exist, `research-report-word-skill` adds `WRITING_SPEC.md`.

---