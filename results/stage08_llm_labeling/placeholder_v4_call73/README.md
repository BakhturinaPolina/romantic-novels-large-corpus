# Stage08 labeling outputs — call 73 (placeholder v4)

Label JSONs for frozen call 73, grouped by experiment type.

| Folder | Contents |
|--------|----------|
| [`production/`](production/) | Full-corpus `v3_topic_labeling` labels |
| [`snippet_trap/`](snippet_trap/) | 79-topic `v3_rep_first` panel relabel + comparison CSV |
| [`gold_regression/`](gold_regression/) | Gold-30 regression labels + validation CSV reports |
| [`sexual_precision/`](sexual_precision/) | Sexual-subset validation across models |
| [`model_sweep/`](model_sweep/) | Early model/prompt pilots (`limit5`, `limit20`, sweep scores) |
| [`legacy_v2/`](legacy_v2/) | Pre-v3 prompt experiments (`v2_c8`, `v2_s1`, base romance_aware) |
| [`stage09_input/`](stage09_input/) | Slim + enriched topic metadata for Stage09 taxonomy mapping |

Historical v2 OVAT sweeps: [`../prompt_sweeps/call73/`](../prompt_sweeps/call73/)

## Production

- **Main labels:** `production/labels_pos_*_v3_topic_labeling.json`

## Snippet-trap panel

See [`snippet_trap/README.md`](snippet_trap/README.md).

## Stage09

See [`stage09_input/README.md`](stage09_input/README.md).
