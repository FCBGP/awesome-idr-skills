#!/usr/bin/env python3
"""生成 Pandoc 专用样式母版：规则写在脚本里，不依赖 调研报告模版.docx。"""

from __future__ import annotations

import shutil
import subprocess
import tempfile
import zipfile
import xml.etree.ElementTree as ET
from copy import deepcopy
from pathlib import Path

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}
W_TAG = lambda local: f"{{{W}}}{local}"


def qn(tag: str) -> str:
    prefix, local = tag.split(":")
    return f"{{{NS[prefix]}}}{local}"


def ensure_child(parent: ET.Element, tag: str) -> ET.Element:
    el = parent.find(f"w:{tag}", NS)
    if el is None:
        el = ET.SubElement(parent, qn(f"w:{tag}"))
    return el


def set_attr(el: ET.Element, name: str, value: str) -> None:
    el.set(qn(f"w:{name}"), value)


def clear_attrs(el: ET.Element) -> None:
    for key in list(el.attrib):
        del el.attrib[key]


def clear_children(parent: ET.Element) -> None:
    for child in list(parent):
        parent.remove(child)


def patch_style(style: ET.Element, *, ppr: dict | None = None, rpr: dict | None = None) -> None:
    if ppr:
        ppr_el = ensure_child(style, "pPr")
        for key, value in ppr.items():
            if key == "spacing":
                sp = ensure_child(ppr_el, "spacing")
                clear_attrs(sp)
                clear_children(sp)
                for sk, sv in value.items():
                    set_attr(sp, sk, sv)
            elif key == "ind":
                ind = ensure_child(ppr_el, "ind")
                clear_attrs(ind)
                clear_children(ind)
                for ik, iv in value.items():
                    set_attr(ind, ik, iv)
            elif key == "jc":
                jc = ensure_child(ppr_el, "jc")
                set_attr(jc, "val", value)
            elif key == "snapToGrid":
                sg = ensure_child(ppr_el, "snapToGrid")
                set_attr(sg, "val", value)
            elif key == "widowControl":
                wc = ensure_child(ppr_el, "widowControl")
                set_attr(wc, "val", value)
            elif key in ("keepNext", "keepLines", "pageBreakBefore") and value is False:
                el = ppr_el.find(f"w:{key}", NS)
                if el is not None:
                    ppr_el.remove(el)
    if rpr:
        rpr_el = ensure_child(style, "rPr")
        for key, value in rpr.items():
            if key == "rFonts":
                fonts = ensure_child(rpr_el, "rFonts")
                # 清除主题字体属性，避免覆盖显式字体（黑体/宋体）
                for theme_attr in ("asciiTheme", "hAnsiTheme", "eastAsiaTheme", "cstheme"):
                    a = qn(f"w:{theme_attr}")
                    if a in fonts.attrib:
                        del fonts.attrib[a]
                for fk, fv in value.items():
                    set_attr(fonts, fk, fv)
            elif key == "sz":
                sz = ensure_child(rpr_el, "sz")
                set_attr(sz, "val", value)
                sz_cs = rpr_el.find("w:szCs", NS)
                if sz_cs is None:
                    sz_cs = ET.SubElement(rpr_el, qn("w:szCs"))
                set_attr(sz_cs, "val", value)
            elif key == "color":
                color = ensure_child(rpr_el, "color")
                clear_attrs(color)  # 清掉 themeColor 等，避免主题色覆盖纯色
                set_attr(color, "val", value)
            elif key == "b":
                if value:
                    ensure_child(rpr_el, "b")
                else:  # 去掉加粗
                    for t in ("b", "bCs"):
                        e = rpr_el.find(f"w:{t}", NS)
                        if e is not None:
                            rpr_el.remove(e)
            elif key == "i":
                if value:
                    ensure_child(rpr_el, "i")
                else:  # 去掉斜体（pandoc 默认标题4/5 带斜体）
                    for t in ("i", "iCs"):
                        e = rpr_el.find(f"w:{t}", NS)
                        if e is not None:
                            rpr_el.remove(e)


