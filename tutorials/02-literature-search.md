# Tutorial — Literature & Web Search (9 skills)

This category covers finding papers, extracting structured experimental data, running systematic reviews, managing citations, and searching the web for scholarly content. Chain several of them for a full literature workflow.

---

## 1. `paper-lookup`

**What it does.** Searches **10 academic databases** (PubMed, PMC full text, bioRxiv, medRxiv, arXiv, OpenAlex, Crossref, Semantic Scholar, CORE, Unpaywall) via REST APIs for papers, preprints, and scholarly articles.

**Use it when** you need to find papers, look up a DOI/PMID, retrieve abstracts or full text, check open access, search an author, or query citation graphs.

**Example scenario.** A bioinformatics student wants recent studies on a gene:
> "Find papers on **p53's role in cell-cycle regulation** via **PubMed** and **bioRxiv** using **paper-lookup**, and return the top 10 recent abstracts with their DOIs and open-access status."

---

## 2. `bgpt-paper-search`

**What it does.** Searches scientific papers and extracts **structured experimental data** (25+ fields per paper — methods, results, sample sizes, quality scores, conclusions) from full text via the BGPT MCP server.

**Use it when** you need experimental details that aren't in an abstract — e.g. sample sizes, assay conditions, or numerical results — for evidence synthesis or a systematic review.

**Example scenario.** A clinician meta-analyzing trial outcomes wants precise numbers from each study:
> "Use **bgpt-paper-search** on these trial papers and extract the **sample size, primary endpoint values, and quality score** for each, so I can build a comparison table."

---

## 3. `literature-review`

**What it does.** Conducts comprehensive, systematic literature reviews across multiple databases (PubMed, arXiv, bioRxiv, Semantic Scholar, etc.), producing formatted Markdown/PDF with verified citations in styles like APA, Nature, and Vancouver.

**Use it when** you need a systematic review, meta-analysis, research synthesis, or a comprehensive literature search.

**Example scenario.** A PhD candidate preparing a dissertation chapter needs a structured review:
> "Run a **systematic literature review** on **CRISPR base editing safety** across PubMed and bioRxiv, and produce a formatted Markdown document with an APA citation list."

---

## 4. `citation-management`

**What it does.** Comprehensive citation management — searches Google Scholar and PubMed, validates citations, converts DOIs to BibTeX, and ensures reference accuracy in scientific writing.

**Use it when** you need to find papers, verify citation info, convert a DOI to BibTeX, or clean up references in a manuscript.

**Example scenario.** An author finalizing a paper wants accurate references:
> "Verify the citations in my manuscript bibliography against Google Scholar and PubMed, convert any DOI to proper **BibTeX**, and flag any that are outdated or incorrectly formatted."

---

## 5. `pyzotero`

**What it does.** Programmatic access to Zotero libraries via the **Zotero Web API v3** using the pyzotero client — retrieve, create, update, and delete items, collections, tags, and attachments.

**Use it when** you need to manage a Zotero library programmatically, export citations, upload PDF attachments, or build automation that integrates with Zotero.

**Example scenario.** A researcher wants to automate their reference library:
> "Sync my Zotero collection with my manuscript's reference list — fetch items for each cited paper, verify tags, and upload the PDF attachments I'm missing."

---

## 6. `paperzilla`

**What it does.** Chat with your agent about **projects, recommendations, and canonical papers** in Paperzilla — project recommendations, canonical paper details, markdown summaries, recommendation feedback, feed export, and Atom feed URLs.

**Use it when** you want recent project recommendations, canonical paper details, or a feed export.

**Example scenario.** A scientist exploring a field wants a curated starting point:
> "Use **paperzilla** to recommend recent projects and canonical papers in **single-cell genomics**, and give me a markdown summary plus an Atom feed URL for updates."

---

## 7. `exa-search`

**What it does.** A web toolkit powered by **Exa**, tuned for scientific and technical content — semantic web search (with optional research-paper category and academic domain filtering) and URL extraction (fetching pages, articles, academic PDFs in batch).

**Use it when** you need high-quality web search or scholarly filtering, or to extract content from URLs/PDFs.

**Example scenario.** A reviewer wants to check a claim against the latest technical literature:
> "Use **exa-search** with `category=research paper` to find recent articles on **quantum error correction**, then fetch and extract the key PDFs."

---

## 8. `parallel-web`

**What it does.** All-in-one web toolkit powered by **parallel-cli** — web search, URL extraction, bulk data enrichment (adding fields to CSV/lists from the web), and deep research reports, with a strong emphasis on academic and scientific sources.

**Use it when** you need ANY web-related task — lookups, page fetching, dataset enrichment, topic investigation, citation checks, or reviewing scientific literature — even if you don't mention "parallel" or "web" explicitly.

**Example scenario.** A data analyst enriching a bibliography list:
> "Use **parallel-web** to enrich this CSV of conference papers — add each paper's DOI, publication year, and citation count from the web."

---

## 9. `research-lookup`

**What it does.** Routes current-research lookups across **parallel-cli** (fast web search), the **Parallel Chat API** (deep research), and **Perplexity sonar-pro-search** (academic paper searches), auto-selecting the best backend.

**Use it when** you need to find papers, gather research data, or verify scientific information — especially when you want the query routed to the best search backend automatically.

**Example scenario.** A grant writer wants the latest evidence to support a claim:
> "Use **research-lookup** to find the most recent peer-reviewed evidence on **brain-computer interface safety** for my grant narrative, and note which backend it chose."

---