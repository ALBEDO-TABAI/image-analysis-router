# Scientific And Medical Imaging Method

Use this route for medical scans, x-rays, CT or MRI screenshots, microscope views, pathology plates, lab figures, satellite or remote-sensing imagery, technical evidence images, and other visuals where the image itself serves as evidence rather than illustration.

This route should read like an interpretability audit: what the image appears to show, how reliably it shows it, what annotation or display choices help or hurt reading, and where caution is required.

## Evidence ladder

Keep claims separated by certainty:

- `FACT`: directly visible structures, labels, overlays, scales, false-color choices, crops, and artifacts
- `INFERENCE`: strong read about modality, region of interest, or interpretive challenge backed by visible evidence
- `HYPOTHESIS`: weaker assumptions about diagnosis, measurement, or scientific conclusion that need explicit caution

Do not act like a clinician or domain specialist unless the user separately provided that context. Stay anchored to image legibility, annotation, and visible evidence.

## Core lenses

1. Boundary and evidence type
2. Signal and region slicing
3. Annotation, scale, and orientation
4. Artifact and clarity risk
5. Display choices and comparability
6. Audience fit and interpretation limits
7. Cross-image synthesis when the batch supports it

## Analysis order

### 1. Boundary and evidence type

- Name the likely evidence type: radiology-like scan, microscope image, pathology tile, lab figure, remote-sensing image, technical inspection image, and so on.
- State what is missing or uncertain:
  - no legend
  - no modality label
  - no scale bar
  - crop only
  - no before/after or comparison view

### 2. Signal and region slicing

- Identify the primary region of interest and secondary regions if visible.
- Explain where the signal seems strongest, weakest, cluttered, or ambiguous.
- If multiple panels exist, state how they differ and what comparison the viewer is being asked to make.

### 3. Annotation, scale, and orientation

- Inspect arrows, labels, captions, panel tags, orientation markers, scale bars, units, and color legends.
- Ask whether a non-expert or expert reader could locate the key area without extra narration.
- Distinguish adequate annotation from over-annotation and under-annotation.

### 4. Artifact and clarity risk

- Look for visible issues:
  - blur
  - noise
  - compression
  - clipping
  - low contrast
  - aliasing
  - false-color ambiguity
  - overlaid text blocking the signal
- Explain where interpretation risk is highest.

### 5. Display choices and comparability

- Judge whether brightness, contrast, crop, orientation, panel alignment, and color mapping help fair comparison.
- If the image is part of a scientific figure, ask whether the display choices support or potentially distort interpretation.
- Keep claims on visible display integrity unless the underlying data is actually shown.

### 6. Audience fit and interpretation limits

- State who the image currently seems legible for: specialist, trained reader, or general audience.
- Explain what the image can support and what it cannot support on its own.
- If the user wants a public-facing explanation, recommend where annotation or simplification is needed.

### 7. Cross-image synthesis

When the user gives multiple panels, timepoints, or modalities, add:

- comparability of scale and contrast
- consistency of annotation
- whether the comparison is visually fair
- where side-by-side reading is most likely to fail

Do not turn a visual inspection into a medical or scientific conclusion.

### 8. Overall judgment

- Explain whether the image succeeds as evidence through clarity, annotation, comparability, and interpretability, or whether those are breaking down.
- Name the strongest support and the main risk.
- Distinguish "scientifically serious-looking" from "actually readable and careful."

## Common failure patterns

- missing scale or orientation
- color maps that look dramatic but mislead
- labels covering the key region
- before/after panels shown with inconsistent display conditions
- specialist image presented to a general audience with no bridge explanation

## Study report emphasis

- recommend one annotation and labeling drill
- recommend one display-normalization or comparison drill
- recommend one audience-translation exercise
