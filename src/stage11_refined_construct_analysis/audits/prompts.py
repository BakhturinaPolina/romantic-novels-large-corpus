"""Hypothesis audit helpers: load frozen prompts and format Pass A/B/C messages."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Mapping, Sequence

from src.stage11_refined_construct_analysis.config import Stage11Config, load_prompt_yaml


HYPOTHESIS_PROMPT_KEYS = {
    "H1": "h1_intimacy.yaml",
    "H2": "h2_hea.yaml",
    "H3": "h3_security.yaml",
    "H4": "h4_protection.yaml",
    "H5": "h5_darkness.yaml",
    "H6": "h6_arc.yaml",
}


def prompt_path_for(cfg: Stage11Config, hypothesis: str) -> Path:
    hyp = str(hypothesis).upper()
    configured = cfg.section("hypotheses", hyp).get("prompt")
    if configured:
        path = Path(configured)
        if not path.is_absolute():
            path = cfg.root / path
        return path
    name = HYPOTHESIS_PROMPT_KEYS[hyp]
    return cfg.root / "configs" / "stage11" / "prompts" / name


def load_hypothesis_prompt(
    cfg: Stage11Config,
    hypothesis: str,
    *,
    prompt_path: Path | str | None = None,
) -> Dict[str, Any]:
    path = Path(prompt_path) if prompt_path else prompt_path_for(cfg, hypothesis)
    if not path.is_absolute():
        path = cfg.root / path
    data = load_prompt_yaml(path)
    if not data.get("frozen", False):
        raise ValueError(f"Prompt for {hypothesis} is not marked frozen: {path}")
    return data


def rep_lists(packet: Mapping[str, Any]) -> Dict[str, str]:
    """Flatten four keyword representations for prompt formatting."""
    reps = packet.get("lexical", {}).get("representations", {})
    out = {}
    for name in ("Main", "KeyBERT", "POS", "MMR"):
        words = reps.get(name) or []
        out[name.lower()] = ", ".join(str(w) for w in words) if words else "(none)"
    return out


# Back-compat alias
_rep_lists = rep_lists


def format_sentences_block(
    packet: Mapping[str, Any],
    *,
    show_position: bool = False,
    max_sentences: int = 40,
) -> str:
    lines = []
    for sent in packet.get("contextual", {}).get("sentences", [])[:max_sentences]:
        bits = [f"[{sent.get('sid')}]", f"cell={sent.get('cell')}"]
        if show_position:
            bits.append(f"tertile={sent.get('tertile')}")
            pos = sent.get("normalized_position")
            if pos is not None:
                bits.append(f"pos={float(pos):.2f}")
        bits.append(f"p={sent.get('max_topic_prob')}")
        header = " ".join(str(b) for b in bits)
        lines.append(f"{header}\n{sent.get('sentence', '').strip()}")
    return "\n\n".join(lines) if lines else "(no contextual sentences)"


def format_pass_messages(
    prompt: Mapping[str, Any],
    packet: Mapping[str, Any],
    *,
    phrasing: str = "primary",
    pass_name: str = "A",
    lexical_consensus: str = "",
    contextual_dominant: str = "",
    max_sentences: int | None = None,
) -> Dict[str, str]:
    """Return system + user messages for one pass."""
    block = prompt["phrasing"][phrasing]
    reps = rep_lists(packet)
    show_pos = bool(prompt.get("pass_b_shows_position", False))
    reveal = packet.get("pass_c_reveal", {})
    n_sent = 40 if max_sentences is None else int(max_sentences)

    others = reveal.get("radway_other_plausible_ids") or reveal.get("radway_other_plausible") or []
    if isinstance(others, list):
        others_s = ", ".join(str(x) for x in others) if others else "(none)"
    else:
        others_s = str(others) if others else "(none)"
    stage11 = reveal.get("stage11_codes") or []
    if isinstance(stage11, list):
        stage11_s = ", ".join(str(x) for x in stage11) if stage11 else "(none)"
    else:
        stage11_s = str(stage11) if stage11 else "(none)"

    fmt = {
        "topic_id": packet["topic_id"],
        "main": reps["main"],
        "keybert": reps["keybert"],
        "pos": reps["pos"],
        "mmr": reps["mmr"],
        "sentences_block": format_sentences_block(
            packet, show_position=show_pos, max_sentences=n_sent
        ),
        "lexical_consensus": lexical_consensus or "(pending)",
        "contextual_dominant": contextual_dominant or "(pending)",
        "taxonomy_id": reveal.get("taxonomy_main_id", "(hidden)"),
        "taxonomy_name": reveal.get("taxonomy_main_name", "(hidden)"),
        "secondary_id": reveal.get("taxonomy_secondary_id", "(none)"),
        "secondary_name": reveal.get("taxonomy_secondary_name", "(none)"),
        "radway_main_id": reveal.get("radway_main_id", "(none)"),
        "radway_main_name": reveal.get("radway_main_name", "(none)"),
        "radway_secondary_id": reveal.get("radway_secondary_id", "(none)"),
        "radway_other_plausible": others_s,
        "stage11_codes": stage11_s,
    }

    pass_key = f"pass_{pass_name.lower()}"
    user_template = block[pass_key]
    return {
        "system": block["system"].strip(),
        "user": user_template.format(**fmt).strip(),
        "hypothesis": str(prompt.get("hypothesis")),
        "phrasing": phrasing,
        "pass": pass_name.upper(),
        "prompt_version": str(prompt.get("version")),
    }


def list_code_ids(prompt: Mapping[str, Any]) -> Sequence[str]:
    return [str(c["id"]) for c in prompt.get("codes", []) if "id" in c]