def patch_doc_defaults(styles_root: ET.Element) -> None:
    doc_defaults = styles_root.find("w:docDefaults", NS)
    if doc_defaults is None:
        doc_defaults = ET.SubElement(styles_root, qn("w:docDefaults"))
    ppr_default = doc_defaults.find("w:pPrDefault", NS)
    if ppr_default is None:
        ppr_default = ET.SubElement(doc_defaults, qn("w:pPrDefault"))
    ppr = ppr_default.find("w:pPr", NS)
    if ppr is None:
        ppr = ET.SubElement(ppr_default, qn("w:pPr"))
    wc = ensure_child(ppr, "widowControl")
    set_attr(wc, "val", "0")

    rpr = styles_root.find("w:docDefaults/w:rPrDefault/w:rPr", NS)
    if rpr is None:
        return
    fonts = ensure_child(rpr, "rFonts")
    set_attr(fonts, "ascii", "宋体")
    set_attr(fonts, "eastAsia", "宋体")
    set_attr(fonts, "hAnsi", "宋体")
    sz = ensure_child(rpr, "sz")
    set_attr(sz, "val", "24")
    sz_cs = rpr.find("w:szCs", NS)
    if sz_cs is None:
        sz_cs = ET.SubElement(rpr, qn("w:szCs"))
    set_attr(sz_cs, "val", "24")


def find_style(styles_root: ET.Element, style_id: str) -> ET.Element | None:
    for style in styles_root.findall("w:style", NS):
        if style.get(W_TAG("styleId")) == style_id:
            return style
    return None


def clone_style(styles_root: ET.Element, source_id: str, new_id: str, new_name: str) -> ET.Element:
    src = find_style(styles_root, source_id)
    if src is None:
        raise KeyError(f"style not found: {source_id}")
    cloned = deepcopy(src)
    cloned.set(W_TAG("styleId"), new_id)
    name_el = cloned.find("w:name", NS)
    if name_el is None:
        name_el = ET.SubElement(cloned, qn("w:name"))
    name_el.set(W_TAG("val"), new_name)
    styles_root.append(cloned)
    return cloned


# A4 页面与页边距（与原 调研报告模版.docx 一致，已固化在脚本中）
PAGE_SZ = {"w": "11906", "h": "16838"}
PAGE_MAR = {
    "top": "1440",
    "right": "1800",
    "bottom": "1440",
    "left": "1800",
    "header": "851",
    "footer": "992",
    "gutter": "0",
}
BODY_PPR = {
    "jc": "both",
    "ind": {"firstLine": "425", "firstLineChars": "177"},
    "spacing": {"before": "0", "after": "0", "line": "360", "lineRule": "auto"},
}
# 参考文献条目：两端对齐、悬挂缩进 0.78 cm（442 twips）、左侧 0、1.5 倍行距、段前段后 0（见模版「段落」对话框）
# 注意：Bibliography 不再 basedOn Normal（见 patch_reference_styles），以免继承 Normal 的
# firstLineChars=177（字符版首行缩进）——Word 里字符版会压过磅值版悬挂，导致悬挂失效。
# 去掉继承后，这里纯磅值 left/hanging 即可稳定生效（Word 显示 左侧0、悬挂0.78cm）。
BIBLIO_PPR = {
    "jc": "both",
    "ind": {"left": "442", "hanging": "442"},
    "spacing": {"before": "0", "after": "0", "line": "360", "lineRule": "auto"},
    # 五号字在文档行网格下会被吸附放大行距，参考文献关掉「对齐到网格」即可正常 1.5 倍
    "snapToGrid": "0",
}
# 项目符号 / 分点列表：左缩进 0.75 cm、悬挂 0.78 cm
LIST_PPR = {
    "jc": "both",
    "ind": {"left": "425", "hanging": "442"},
    "spacing": {"before": "0", "after": "0", "line": "360", "lineRule": "auto"},
}
TITLE_PPR = {
    "jc": "center",
    "ind": {},
    "spacing": {"line": "360", "lineRule": "auto"},
}
TITLE_RPR = {
    "rFonts": {"ascii": "黑体", "eastAsia": "黑体", "hAnsi": "黑体"},
    "sz": "44",
    "color": "auto",
    "b": True,
}
BODY_RPR = {
    "rFonts": {"ascii": "宋体", "eastAsia": "宋体", "hAnsi": "宋体"},
    "sz": "24",
    "color": "auto",
}
# 参考文献：宋体五号（10.5pt，sz21），与模版一致
BIBLIO_RPR = {
    "rFonts": {"ascii": "宋体", "eastAsia": "宋体", "hAnsi": "宋体"},
    "sz": "21",
    "color": "auto",
}
# 标题：黑体、黑色、不加粗、无斜体、无缩进
# 一级~三级 均为四号14pt；四级 小四12pt（按截图）
HEAD_FONTS = {"ascii": "黑体", "eastAsia": "黑体", "hAnsi": "黑体"}
HEAD_COLOR = "000000"
H1_RPR = {"rFonts": HEAD_FONTS, "sz": "28", "color": HEAD_COLOR, "b": False, "i": False}
H2_RPR = {"rFonts": HEAD_FONTS, "sz": "28", "color": HEAD_COLOR, "b": False, "i": False}
H3_RPR = {"rFonts": HEAD_FONTS, "sz": "28", "color": HEAD_COLOR, "b": False, "i": False}
H4_RPR = {"rFonts": HEAD_FONTS, "sz": "24", "color": HEAD_COLOR, "b": False, "i": False}
# 标题：单倍行距、两端对齐、无缩进；各级均段前6/段后6 磅
# 显式归零缩进（标题基于 Normal，会继承正文首行缩进，必须用 0 覆盖）
SINGLE_LINE = {"line": "240", "lineRule": "auto"}
NO_IND = {"left": "0", "leftChars": "0", "firstLine": "0", "firstLineChars": "0"}
NO_KEEP = {"keepNext": False, "keepLines": False, "pageBreakBefore": False}
H1_PPR = {
    "jc": "both",
    "ind": dict(NO_IND),
    "spacing": {"before": "120", "after": "120", **SINGLE_LINE},
    **NO_KEEP,
}
H2_PPR = {
    "jc": "both",
    "ind": dict(NO_IND),
    "spacing": {"before": "120", "after": "120", **SINGLE_LINE},
    **NO_KEEP,
}
H3_PPR = {**H2_PPR}
H4_PPR = {
    "jc": "both",
    "ind": dict(NO_IND),
    "spacing": {"before": "120", "after": "120", **SINGLE_LINE},
    **NO_KEEP,
}


