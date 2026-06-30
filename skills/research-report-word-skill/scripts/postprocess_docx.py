#!/usr/bin/env python3
"""导出后微调 Word：封面标题、参考文献悬挂缩进等，与 调研报告模版.docx 一致。"""

from __future__ import annotations

import copy
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
XML = "http://www.w3.org/XML/1998/namespace"
NS = {"w": W}
REF_ENTRY = re.compile(r"^\[\d+\]")
REF_SPLIT = re.compile(r"(?=\[\d+\])")
# 图名/表名：以「图3-1」「表3-1」等开头的独立段落
CAPTION = re.compile(r"^[图表]\s*\d+\s*[-－—–]\s*\d+")
# 正文引用标记：[7]、[7-8]、[7-8,11] 等纯数字/逗号/连字符
CITE = re.compile(r"\[([\d,\-–]+)\]")
BOOKMARK_ID_BASE = 900000
# 参考文献自动编号列表（原生编号列表，格式 [1][2][3]）
REF_ABSTRACT_ID = 995
REF_NUM_ID = 1100
# 显式清零缩进（覆盖 BodyText/Normal 的首行缩进继承）
NO_IND = {
    "left": "0",
    "leftChars": "0",
    "firstLine": "0",
    "firstLineChars": "0",
    "right": "0",
    "rightChars": "0",
}


def qn(tag: str) -> str:
    prefix, local = tag.split(":")
    return f"{{{NS[prefix]}}}{local}"


def paragraph_text(p: ET.Element) -> str:
    return "".join(t.text or "" for t in p.iter(qn("w:t"))).strip()


def make_text_paragraph(text: str, style_id: str | None = None) -> ET.Element:
    p = ET.Element(qn("w:p"))
    if style_id:
        ppr = ET.SubElement(p, qn("w:pPr"))
        pstyle = ET.SubElement(ppr, qn("w:pStyle"))
        pstyle.set(qn("w:val"), style_id)
    r = ET.SubElement(p, qn("w:r"))
    t = ET.SubElement(r, qn("w:t"))
    t.text = text
    if text.startswith(" ") or text.endswith(" "):
        t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    return p


def ensure_ppr(p: ET.Element) -> ET.Element:
    ppr = p.find("w:pPr", NS)
    if ppr is None:
        ppr = ET.SubElement(p, qn("w:pPr"))
    return ppr


def set_style(p: ET.Element, style_id: str) -> None:
    ppr = ensure_ppr(p)
    pstyle = ppr.find("w:pStyle", NS)
    if pstyle is None:
        pstyle = ET.SubElement(ppr, qn("w:pStyle"))
    pstyle.set(qn("w:val"), style_id)


def apply_title_style(p: ET.Element) -> None:
    set_style(p, "Title")
    ppr = ensure_ppr(p)
    ind = ppr.find("w:ind", NS)
    if ind is not None:
        ppr.remove(ind)

    jc = ppr.find("w:jc", NS)
    if jc is None:
        jc = ET.SubElement(ppr, qn("w:jc"))
    jc.set(qn("w:val"), "center")

    spacing = ppr.find("w:spacing", NS)
    if spacing is None:
        spacing = ET.SubElement(ppr, qn("w:spacing"))
    spacing.set(qn("w:line"), "360")
    spacing.set(qn("w:lineRule"), "auto")

    for r in p.findall("w:r", NS):
        rpr = r.find("w:rPr", NS)
        if rpr is None:
            rpr = ET.SubElement(r, qn("w:rPr"))
        else:
            for tag in ("rFonts", "sz", "szCs", "color", "b"):
                el = rpr.find(f"w:{tag}", NS)
                if el is not None:
                    rpr.remove(el)
        fonts = ET.SubElement(rpr, qn("w:rFonts"))
        fonts.set(qn("w:ascii"), "黑体")
        fonts.set(qn("w:eastAsia"), "黑体")
        fonts.set(qn("w:hAnsi"), "黑体")
        sz = ET.SubElement(rpr, qn("w:sz"))
        sz.set(qn("w:val"), "44")
        sz_cs = ET.SubElement(rpr, qn("w:szCs"))
        sz_cs.set(qn("w:val"), "44")
        ET.SubElement(rpr, qn("w:b"))


