"""Human-review packet export (topic id, keywords, sentences, taxonomy, codes)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Sequence

from src.stage11_refined_construct_analysis.config import Stage11Config


def build_human_review_packet(
    evidence_packet: Mapping[str, Any],
    *,
    classification_codes: Optional[Mapping[str, Any]] = None,
) -> Dict[str, Any]:
    """Assemble a human-readable review packet (taxonomy visible for reviewers)."""
    lexical = evidence_packet.get("lexical", {})
    reveal = evidence_packet.get("pass_c_reveal", {})
    sentences = evidence_packet.get("contextual", {}).get("sentences", [])
    # Cap for human readability
    sample_sents = sentences[:12]
    return {
        "topic_id": evidence_packet.get("topic_id"),
        "label": lexical.get("label_public"),
        "taxonomy_main_id": reveal.get("taxonomy_main_id"),
        "taxonomy_main_name": reveal.get("taxonomy_main_name"),
        "taxonomy_secondary_id": reveal.get("taxonomy_secondary_id"),
        "taxonomy_secondary_name": reveal.get("taxonomy_secondary_name"),
        "exhaustive": bool(evidence_packet.get("exhaustive")),
        "representations": lexical.get("representations", {}),
        "stage08_snippets": lexical.get("stage08_snippets", []),
        "representative_sentences": [
            {
                "sid": s.get("sid"),
                "cell": s.get("cell"),
                "tertile": s.get("tertile"),
                "normalized_position": s.get("normalized_position"),
                "max_topic_prob": s.get("max_topic_prob"),
                "sentence": s.get("sentence"),
            }
            for s in sample_sents
        ],
        "classification_codes": dict(classification_codes or {}),
        "review_status": "pending",
    }


def write_human_review_packets(
    cfg: Stage11Config,
    packets: Mapping[int, Mapping[str, Any]],
    *,
    codes_by_topic: Optional[Mapping[int, Mapping[str, Any]]] = None,
) -> Path:
    out_dir = cfg.output_path("human_review_dir", create=True)
    index = []
    for tid, packet in sorted(packets.items(), key=lambda x: int(x[0])):
        review = build_human_review_packet(
            packet,
            classification_codes=(codes_by_topic or {}).get(int(tid)),
        )
        path = out_dir / f"topic_{int(tid):04d}.json"
        path.write_text(json.dumps(review, indent=2, ensure_ascii=False), encoding="utf-8")
        index.append({"topic_id": int(tid), "path": str(path.relative_to(cfg.root))})
    index_path = out_dir / "index.json"
    index_path.write_text(json.dumps(index, indent=2), encoding="utf-8")
    return index_path
