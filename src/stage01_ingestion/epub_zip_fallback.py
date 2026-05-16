"""Read EPUB X/HTML via ZIP + OPF when ``ebooklib.read_epub`` fails.

Resolves manifest paths with **case-insensitive** matching against ``ZipFile.namelist``
(Linux-friendly for broken publisher casing). Walks ``<spine>`` order; skips missing
or non-HTML manifest items instead of aborting the whole book.
"""

from __future__ import annotations

import posixpath
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Optional, Tuple

_HTML_MEDIA = frozenset(
    {
        "application/xhtml+xml",
        "application/html+xml",
        "text/html",
        "text/xhtml",
    }
)


def _tag_local(tag: str) -> str:
    if tag.startswith("{") and "}" in tag:
        return tag.split("}", 1)[1]
    return tag


def _zip_name_index(names: List[str]) -> Dict[str, str]:
    return {n.replace("\\", "/").lower(): n for n in names}


def _read_member_ci(zf: zipfile.ZipFile, index: Dict[str, str], rel_path: str) -> Optional[bytes]:
    key = rel_path.replace("\\", "/").strip("/").lower()
    real = index.get(key)
    if real is None:
        return None
    return zf.read(real)


def _rootfile_path_from_container(xml_bytes: bytes) -> Optional[str]:
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError:
        return None
    for el in root.iter():
        if _tag_local(el.tag) == "rootfile":
            fp = el.get("full-path")
            if fp:
                return fp.replace("\\", "/").strip()
    return None


def _is_html_item(href: str, media_type: Optional[str]) -> bool:
    lower = href.lower()
    if media_type:
        mt = media_type.split(";")[0].strip().lower()
        if mt in _HTML_MEDIA:
            return True
    return lower.endswith((".html", ".htm", ".xhtml"))


def iter_spine_html_raw(epub_path: Path) -> Tuple[List[Tuple[str, bytes]], Optional[str]]:
    """
    Return (list of (logical_path, raw_html_bytes), error).

    ``logical_path`` is the path used inside the EPUB (for debugging), not necessarily
    the on-disk zip member spelling.
    """
    if not epub_path.is_file():
        return [], "missing_file"

    try:
        zf = zipfile.ZipFile(epub_path, "r")
    except zipfile.BadZipFile as e:
        return [], f"bad_zip:{e}"

    with zf:
        index = _zip_name_index(zf.namelist())
        cxml = _read_member_ci(zf, index, "META-INF/container.xml")
        if not cxml:
            return [], "missing_container_xml"

        opf_rel = _rootfile_path_from_container(cxml)
        if not opf_rel:
            return [], "container_parse_failed"

        opf_bytes = _read_member_ci(zf, index, opf_rel)
        if not opf_bytes:
            return [], f"missing_opf:{opf_rel}"

        opf_dir = posixpath.dirname(opf_rel.replace("\\", "/"))

        try:
            opf_root = ET.fromstring(opf_bytes)
        except ET.ParseError:
            return [], "opf_parse_error"

        id_to_href: Dict[str, str] = {}
        id_to_media: Dict[str, Optional[str]] = {}
        for el in opf_root.iter():
            if _tag_local(el.tag) != "item":
                continue
            iid = el.get("id")
            href = el.get("href")
            if not iid or not href:
                continue
            id_to_href[iid] = href.replace("\\", "/")
            id_to_media[iid] = el.get("media-type")

        spine_ids: List[str] = []
        for el in opf_root.iter():
            if _tag_local(el.tag) != "itemref":
                continue
            idref = el.get("idref")
            if idref:
                spine_ids.append(idref)

        out: List[Tuple[str, bytes]] = []
        for sid in spine_ids:
            href = id_to_href.get(sid)
            if not href:
                continue
            media = id_to_media.get(sid)
            if not _is_html_item(href, media):
                continue
            full = posixpath.normpath(posixpath.join(opf_dir or "", href)).replace("\\", "/")
            raw = _read_member_ci(zf, index, full)
            if raw is None:
                continue
            out.append((full, raw))

    if not out:
        return [], "zip_fallback_no_html_from_spine"
    return out, None


def zip_fallback_plain_stats(epub_path: Path) -> Tuple[int, int, Optional[str]]:
    """Return (n_docs, n_chars_plain_space_collapsed, error_or_none) without spaCy."""
    chapters, err = iter_spine_html_raw(epub_path)
    if err:
        return 0, 0, err
    total_chars = 0
    # Lightweight strip: no BeautifulSoup import here (repair script stays light).
    for _path, raw in chapters:
        try:
            text = raw.decode("utf-8", errors="replace")
        except Exception:
            text = ""
        # crude tag strip for stats only
        in_tag = False
        buf: List[str] = []
        for ch in text:
            if ch == "<":
                in_tag = True
                continue
            if ch == ">":
                in_tag = False
                continue
            if not in_tag:
                buf.append(ch)
        collapsed = " ".join("".join(buf).split())
        total_chars += len(collapsed)
    return len(chapters), total_chars, None
