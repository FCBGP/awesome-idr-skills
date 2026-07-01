# Reference Rules

## Citation Style

Use numeric square-bracket citations:

```markdown
PBFT[16]、HotStuff[18]、分片机制[10,31-33]。
```

Rules:

- Single source: `[n]`
- Continuous range: `[n-m]`
- Mixed sources: `[n,m,p-q]`
- Punctuation comes after the citation: `……不足[32]。`
- Do not use author-year style.
- Do not use HTML superscript.

## Numbering Order

References must be numbered by first appearance in body text.

When adding or moving content:

1. Scan all body citations in order.
2. Assign the first seen source the next number.
3. Reuse the same number for repeated citations.
4. Delete bibliography entries that are not cited.
5. Ensure no missing numbers or jumps.

Before export, run:

```bash
python3 scripts/check_references.py /path/to/report.md
```

## Bibliography Block

The bibliography heading is plain text:

```markdown
参考文献

[1] Castro M, Liskov B. Practical byzantine fault tolerance[C]//Proc. of OSDI. USENIX, 1999: 173-186.

[2] Yin M, Malkhi D, Reiter M K, et al. HotStuff: BFT consensus with linearity and responsiveness[C]//Proc. of PODC. ACM, 2019: 347-356.
```

Rules:

- Do not write `# 参考文献`.
- Leave a blank line before `参考文献`.
- Leave a blank line after `参考文献`.
- Leave a blank line between every bibliography entry.
- Start each entry with `[n]`.
- Do not use Markdown ordered lists like `1.`.

## Entry Format

General:

```text
[n] 作者. 题名[文献类型标识]. 出处/出版项, 年: 页码或编号.
```

Common types:

- `[J]` journal article
- `[C]` conference paper
- `[R]` report/RFC/technical report
- `[D]` thesis
- `[EB/OL]` online resource

Conference examples:

```markdown
[16] Castro M, Liskov B. Practical byzantine fault tolerance[C]//Proc. of OSDI. USENIX, 1999: 173-186.
[18] Yin M, Malkhi D, Reiter M K, et al. HotStuff: BFT consensus with linearity and responsiveness[C]//Proc. of PODC. ACM, 2019: 347-356.
```

Use `Proc. of ...`, not `Proceedings of ...`.

## Word Output Behavior

`postprocess_docx.py` converts Markdown references into Word-native features:

- bibliography entries become an automatic numbered list;
- each entry receives a bookmark like `ref16`;
- body citations become Word `REF` fields;
- citations are clickable and can update after renumbering.

After opening Word, update fields:

```text
Ctrl+A -> F9
```

On macOS, use `fn+F9` if needed.