def apply_reference_heading_style(p: ET.Element) -> None:
    set_style(p, "BodyText")
    ppr = ensure_ppr(p)
    ind = ppr.find("w:ind", NS)
    if ind is not None:
        ppr.remove(ind)
    spacing = ppr.find("w:spacing", NS)
    if spacing is None:
        spacing = ET.SubElement(ppr, qn("w:spacing"))
    spacing.set(qn("w:before"), "0")
    spacing.set(qn("w:after"), "0")
    spacing.set(qn("w:line"), "360")
    spacing.set(qn("w:lineRule"), "auto")
    jc = ppr.find("w:jc", NS)
    if jc is None:
        jc = ET.SubElement(ppr, qn("w:jc"))
    jc.set(qn("w:val"), "both")


def apply_bibliography_style(p: ET.Element) -> None:
    set_style(p, "Bibliography")


def apply_no_indent(p: ET.Element, *, center: bool = False) -> None:
    """显式清零段落缩进，避免继承 BodyText 的首行 1.77 字符。"""
    ppr = ensure_ppr(p)
    ind = ppr.find("w:ind", NS)
    if ind is None:
        ind = ET.SubElement(ppr, qn("w:ind"))
    for key, val in NO_IND.items():
        ind.set(qn(f"w:{key}"), val)
    if center:
        jc = ppr.find("w:jc", NS)
        if jc is None:
            jc = ET.SubElement(ppr, qn("w:jc"))
        jc.set(qn("w:val"), "center")


def paragraph_has_image(p: ET.Element) -> bool:
    return p.find(".//w:drawing", NS) is not None or p.find(".//w:pict", NS) is not None


def apply_image_paragraph_style(p: ET.Element) -> None:
    """图片段落：居中、无缩进。"""
    ppr = ensure_ppr(p)
    pstyle = ppr.find("w:pStyle", NS)
    if pstyle is not None:
        ppr.remove(pstyle)
    apply_no_indent(p, center=True)
    spacing = ppr.find("w:spacing", NS)
    if spacing is None:
        spacing = ET.SubElement(ppr, qn("w:spacing"))
    spacing.set(qn("w:before"), "0")
    spacing.set(qn("w:after"), "0")
    spacing.set(qn("w:line"), "240")
    spacing.set(qn("w:lineRule"), "auto")


def apply_caption_style(p: ET.Element) -> None:
    """图名/表名：居中、黑体、五号(10.5pt)、无缩进、单倍行距。"""
    ppr = ensure_ppr(p)
    pstyle = ppr.find("w:pStyle", NS)
    if pstyle is not None:
        ppr.remove(pstyle)
    apply_no_indent(p, center=True)
    spacing = ppr.find("w:spacing", NS)
    if spacing is None:
        spacing = ET.SubElement(ppr, qn("w:spacing"))
    spacing.set(qn("w:before"), "60")
    spacing.set(qn("w:after"), "60")
    spacing.set(qn("w:line"), "240")
    spacing.set(qn("w:lineRule"), "auto")
    for r in p.findall("w:r", NS):
        rpr = r.find("w:rPr", NS)
        if rpr is None:
            rpr = ET.SubElement(r, qn("w:rPr"))
            r.insert(0, rpr)
        else:
            for tag in ("rFonts", "sz", "szCs", "color", "b", "i"):
                el = rpr.find(f"w:{tag}", NS)
                if el is not None:
                    rpr.remove(el)
        fonts = ET.SubElement(rpr, qn("w:rFonts"))
        fonts.set(qn("w:ascii"), "黑体")
        fonts.set(qn("w:eastAsia"), "黑体")
        fonts.set(qn("w:hAnsi"), "黑体")
        sz = ET.SubElement(rpr, qn("w:sz"))
        sz.set(qn("w:val"), "21")
        sz_cs = ET.SubElement(rpr, qn("w:szCs"))
        sz_cs.set(qn("w:val"), "21")


def split_reference_entries(text: str) -> list[str]:
    parts = [part.strip() for part in REF_SPLIT.split(text) if part.strip()]
    return [part for part in parts if REF_ENTRY.match(part)]


