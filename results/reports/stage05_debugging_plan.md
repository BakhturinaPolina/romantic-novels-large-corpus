# Stage05 Topic Quality Debugging Plan

## Current Status

After analyzing legacy vs. new code preprocessing, three key issues were identified:

1. **Empty topic representations** - Fixed by overriding `min_df` to absolute value (5)
2. **Garbage tokens** - Fixed by adding `token_pattern = r"(?u)\b[a-zA-Z]{2,}\b"`
3. **Non-English books** - Requires corpus filtering (v3 dataset)

## Debugging Steps

### Step 1: Verify Fixes with Single Model Test

```bash
# Delete one existing call to force re-run with fixes
rm -rf results/experiments/stratified_minilm12v2_seed42_v2/final_compare/call_59

# Re-run that call with updated code
python -m src.stage05_final_fit.cli compare \
  --trials results/experiments/stratified_minilm12v2_seed42_v2/trials_partial.csv \
  --bo-calls 59 \
  --run-id stratified_minilm12v2_seed42_v2
```

**Expected logs:**
- `Overriding min_df from 0.0149 (proportional) to 5 (absolute)`
- `Set token_pattern to enforce 2+ char alphabetic tokens only`
- `Post-fit snapshot: N topics (excl. outliers), outlier docs=...`
- No `DIAGNOSTIC: N topics have empty representations` warning
- Topic word lists with actual words (not empty strings)

### Step 2: Check Output Quality

After the test run:

```bash
# Check topic_info.csv for non-empty representations
head -20 results/experiments/stratified_minilm12v2_seed42_v2/final_compare/call_59/topic_info.csv

# Check top_words.csv for meaningful words
head -50 results/experiments/stratified_minilm12v2_seed42_v2/final_compare/call_59/top_words.csv

# Check metrics.json
cat results/experiments/stratified_minilm12v2_seed42_v2/final_compare/call_59/metrics.json
```

**Quality checklist:**
- [ ] All topics have words in Representation column (no `['', '', '', ...]`)
- [ ] No single-character tokens in top words
- [ ] No number-only tokens
- [ ] No mojibake artifacts (â€™, etc.)
- [ ] Character names from stoplist are filtered

### Step 3: Analyze Non-English Content

```bash
# Install langdetect if needed
pip install langdetect

# Run language analysis on train split
python scripts/detect_non_english_books.py --analyze --split train

# Expected output: language distribution report
# Look for: French (fr), Spanish (es), Portuguese (pt), Chinese (zh-cn), Arabic (ar)
```

### Step 4: Create v3 Filtered Corpus (if non-English books found)

```bash
# Create v3 splits excluding non-English books
python scripts/detect_non_english_books.py --create-v3 --min-confidence 0.6

# Outputs:
# - data/raw/romance_subdataset_filtered_v3/sentences_{train,val,test}.csv
# - data/raw/romance_subdataset_filtered_v3/v3_filtering_manifest.json
# - data/raw/romance_subdataset_filtered_v3/language_analysis.csv
```

### Step 5: Rebuild Corpus and Re-tune (if v3 created)

With v3 corpus, rebuild the full pipeline:

1. Update `configs/paths_stage03_fit.yaml` to point to v3 sentence CSVs
2. Re-run stratified sampling: `python -m src.stage03_train.cli sample ...`
3. Re-run BO tuning: `python -m src.stage03_train.cli tune ...`
4. Re-run compare-fit on new top trials

## Early Topic Printing (Already Added)

The `compare_fit.py` now prints diagnostic info after every fit:

```
Post-fit snapshot: 17 topics (excl. outliers), outlier docs=27915 (5.58%)
  Topic 0 (455126 docs): opened, closed, used, leaned, stepped, mr, lifted, miss
  Topic 1 (11208 docs): se, en, la, le, il, el, su, eu
  ...
```

If empty representations are detected:
```
DIAGNOSTIC: 15/17 topics have empty representations: [2, 3, 4, ...]
```

## Code Changes Summary

### `compare_fit.py` changes:

1. **`min_df` override**: Converts proportional (0.01) to absolute (5) 
2. **`token_pattern` override**: Enforces `r"(?u)\b[a-zA-Z]{2,}\b"`
3. **Post-fit diagnostics**: Prints topic counts, warns on empty representations, shows top-5 topics

### Pending improvements (future work):

1. Port legacy `preprocess_character_name()` to `load_custom_stopwords_from_config()`
2. Add mojibake fix and unicode normalization to `clean_sentence()` in `data_io.py`
3. Add language detection to Stage 01 sentence extraction pipeline
