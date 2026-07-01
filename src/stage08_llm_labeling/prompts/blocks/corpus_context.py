CORPUS_CONTEXT = """
CORPUS CONTEXT (IMPORTANT)

You are labeling topics from a large English romance-novel corpus (2000–2017):
contemporary, paranormal, historical, young-adult, and mystery subgenres.
This is NOT a billionaire-only or CEO-romance subset.
Topics may reflect discourse patterns (how things are said), subgenre markers,
procedural transitions, or preprocessing artefacts — not only romantic scenes.
""".strip()

EVIDENCE_HIERARCHY = """
EVIDENCE HIERARCHY (highest → lowest weight)

1. REPRESENTATIVE SNIPPETS — primary evidence; define the shared narrative thread
2. KeyBERT keywords — salient distilled terms
3. MMR keywords — diverse salient terms
4. POS keywords — content-word (noun/verb/adj) terms
5. ALL KEYWORDS union (KeyBERT + MMR + POS; Main excluded)
6. Main representation — lowest weight; often high-frequency glue or character names

When Main conflicts with snippets or higher-priority representations, trust snippets first.
Do not label from Main alone when snippets show a coherent different theme.
""".strip()

STAGE07_EMPHASIZE = """
STAGE07 HINTS (IMPORTANT): Post-hoc flags are often correct for publisher_boilerplate topics,
but may false-positive on real scenes. Override only when snippets clearly contradict the flag;
cite evidence in rationale.
""".strip()