def normalize_reference_block(body: ET.Element) -> None:
    """处理 pandoc 把「参考文献」与 [1]… 合并的问题。"""
    children = list(body)
    for idx, p in enumerate(children):
        text = paragraph_text(p)

        # 独立成段的「参考文献」标题。
        if text == "参考文献":
            apply_reference_heading_style(p)
            continue

        # 合并段：正文尾部 参考文献 [1]…[n]，或 参考文献 [1]…[n]。
        # 仅当「参考文献」后确实跟着 [n] 条目时才视为参考文献区，
        # 否则正文里「参考文献编号」之类的提及会被误判为标题。
        if "参考文献" in text:
            before, _, after = text.partition("参考文献")
            entries = split_reference_entries(after)
            if not entries:
                continue
            replacement = []
            if before.strip():
                replacement.append(make_text_paragraph(before.strip(), "BodyText"))
            heading = make_text_paragraph("参考文献")
            apply_reference_heading_style(heading)
            replacement.append(heading)
            replacement.extend(make_text_paragraph(entry, "Bibliography") for entry in entries)
            for offset, new_p in enumerate(replacement):
                body.insert(idx + offset, new_p)
            body.remove(p)
            return

        # 无标题词，但多条 [n] 被合并到同一段。
        entries = split_reference_entries(text)
        if len(entries) > 1:
            replacement = [make_text_paragraph(entry, "Bibliography") for entry in entries]
            for offset, new_p in enumerate(replacement):
                body.insert(idx + offset, new_p)
            body.remove(p)
            return


def _clear_attrs(el: ET.Element) -> None:
    for k in list(el.attrib):
        del el.attrib[k]


def _set_border(borders: ET.Element, name: str, val: str, sz: int) -> None:
    el = borders.find(f"w:{name}", NS)
    if el is None:
        el = ET.SubElement(borders, qn(f"w:{name}"))
    _clear_attrs(el)
    el.set(qn("w:val"), val)
    el.set(qn("w:sz"), str(sz))
    el.set(qn("w:space"), "0")
    el.set(qn("w:color"), "auto")


def format_cell_paragraph(p: ET.Element) -> None:
    """单元格内容：无缩进、单倍行距、居中、五号(10.5pt)。"""
    ppr = p.find("w:pPr", NS)
    if ppr is None:
        ppr = ET.Element(qn("w:pPr"))
        p.insert(0, ppr)
    spacing = ppr.find("w:spacing", NS)
    if spacing is None:
        spacing = ET.SubElement(ppr, qn("w:spacing"))
    _clear_attrs(spacing)
    spacing.set(qn("w:before"), "0")
    spacing.set(qn("w:after"), "0")
    spacing.set(qn("w:line"), "240")
    spacing.set(qn("w:lineRule"), "auto")
    ind = ppr.find("w:ind", NS)
    if ind is None:
        ind = ET.SubElement(ppr, qn("w:ind"))
    _clear_attrs(ind)
    for a in ("left", "leftChars", "firstLine", "firstLineChars"):
        ind.set(qn(f"w:{a}"), "0")
    jc = ppr.find("w:jc", NS)
    if jc is None:
        jc = ET.SubElement(ppr, qn("w:jc"))
    jc.set(qn("w:val"), "center")
    for r in p.findall("w:r", NS):
        rpr = r.find("w:rPr", NS)
        if rpr is None:
            rpr = ET.Element(qn("w:rPr"))
            r.insert(0, rpr)
        for tag in ("sz", "szCs"):
            el = rpr.find(f"w:{tag}", NS)
            if el is None:
                el = ET.SubElement(rpr, qn(f"w:{tag}"))
            el.set(qn("w:val"), "21")


def _is_inline_code_run(r: ET.Element) -> bool:
    """Pandoc 会把反引号内联代码导出为 Code/VerbatimChar 等样式或等宽字体。"""
    rpr = r.find("w:rPr", NS)
    if rpr is None:
        return False
    rstyle = rpr.find("w:rStyle", NS)
    if rstyle is not None:
        val = (rstyle.get(qn("w:val")) or "").lower()
        if any(key in val for key in ("code", "sourcecode", "verbatim")):
            return True
    fonts = rpr.find("w:rFonts", NS)
    if fonts is not None:
        values = " ".join(v.lower() for v in fonts.attrib.values())
        if any(name in values for name in ("consolas", "courier", "mono", "menlo")):
            return True
    return False


def normalize_inline_code_runs(p: ET.Element) -> None:
    """正文内联代码/API地址：按正文宋体小四显示，不使用等宽代码字体。"""
    for r in p.findall("w:r", NS):
        if not _is_inline_code_run(r):
            continue
        rpr = r.find("w:rPr", NS)
        if rpr is None:
            rpr = ET.Element(qn("w:rPr"))
            r.insert(0, rpr)
        for tag in ("rStyle", "rFonts", "sz", "szCs", "color", "highlight", "shd"):
            el = rpr.find(f"w:{tag}", NS)
            if el is not None:
                rpr.remove(el)
        fonts = ET.SubElement(rpr, qn("w:rFonts"))
        fonts.set(qn("w:ascii"), "宋体")
        fonts.set(qn("w:eastAsia"), "宋体")
        fonts.set(qn("w:hAnsi"), "宋体")
        sz = ET.SubElement(rpr, qn("w:sz"))
        sz.set(qn("w:val"), "24")
        sz_cs = ET.SubElement(rpr, qn("w:szCs"))
        sz_cs.set(qn("w:val"), "24")