def patch_reference_styles(styles_root: ET.Element) -> None:
    patch_doc_defaults(styles_root)

    title = find_style(styles_root, "Title")
    if title is None:
        title = clone_style(styles_root, "Normal", "Title", "Title")
    patch_style(title, ppr=TITLE_PPR, rpr=TITLE_RPR)

    for style_id, ppr, rpr in [
        ("Normal", BODY_PPR, BODY_RPR),
        ("FirstParagraph", BODY_PPR, BODY_RPR),
        ("BodyText", BODY_PPR, BODY_RPR),
        ("Heading1", H1_PPR, H1_RPR),
        ("Heading2", H2_PPR, H2_RPR),
        ("Heading3", H3_PPR, H3_RPR),
    ]:
        style = find_style(styles_root, style_id)
        if style is None:
            style = clone_style(styles_root, "Normal", style_id, style_id.replace("Heading", "heading "))
        patch_style(style, ppr=ppr, rpr=rpr)

    bib = find_style(styles_root, "Bibliography")
    if bib is None:
        bib = clone_style(styles_root, "Normal", "Bibliography", "Bibliography")
    patch_style(bib, ppr=BIBLIO_PPR, rpr=BIBLIO_RPR)
    # 解除 basedOn Normal：否则会继承 Normal 的字符版首行缩进(firstLineChars=177)，
    # 在 Word 中压过磅值版悬挂。解除后字体/字号已由 BODY_RPR 与 docDefaults 显式给定。
    based_on = bib.find("w:basedOn", NS)
    if based_on is not None:
        bib.remove(based_on)

    for list_sid in ["Compact", "ListParagraph"]:
        lst = find_style(styles_root, list_sid)
        if lst is None:
            lst = clone_style(styles_root, "Normal", list_sid, list_sid)
        patch_style(lst, ppr=LIST_PPR, rpr=BODY_RPR)

    # 标题4：黑体小四、段后 8 磅（与模版一致）
    h4 = find_style(styles_root, "Heading4")
    if h4 is None:
        h4 = clone_style(styles_root, "Normal", "Heading4", "heading 4")
    patch_style(h4, ppr=H4_PPR, rpr=H4_RPR)

    # 避免 pandoc 继续套用 Word 主题里的蓝绿色标题
    for sid in ["Heading5", "Heading6", "Heading7", "Heading8", "Heading9"]:
        style = find_style(styles_root, sid)
        if style is not None:
            patch_style(style, ppr=H3_PPR, rpr=H3_RPR)

    disable_widow_control_all_styles(styles_root)
    disable_heading_keep_together(styles_root)


