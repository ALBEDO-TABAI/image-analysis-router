# Batch Handling

Use this file only when the input contains multiple images or the script returns a non-`single` `batch_type`.

Batch handling decides grouping and comparison shape. Route-specific analysis still comes from the relevant `method-*.md` files.

## Batch types

### `same_series`

Use when images share one subject, route, author, campaign, project, or visual system.

- Analyze the strongest and weakest individual examples.
- Then judge consistency, range, and drift.
- Do not repeat a full route report for every image unless the user asks.

### `versioned`

Use for before/after, v1/v2, old/new, or revision comparisons.

- Name the baseline.
- Name the revision.
- Focus on deltas: improved, regressed, unchanged, and still blocked.
- Avoid generic critique that could apply to either version.

### `reference_pack`

Use for mood boards, inspiration boards, reference sets, and loose visual collections.

- Extract repeated signals: composition, palette, material, pacing, mood, or interaction logic.
- Suppress single-image depth unless one image is clearly the anchor.
- End with what the user can borrow and what should not be copied.

### `subject_vs_reference`

Use when one image is the work being evaluated and the rest are anchors.

- Identify the subject image first.
- Use reference images as comparison anchors only.
- Do not critique the reference pack as if it were the user's work.
- If subject and reference roles are unclear, ask before analyzing.

### `mixed_domain`

Use when the batch has multiple stable subroutes.

- Split images into route-specific groups.
- Analyze each group with its own method file.
- Close with why these images may have been placed together and where the set is incoherent.

### `unknown`

Use when the script cannot see image count or roles.

- Let visual inspection determine the real batch type.
- If the visual evidence still cannot establish roles, ask one clarifying question.

## Size rules

- 2 images: use a compact A/B difference read.
- 3-5 images: use standard grouped batch output.
- More than 5 images: group first, keep groups to five or fewer, then analyze representative examples.

## Output shape

For `same_series`, `reference_pack`, and `mixed_domain`, use:

```markdown
## Batch Report

### Batch Map
- Type:
- Groups:
- Main comparison axis:

### Group A: <route> (<image names>)
#### Analysis Report
#### Study Report

### Group B: <route> (<image names>)
#### Analysis Report
#### Study Report

### Cross-batch synthesis
```

For `versioned` or 2-image batches, use:

```markdown
## A/B Report

### Baseline
### Revision or comparison image
### What changed
### What improved
### What regressed
### What to do next
```