def style_three_line_table(tbl: ET.Element) -> None:
    """三线表：上/下粗线、表头下细线，无竖线与其余横线；单元格统一格式。"""
    tblpr = tbl.find("w:tblPr", NS)
    if tblpr is None:
        tblpr = ET.Element(qn("w:tblPr"))
        tbl.insert(0, tblpr)
    tbl_jc = tblpr.find("w:jc", NS)
    if tbl_jc is None:
        tbl_jc = ET.SubElement(tblpr, qn("w:jc"))
    tbl_jc.set(qn("w:val"), "center")
    old = tblpr.find("w:tblBorders", NS)
    if old is not None:
        tblpr.remove(old)
    borders = ET.Element(qn("w:tblBorders"))
    _set_border(borders, "top", "single", 12)
    _set_border(borders, "bottom", "single", 12)
    _set_border(borders, "left", "nil", 0)
    _set_border(borders, "right", "nil", 0)
    _set_border(borders, "insideH", "nil", 0)
    _set_border(borders, "insideV", "nil", 0)
    layout = tblpr.find("w:tblLayout", NS)
    if layout is not None:
        tblpr.insert(list(tblpr).index(layout), borders)
    else:
        tblpr.append(borders)

    rows = tbl.findall("w:tr", NS)
    for ridx, tr in enumerate(rows):
        for tc in tr.findall("w:tc", NS):
            tcpr = tc.find("w:tcPr", NS)
            if tcpr is None:
                tcpr = ET.Element(qn("w:tcPr"))
                tc.insert(0, tcpr)
            if ridx == 0:  # 表头行底部细线
                tb = tcpr.find("w:tcBorders", NS)
                if tb is None:
                    tb = ET.SubElement(tcpr, qn("w:tcBorders"))
                _set_border(tb, "bottom", "single", 6)
            valign = tcpr.find("w:vAlign", NS)  # 垂直居中
            if valign is None:
                valign = ET.SubElement(tcpr, qn("w:vAlign"))
            valign.set(qn("w:val"), "center")
            for p in tc.findall("w:p", NS):
                format_cell_paragraph(p)


def _ensure_superscript(rpr: ET.Element) -> None:
    va = rpr.find("w:vertAlign", NS)
    if va is None:
        va = ET.SubElement(rpr, qn("w:vertAlign"))
    va.set(qn("w:val"), "superscript")


def _run_rpr(rpr_src: ET.Element | None, *, superscript: bool = False) -> ET.Element:
    rpr = copy.deepcopy(rpr_src) if rpr_src is not None else ET.Element(qn("w:rPr"))
    if superscript:
        _ensure_superscript(rpr)
    return rpr


def _make_run(text: str, rpr_src: ET.Element | None, *, superscript: bool = False) -> ET.Element:
    r = ET.Element(qn("w:r"))
    rpr = _run_rpr(rpr_src, superscript=superscript)
    if len(rpr):
        r.append(rpr)
    t = ET.SubElement(r, qn("w:t"))
    t.text = text
    if text != text.strip():
        t.set(f"{{{XML}}}space", "preserve")
    return r


def _make_fldsimple(
    instr: str, cached: str, rpr_src: ET.Element | None, *, superscript: bool = True
) -> ET.Element:
    fld = ET.Element(qn("w:fldSimple"))
    fld.set(qn("w:instr"), instr)
    r = ET.SubElement(fld, qn("w:r"))
    rpr = _run_rpr(rpr_src, superscript=superscript)
    if len(rpr):
        r.append(rpr)
    t = ET.SubElement(r, qn("w:t"))
    t.text = cached
    return fld


def _make_bookmark(bid: int, name: str) -> tuple[ET.Element, ET.Element]:
    start = ET.Element(qn("w:bookmarkStart"))
    start.set(qn("w:id"), str(bid))
    start.set(qn("w:name"), name)
    end = ET.Element(qn("w:bookmarkEnd"))
    end.set(qn("w:id"), str(bid))
    return start, end


