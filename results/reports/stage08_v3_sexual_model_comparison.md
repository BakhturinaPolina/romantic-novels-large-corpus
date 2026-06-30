# Stage08 v3 sexual-topic model comparison

Gold reference: `configs/stage08_v3_sexual_subset_gold.yaml` (28 topics).
Prompt: `v3_sexual_precision` | temp 0.0 | max_tokens 256

## Summary

| model | status | topics | fn_agreement | axis_agreement | cliches | overall_pass |
| --- | --- | --- | --- | --- | --- | --- |
| claude-sonnet-4.6 | ok | 28 | 46.4% | 67.9% | 1.0 | False |
| lumimaid-70b | missing | 0 | None | None | nan | None |
| grok-4.20 | ok | 28 | 35.7% | 64.3% | 0.0 | False |
| dolphin-24b-venice-free | ok | 4 | 0.0% | 0.0% | 0.0 | False |

## Issues by model

- **claude-sonnet-4.6** topic 1: `Gentle Kiss With Hesitation` — label overlap 0.11 vs gold 'Tender Kissing With Possible Sexual Escalation'
- **claude-sonnet-4.6** topic 2: `Close Whisper With Neck Touch` — sexual_function: expected sexual_tension, got presex_escalation; axis_hint: expected sexual_tension_explicit_intimacy, got everyday_intimacy_emotional_safety; label overlap 0.00 vs gold 'Charged Physical Nearness Before a Kiss'
- **claude-sonnet-4.6** topic 7: `Playful Wink and Smirk` — sexual_function: expected nonsexual_affection, got none; label overlap 0.14 vs gold 'Flirtatious Smile or Wink'
- **claude-sonnet-4.6** topic 26: `Maneuvering Bodies on The Bed` — label overlap 0.09 vs gold 'Suggestive Bed Positioning or Pre-Intimacy Movement'
- **claude-sonnet-4.6** topic 40: `Hotel Room Suggestion` — label overlap 0.00 vs gold 'Negotiating Private Lodging With Sexual Subtext'
- **claude-sonnet-4.6** topic 56: `Post-Sex and Embrace` — MANUAL_REVIEW: snippet-dependent topic
- **claude-sonnet-4.6** topic 66: `Complimenting Her Appearance` — sexual_function: expected sexual_tension, got nonsexual_affection; label overlap 0.00 vs gold 'Verbal Physical Admiration / Attraction'
- **claude-sonnet-4.6** topic 70: `Threat Against Unwanted Touch` — coercion_watchlist without boundary_risk keywords
- **claude-sonnet-4.6** topic 72: `Hesitant Step Closer` — sexual_function: expected nonsexual_affection, got none; label overlap 0.00 vs gold 'Cautious Romantic Approach'
- **claude-sonnet-4.6** topic 78: `Fumbling With Clothes Outdoors` — label overlap 0.00 vs gold 'Undressing and Clothing Fastenings in Sexual Tension'
- **claude-sonnet-4.6** topic 84: `Hair Touched During Flirtation` — sexual_function: expected nonsexual_affection, got presex_escalation; axis_hint: expected everyday_intimacy_emotional_safety, got sexual_tension_explicit_intimacy; label overlap 0.11 vs gold 'Flirtatious Hair Touching and Physical Charge'
- **claude-sonnet-4.6** topic 108: `Towel-Clad Man After Shower` — label overlap 0.10 vs gold 'Post-Shower Body Display / Bathroom Intimacy'
- **claude-sonnet-4.6** topic 118: `Forceful Pounding Into Mattress` — axis_hint: expected consent_control_risk, got sexual_tension_explicit_intimacy; consent_status: expected unclear_from_topic, got consensual_implied; label overlap 0.12 vs gold 'Forceful Sexual Positioning in Bed'; MANUAL_REVIEW: snippet-dependent topic
- **claude-sonnet-4.6** topic 123: `Spontaneous Reassuring Hug` — label overlap 0.33 vs gold 'Reassuring Hug or Comfort Touch'
- **claude-sonnet-4.6** topic 138: `Condom Availability Discussion` — label overlap 0.12 vs gold 'Condom and Lube Preparation Before Sex'
- **claude-sonnet-4.6** topic 140: `Agreeing to Stop When Asked` — sexual_function: expected sexual_negotiation, got consent_boundary; axis_hint: expected consent_control_risk, got everyday_intimacy_emotional_safety
- **claude-sonnet-4.6** topic 152: `Struck By Someone's Appearance` — sexual_function: expected sexual_tension, got none; axis_hint: expected sexual_tension_explicit_intimacy, got everyday_intimacy_emotional_safety; label overlap 0.00 vs gold 'Visual Attraction to a Stranger'
- **claude-sonnet-4.6** topic 161: `Claiming Her Mouth Impulsively` — sexual_function: expected sexual_tension, got nonsexual_affection; axis_hint: expected sexual_tension_explicit_intimacy, got everyday_intimacy_emotional_safety; label overlap 0.00 vs gold 'Urgent or Possessive Kissing'; Genre cliché label phrase: 'claiming her mouth'
- **claude-sonnet-4.6** topic 174: `Playful Suggestive Banter` — label overlap 0.25 vs gold 'Playful Sexual Innuendo and Body-Size Banter'
- **claude-sonnet-4.6** topic 210: `Choosing Sex Without Love` — label overlap 0.29 vs gold 'Negotiating Sex Without Emotional Commitment'
- **claude-sonnet-4.6** topic 218: `Sweat-Soaked Physical Exertion` — sexual_function: expected sexual_tension, got none; axis_hint: expected sexual_tension_explicit_intimacy, got everyday_intimacy_emotional_safety
- **claude-sonnet-4.6** topic 248: `Audible Sounds After Sex` — sexual_function: expected sexual_tension, got postsex_aftercare; label overlap 0.00 vs gold 'Overheard Sexual or Ambiguous Noises Through Walls'
- **claude-sonnet-4.6** topic 257: `Flushed Skin From Embarrassment` — sexual_function: expected sexual_tension, got nonsexual_affection; axis_hint: expected sexual_tension_explicit_intimacy, got everyday_intimacy_emotional_safety; label overlap 0.29 vs gold 'Flushed Skin and Embarrassed Arousal'
- **claude-sonnet-4.6** topic 277: `Aroused Erection Straining Against Clothes` — sexual_function: expected explicit_contact, got sexual_tension; label overlap 0.00 vs gold 'Explicit Male Arousal Through Clothing'
- **claude-sonnet-4.6** topic 284: `Eyes Closed Near Climax` — sexual_function: expected orgasm_climax, got presex_escalation; label overlap 0.00 vs gold 'Approaching Orgasm or Overwhelming Sexual Sensation'; MANUAL_REVIEW: snippet-dependent topic
- **claude-sonnet-4.6** topic 292: `Incoherent Mixed Scene Fragments` — sexual_function: expected sexual_tension, got none; axis_hint: expected sexual_tension_explicit_intimacy, got exclude_from_axes; label overlap 0.00 vs gold 'Sexual Longing During Reunion or Separation'
- **claude-sonnet-4.6** topic 303: `Savoring Her Taste` — sexual_function: expected sexual_tension, got postsex_arousal; label overlap 0.11 vs gold 'Sensual Taste Description During Kissing or Intimacy'
- **claude-sonnet-4.6** topic 326: `Goodnight Kiss at The Door` — label overlap 0.22 vs gold 'Goodnight Kiss and Promise to Reconnect'
- **grok-4.20** topic 1: `Tender Temple Kiss` — label overlap 0.12 vs gold 'Tender Kissing With Possible Sexual Escalation'
- **grok-4.20** topic 2: `Forehead Touch and Neck Caress` — sexual_function: expected sexual_tension, got nonsexual_affection; axis_hint: expected sexual_tension_explicit_intimacy, got everyday_intimacy_emotional_safety; label overlap 0.00 vs gold 'Charged Physical Nearness Before a Kiss'
- **grok-4.20** topic 7: `Winking and Smirking Exchange` — sexual_function: expected nonsexual_affection, got none; label overlap 0.00 vs gold 'Flirtatious Smile or Wink'
- **grok-4.20** topic 26: `Positioning on King-Sized Bed` — label overlap 0.20 vs gold 'Suggestive Bed Positioning or Pre-Intimacy Movement'
- **grok-4.20** topic 40: `Hotel Room Conversation` — sexual_function: expected sexual_tension, got none; axis_hint: expected sexual_tension_explicit_intimacy, got everyday_intimacy_emotional_safety; label overlap 0.00 vs gold 'Negotiating Private Lodging With Sexual Subtext'
- **grok-4.20** topic 56: `Cock Recovery After Sex` — sexual_function: expected postsex_arousal, got explicit_contact; label overlap 0.10 vs gold 'Explicit Sexual Contact and Post-Sex Arousal'; MANUAL_REVIEW: snippet-dependent topic
- **grok-4.20** topic 66: `Compliments on Beauty` — axis_hint: expected everyday_intimacy_emotional_safety, got sexual_tension_explicit_intimacy; label overlap 0.00 vs gold 'Verbal Physical Admiration / Attraction'
- **grok-4.20** topic 70: `Threatening Touch Warning` — sexual_function: expected consent_boundary, got sexual_tension; consent_status: expected coercion_watchlist, got unclear_from_topic; label overlap 0.14 vs gold 'Protective Threat Around Unwanted Touch'
- **grok-4.20** topic 72: `Anxious Step Closer` — sexual_function: expected nonsexual_affection, got none; label overlap 0.00 vs gold 'Cautious Romantic Approach'
- **grok-4.20** topic 78: `Fumbling With Zippers and Buttons` — label overlap 0.09 vs gold 'Undressing and Clothing Fastenings in Sexual Tension'
- **grok-4.20** topic 84: `Hair Twirling and Pulling` — sexual_function: expected nonsexual_affection, got presex_escalation; axis_hint: expected everyday_intimacy_emotional_safety, got sexual_tension_explicit_intimacy; label overlap 0.25 vs gold 'Flirtatious Hair Touching and Physical Charge'
- **grok-4.20** topic 108: `Towel After Shower` — sexual_function: expected presex_escalation, got none; axis_hint: expected sexual_tension_explicit_intimacy, got everyday_intimacy_emotional_safety; label overlap 0.12 vs gold 'Post-Shower Body Display / Bathroom Intimacy'
- **grok-4.20** topic 118: `Pounding Into Plush Mattress` — axis_hint: expected consent_control_risk, got sexual_tension_explicit_intimacy; consent_status: expected unclear_from_topic, got consensual_implied; label overlap 0.00 vs gold 'Forceful Sexual Positioning in Bed'; MANUAL_REVIEW: snippet-dependent topic
- **grok-4.20** topic 123: `Reassuring Brief Hug` — label overlap 0.33 vs gold 'Reassuring Hug or Comfort Touch'
- **grok-4.20** topic 138: `Condom Purchase Discussion` — label overlap 0.12 vs gold 'Condom and Lube Preparation Before Sex'
- **grok-4.20** topic 140: `Consent and Stopping Agreement` — sexual_function: expected sexual_negotiation, got none; axis_hint: expected consent_control_risk, got everyday_intimacy_emotional_safety; label overlap 0.00 vs gold 'Negotiating When to Stop'
- **grok-4.20** topic 152: `Stunning Visual Admiration` — sexual_function: expected sexual_tension, got none; axis_hint: expected sexual_tension_explicit_intimacy, got everyday_intimacy_emotional_safety; label overlap 0.14 vs gold 'Visual Attraction to a Stranger'
- **grok-4.20** topic 161: `Claiming Her Plump Mouth` — sexual_function: expected sexual_tension, got presex_escalation; label overlap 0.00 vs gold 'Urgent or Possessive Kissing'
- **grok-4.20** topic 174: `Playful Spanking Threat` — sexual_function: expected sexual_tension, got presex_escalation; label overlap 0.11 vs gold 'Playful Sexual Innuendo and Body-Size Banter'
- **grok-4.20** topic 218: `Sweat Soaked Skin` — sexual_function: expected sexual_tension, got none; axis_hint: expected sexual_tension_explicit_intimacy, got everyday_intimacy_emotional_safety; label overlap 0.11 vs gold 'Sweat, Heat, and Physical Arousal or Exertion'
- **grok-4.20** topic 248: `Muffled Noises During Sex` — sexual_function: expected sexual_tension, got presex_escalation; label overlap 0.10 vs gold 'Overheard Sexual or Ambiguous Noises Through Walls'
- **grok-4.20** topic 257: `Flushed Skin From Embarrassment` — sexual_function: expected sexual_tension, got none; axis_hint: expected sexual_tension_explicit_intimacy, got everyday_intimacy_emotional_safety; label overlap 0.29 vs gold 'Flushed Skin and Embarrassed Arousal'
- **grok-4.20** topic 277: `Straining Erection in Pants` — sexual_function: expected explicit_contact, got presex_escalation; label overlap 0.00 vs gold 'Explicit Male Arousal Through Clothing'
- **grok-4.20** topic 284: `Eyes Closed in Anticipation` — sexual_function: expected orgasm_climax, got presex_escalation; label overlap 0.00 vs gold 'Approaching Orgasm or Overwhelming Sexual Sensation'; MANUAL_REVIEW: snippet-dependent topic
- **grok-4.20** topic 292: `Frantic Hesitation Before Sex` — sexual_function: expected sexual_tension, got presex_escalation; label overlap 0.00 vs gold 'Sexual Longing During Reunion or Separation'
- **grok-4.20** topic 303: `Tasting and Flavor Compliments` — label overlap 0.00 vs gold 'Sensual Taste Description During Kissing or Intimacy'
- **grok-4.20** topic 326: `Goodnight Kiss at Door` — label overlap 0.25 vs gold 'Goodnight Kiss and Promise to Reconnect'
- **dolphin-24b-venice-free** topic 1: `plump` — sexual_function: expected nonsexual_affection, got None; axis_hint: expected everyday_intimacy_emotional_safety, got None; label overlap 0.00 vs gold 'Tender Kissing With Possible Sexual Escalation'
- **dolphin-24b-venice-free** topic 2: `moves` — sexual_function: expected sexual_tension, got None; axis_hint: expected sexual_tension_explicit_intimacy, got None; label overlap 0.00 vs gold 'Charged Physical Nearness Before a Kiss'
- **dolphin-24b-venice-free** topic 7: `smirk` — sexual_function: expected nonsexual_affection, got None; axis_hint: expected everyday_intimacy_emotional_safety, got None; label overlap 0.00 vs gold 'Flirtatious Smile or Wink'
- **dolphin-24b-venice-free** topic 26: `sized` — sexual_function: expected presex_escalation, got None; axis_hint: expected sexual_tension_explicit_intimacy, got None; label overlap 0.00 vs gold 'Suggestive Bed Positioning or Pre-Intimacy Movement'
- **dolphin-24b-venice-free** topic 40: `nan` — topic not in labels JSON
- **dolphin-24b-venice-free** topic 56: `nan` — topic not in labels JSON
- **dolphin-24b-venice-free** topic 66: `nan` — topic not in labels JSON
- **dolphin-24b-venice-free** topic 70: `nan` — topic not in labels JSON
- **dolphin-24b-venice-free** topic 72: `nan` — topic not in labels JSON
- **dolphin-24b-venice-free** topic 78: `nan` — topic not in labels JSON
- **dolphin-24b-venice-free** topic 84: `nan` — topic not in labels JSON
- **dolphin-24b-venice-free** topic 108: `nan` — topic not in labels JSON
- **dolphin-24b-venice-free** topic 118: `nan` — topic not in labels JSON
- **dolphin-24b-venice-free** topic 123: `nan` — topic not in labels JSON
- **dolphin-24b-venice-free** topic 138: `nan` — topic not in labels JSON
- **dolphin-24b-venice-free** topic 140: `nan` — topic not in labels JSON
- **dolphin-24b-venice-free** topic 152: `nan` — topic not in labels JSON
- **dolphin-24b-venice-free** topic 161: `nan` — topic not in labels JSON
- **dolphin-24b-venice-free** topic 174: `nan` — topic not in labels JSON
- **dolphin-24b-venice-free** topic 210: `nan` — topic not in labels JSON
- **dolphin-24b-venice-free** topic 218: `nan` — topic not in labels JSON
- **dolphin-24b-venice-free** topic 248: `nan` — topic not in labels JSON
- **dolphin-24b-venice-free** topic 257: `nan` — topic not in labels JSON
- **dolphin-24b-venice-free** topic 277: `nan` — topic not in labels JSON
- **dolphin-24b-venice-free** topic 284: `nan` — topic not in labels JSON
- **dolphin-24b-venice-free** topic 292: `nan` — topic not in labels JSON
- **dolphin-24b-venice-free** topic 303: `nan` — topic not in labels JSON
- **dolphin-24b-venice-free** topic 326: `nan` — topic not in labels JSON
