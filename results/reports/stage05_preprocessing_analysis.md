# Stage05 Preprocessing Gap Analysis

## Summary

Topic quality issues in the new pipeline (empty representations, character names appearing, non-English text clusters) stem from **missing preprocessing steps** that existed in legacy code.

## Comparison: Legacy vs. New Preprocessing

### 1. Text Cleaning

| Step | Legacy (`retrain_models.py`) | New (`data_io.py`) | New (`compare_fit.py`) |
|------|------------------------------|---------------------|------------------------|
| Newline removal | ✅ `\n` → ` ` | ✅ `\n` → ` ` | N/A (uses corpus store) |
| Whitespace normalization | ✅ `\s+` → ` ` | ✅ split/join | N/A |
| Lowercase | ✅ `.lower()` | ✅ `.lower()` | N/A |
| **Mojibake fix** | ✅ `â€™` → `'` etc. | ❌ Missing | ❌ Missing |
| **Unicode normalization** | ✅ NFKD decomposition | ❌ Missing | ❌ Missing |

### 2. Stopwords / Character Names

| Step | Legacy (`retrain_models.py`) | New (`compare_fit.py`) |
|------|------------------------------|------------------------|
| English stopwords | ✅ sklearn ENGLISH_STOP_WORDS | ✅ sklearn ENGLISH_STOP_WORDS |
| Custom stoplist file | ✅ Loaded from `custom_stoplist.txt` | ✅ Loaded from config |
| **Character name preprocessing** | ✅ `preprocess_character_name()` (removes prefixes, extracts tokens) | ❌ Simple regex only |

### 3. CountVectorizer Settings

| Parameter | Legacy (`retrain_models.py`) | New (`compare_fit.py`) | Impact |
|-----------|------------------------------|------------------------|--------|
| `stop_words` | English + custom (preprocessed names) | English + custom (raw tokens) | Character names may slip through |
| `min_df` | Varies by HP tuning | **Proportional (0.008-0.015)** | **Empty representations for small clusters** |
| `token_pattern` | `r'(?u)\b[a-zA-Z]{2,}\b'` (2+ alpha only) | **Default** (`\w\w+`) | Single chars, numbers, symbols in topics |

### 4. Topic Word Post-Processing

| Step | Legacy | New |
|------|--------|-----|
| Filter by gensim Dictionary | ✅ Yes | ✅ Yes |
| Remove "mr"/"ms" | ✅ Yes | ✅ Yes |
| **Pad topics to equal length** | ✅ Yes | ❌ Missing |

## Root Causes of Observed Issues

### Issue 1: Empty Topic Representations
**Cause:** `min_df` as proportion (0.008 = 4000 docs minimum on 500K sample) filters all words in small clusters (150-400 docs).
**Fix:** Override `min_df` to absolute value (5-10 docs).

### Issue 2: Character Names in Topics
**Cause:** New code doesn't use `preprocess_character_name()` to parse multi-word entries like "A Alex" → "alex".
**Fix:** Port legacy character name preprocessing to `load_custom_stopwords_from_config`.

### Issue 3: Non-English Clusters (French, Spanish, Chinese, Arabic)
**Cause:** Non-English books included in corpus.
**Fix:** Detect and filter non-English books before corpus creation (v3 dataset).

### Issue 4: Garbage Tokens (single chars, numbers, special patterns)
**Cause:** Missing `token_pattern = r'(?u)\b[a-zA-Z]{2,}\b'` in CountVectorizer.
**Fix:** Add explicit token_pattern to CountVectorizer configuration.

## Recommendations

1. **Immediate fix** (already done): Override `min_df` to absolute value in `compare_fit.py`
2. **Short-term**: Port legacy preprocessing to new pipeline
3. **Medium-term**: Create v3 corpus excluding non-English books
4. **Long-term**: Add language detection to Stage 01 sentence extraction