def _replace_run(p: ET.Element, run: ET.Element, nodes: list[ET.Element]) -> None:
    idx = list(p).index(run)
    p.remove(run)
    for offset, node in enumerate(nodes):
        p.insert(idx + offset, node)


def convert_body_citations(p: ET.Element) -> None:
    """正文 [n]/[n-m]/[n,m] → 上标交叉引用域（REF refN \\r \\h）。

    每个数字编号返回带方括号的列表编号（如 [14]），区间/多篇按展开式呈现：
    [14-16] → [14]-[16]，[7-8,11] → [7]-[8],[11]；整段引用标记均为上标。
    """
    for run in list(p.findall("w:r", NS)):
        t_el = run.find("w:t", NS)
        if t_el is None or not t_el.text or not CITE.search(t_el.text):
            continue
        rpr = run.find("w:rPr", NS)
        text = t_el.text
        nodes: list[ET.Element] = []
        last = 0
        for m in CITE.finditer(text):
            if m.start() > last:
                nodes.append(_make_run(text[last:m.start()], rpr, superscript=False))
            for piece in re.findall(r"\d+|[^\d]+", m.group(1)):
                if piece.isdigit():
                    nodes.append(
                        _make_fldsimple(f" REF ref{piece} \\r \\h ", f"[{piece}]", rpr)
                    )
                else:
                    nodes.append(_make_run(piece, rpr, superscript=True))
            last = m.end()
        if last < len(text):
            nodes.append(_make_run(text[last:], rpr, superscript=False))
        _replace_run(p, run, nodes)


def convert_reference_entry(p: ET.Element, bid: int) -> int:
    """参考文献条目改为原生自动编号列表项，并加书签 refN 供「编号项」交叉引用。

    去掉手写的 [n] 前缀，挂上编号列表（numId=REF_NUM_ID，格式 [1]），
    用书签包住整段内容，正文 REF \\r 即可取到该段的列表编号。
    """
    num = None
    for run in p.findall("w:r", NS):
        t_el = run.find("w:t", NS)
        if t_el is None or not t_el.text:
            continue
        m = re.match(r"^\s*\[(\d+)\]\s*(.*)$", t_el.text, re.S)
        if not m:
            return bid
        num, rest = m.group(1), m.group(2)
        t_el.text = rest
        if rest != rest.strip():
            t_el.set(f"{{{XML}}}space", "preserve")
        break
    if num is None:
        return bid

    ppr = ensure_ppr(p)
    old = ppr.find("w:numPr", NS)
    if old is not None:
        ppr.remove(old)
    pstyle = ppr.find("w:pStyle", NS)
    numpr = ET.Element(qn("w:numPr"))
    ilvl = ET.SubElement(numpr, qn("w:ilvl"))
    ilvl.set(qn("w:val"), "0")
    nid = ET.SubElement(numpr, qn("w:numId"))
    nid.set(qn("w:val"), str(REF_NUM_ID))
    insert_at = list(ppr).index(pstyle) + 1 if pstyle is not None else 0
    ppr.insert(insert_at, numpr)

    start, end = _make_bookmark(bid, f"ref{num}")
    body_idx = 1 if (len(p) and p[0].tag == qn("w:pPr")) else 0
    p.insert(body_idx, start)
    p.append(end)
    return bid + 1


def disable_widow_control(body: ET.Element) -> None:
    """全文关闭孤行控制（Word 段落「孤行控制」= widowControl）。"""
    for p in body.iter(qn("w:p")):
        ppr = ensure_ppr(p)
        wc = ppr.find("w:widowControl", NS)
        if wc is None:
            wc = ET.SubElement(ppr, qn("w:widowControl"))
        wc.set(qn("w:val"), "0")


def strip_heading_keep_together(body: ET.Element) -> None:
    """去掉标题段落的 keepNext/keepLines（防止页尾被整块推到下一页）。"""
    heading_styles = {
        "Heading1", "Heading2", "Heading3", "Heading4",
        "Heading5", "Heading6", "Heading7", "Heading8", "Heading9",
    }
    for p in body.findall("w:p", NS):
        ppr = p.find("w:pPr", NS)
        if ppr is None:
            continue
        ps = ppr.find("w:pStyle", NS)
        if ps is None or ps.get(qn("w:val")) not in heading_styles:
            continue
        for tag in ("keepNext", "keepLines", "pageBreakBefore"):
            el = ppr.find(f"w:{tag}", NS)
            if el is not None:
                ppr.remove(el)