def disable_heading_keep_together(styles_root: ET.Element) -> None:
    """去掉标题「与下段同页 / 段中不分页」，避免页尾大块空白。"""
    for style in styles_root.findall("w:style", NS):
        sid = style.get(W_TAG("styleId")) or ""
        if not sid.startswith("Heading"):
            continue
        ppr = style.find("w:pPr", NS)
        if ppr is None:
            continue
        for tag in ("keepNext", "keepLines", "pageBreakBefore"):
            el = ppr.find(f"w:{tag}", NS)
            if el is not None:
                ppr.remove(el)


def disable_widow_control_all_styles(styles_root: ET.Element) -> None:
    """关闭孤行控制（widowControl），与模版 Normal 一致。"""
    for style in styles_root.findall("w:style", NS):
        ppr = style.find("w:pPr", NS)
        if ppr is None:
            continue
        wc = ensure_child(ppr, "widowControl")
        set_attr(wc, "val", "0")


def export_pandoc_default_reference(path: Path) -> None:
    data = subprocess.check_output(["pandoc", "--print-default-data-file", "reference.docx"])
    path.write_bytes(data)


def patch_reference_document_page(output: Path) -> None:
    """在 reference 的 document.xml 写入 A4 页边距（供 pandoc 继承）。"""
    with zipfile.ZipFile(output, "r") as zin:
        doc_xml = zin.read("word/document.xml")

    ET.register_namespace("w", W)
    root = ET.fromstring(doc_xml)
    body = root.find("w:body", NS)
    if body is None:
        return
    sect = body.find("w:sectPr", NS)
    if sect is None:
        sect = ET.SubElement(body, qn("w:sectPr"))

    pg_sz = sect.find("w:pgSz", NS)
    if pg_sz is None:
        pg_sz = ET.SubElement(sect, qn("w:pgSz"))
    clear_attrs(pg_sz)
    for k, v in PAGE_SZ.items():
        set_attr(pg_sz, k, v)

    pg_mar = sect.find("w:pgMar", NS)
    if pg_mar is None:
        pg_mar = ET.SubElement(sect, qn("w:pgMar"))
    clear_attrs(pg_mar)
    for k, v in PAGE_MAR.items():
        set_attr(pg_mar, k, v)

    patched = ET.tostring(root, encoding="utf-8", xml_declaration=True)
    tmp = output.with_suffix(".page.tmp.docx")
    with zipfile.ZipFile(output, "r") as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = patched if item.filename == "word/document.xml" else zin.read(item.filename)
            zout.writestr(item, data)
    tmp.replace(output)


def build_reference(output: Path) -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        base = Path(tmpdir) / "pandoc-default.docx"
        export_pandoc_default_reference(base)
        shutil.copy2(base, output)

    with zipfile.ZipFile(output, "r") as zin:
        styles_xml = zin.read("word/styles.xml")

    ET.register_namespace("w", W)
    styles_root = ET.fromstring(styles_xml)
    patch_reference_styles(styles_root)
    patched = ET.tostring(styles_root, encoding="utf-8", xml_declaration=True)

    tmp = output.with_suffix(".tmp.docx")
    with zipfile.ZipFile(output, "r") as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = patched if item.filename == "word/styles.xml" else zin.read(item.filename)
            zout.writestr(item, data)
    tmp.replace(output)

    patch_reference_document_page(output)


def main() -> None:
    base = Path(__file__).resolve().parent
    output = base / "调研报告-reference.docx"
    build_reference(output)
    print(f"已生成样式母版: {output}")
    print("说明: 由 pandoc 默认 reference + 本脚本规则生成，无需 调研报告模版.docx。")


if __name__ == "__main__":
    main()