def ensure_doc_grid(body: ET.Element) -> None:
    """给节属性补上行网格，与模版一致（w:docGrid type=lines linePitch=312）。

    模版开启了文档行网格 + 段落「对齐到网格」，1.5 倍行距时每行吸附到等距网格、
    文字垂直居中；pandoc 默认无 docGrid，多余行距全堆到文字下方，观感不同。
    """
    sect = body.find("w:sectPr", NS)
    if sect is None:
        return
    grid = sect.find("w:docGrid", NS)
    if grid is None:
        grid = ET.SubElement(sect, qn("w:docGrid"))
    grid.set(qn("w:type"), "lines")
    grid.set(qn("w:linePitch"), "312")


def _ref_abstract_num_xml() -> str:
    return (
        f'<w:abstractNum w:abstractNumId="{REF_ABSTRACT_ID}">'
        '<w:multiLevelType w:val="singleLevel"/>'
        '<w:lvl w:ilvl="0">'
        '<w:start w:val="1"/>'
        '<w:numFmt w:val="decimal"/>'
        '<w:lvlText w:val="[%1]"/>'
        '<w:lvlJc w:val="left"/>'
        '<w:pPr><w:ind w:left="442" w:hanging="442"/></w:pPr>'
        '</w:lvl></w:abstractNum>'
    )


def _ref_num_xml() -> str:
    return (
        f'<w:num w:numId="{REF_NUM_ID}">'
        f'<w:abstractNumId w:val="{REF_ABSTRACT_ID}"/></w:num>'
    )


def patch_numbering_xml(nb: str) -> str:
    """向 numbering.xml 追加参考文献编号定义（abstractNum 必须在 num 之前）。"""
    if f'w:numId="{REF_NUM_ID}"' in nb:
        return nb
    abstract = _ref_abstract_num_xml()
    num = _ref_num_xml()
    pos = nb.find("<w:num ")
    if pos == -1:
        pos = nb.rfind("</w:numbering>")
    nb = nb[:pos] + abstract + nb[pos:]
    end = nb.rfind("</w:numbering>")
    return nb[:end] + num + nb[end:]


def postprocess_docx(path: Path, title_text: str = "项目调研报告") -> None:
    ET.register_namespace("w", W)
    with zipfile.ZipFile(path, "r") as zin:
        doc_xml = zin.read("word/document.xml")
        has_numbering = "word/numbering.xml" in zin.namelist()
        numbering_xml = zin.read("word/numbering.xml").decode("utf-8") if has_numbering else None

    root = ET.fromstring(doc_xml)
    body = root.find("w:body", NS)
    if body is None:
        raise ValueError("document.xml 缺少 w:body")

    for p in body.findall("w:p", NS):
        if paragraph_text(p) == title_text:
            apply_title_style(p)
            break

    normalize_reference_block(body)

    in_references = False
    bid = BOOKMARK_ID_BASE
    for p in body.findall("w:p", NS):
        if paragraph_has_image(p):
            apply_image_paragraph_style(p)

        text = paragraph_text(p)
        if not text:
            continue
        if text == "参考文献":
            in_references = True
            continue
        if in_references:
            if REF_ENTRY.match(text):
                apply_bibliography_style(p)
                bid = convert_reference_entry(p, bid)
            continue
        normalize_inline_code_runs(p)
        if CAPTION.match(text):
            apply_caption_style(p)
        else:
            convert_body_citations(p)

    for tbl in body.findall("w:tbl", NS):
        style_three_line_table(tbl)

    disable_widow_control(body)
    strip_heading_keep_together(body)
    ensure_doc_grid(body)

    patched = ET.tostring(root, encoding="utf-8", xml_declaration=True)
    patched_numbering = (
        patch_numbering_xml(numbering_xml).encode("utf-8") if numbering_xml is not None else None
    )
    tmp = path.with_suffix(".post.tmp.docx")
    with zipfile.ZipFile(path, "r") as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            if item.filename == "word/document.xml":
                data = patched
            elif item.filename == "word/numbering.xml" and patched_numbering is not None:
                data = patched_numbering
            else:
                data = zin.read(item.filename)
            zout.writestr(item, data)
    tmp.replace(path)


def main() -> None:
    if len(sys.argv) != 2:
        print(f"用法: {sys.argv[0]} <输出.docx>", file=sys.stderr)
        sys.exit(1)
    postprocess_docx(Path(sys.argv[1]).resolve())


if __name__ == "__main__":
    main()
