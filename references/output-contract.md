# Output Contract

Always return two artifacts:

1. `Analysis Report`
2. `Study Report`

## 1. Route Decision

Open with:

- chosen route
- confidence
- one short reason tied to visible evidence and the user's goal

If the image is a single frame, render, or cropped detail, note that limitation early.

## 2. Analysis Report

Start with a short digest, then expand.

Recommended structure:

- `Quick Read`: 3-5 concise findings
- `Detailed Analysis`: use the route-specific dimensions from the chosen method file
- `Overall Judgment`: what works, what weakens the image, and what the image is trying to do

Rules:

- Tie every important claim to visible evidence.
- Prefer plain language over theory names unless the theory genuinely improves clarity.
- If the user asked for comparison, explicitly separate shared traits from differences.
- If the route confidence is not high, keep the judgment proportional.

### Photography minimums

When the chosen route is `photography`, the detailed section should cover these blocks when the evidence allows:

- forensics and medium
- scene slicing or foreground/midground/background read
- geometry or optics read
- lighting read
- color/material/processing read
- emotion/context read

Separate direct facts from stronger and weaker inferences instead of blending them into one certainty tone.

### Graphic design minimums

When the chosen route is `graphic-design`, the detailed section should cover these blocks when the evidence allows:

- task and format
- message slicing
- hierarchy
- structure or grid
- typography
- color/asset treatment/brand fit
- persuasion or usability logic

### Painting and illustration minimums

When the chosen route is `painting-illustration`, the detailed section should cover these blocks when the evidence allows:

- medium read
- descriptive inventory
- formal language
- spatial or compositional logic
- symbol/culture/meaning read
- medium or process control

### Interior design minimums

When the chosen route is `interior-design`, the detailed section should cover these blocks when the evidence allows:

- room type and program
- zoning or circulation
- form or envelope read
- lighting read
- material/furniture/palette read
- usability or lived-reality read

### Architecture and urban minimums

When the chosen route is `architecture-urban`, the detailed section should cover these blocks when the evidence allows:

- building or place type
- site/context read
- massing or silhouette
- facade/opening logic
- ground plane/public realm
- material/light/environmental response

### Infographic and diagram minimums

When the chosen route is `infographic-diagram`, the detailed section should cover these blocks when the evidence allows:

- format and information task
- message or claim slicing
- structural readability
- data/logic integrity cues
- labeling/annotation
- interpretation risk

### Product and industrial design minimums

When the chosen route is `product-industrial-design`, the detailed section should cover these blocks when the evidence allows:

- object type and use scenario
- form slicing
- affordance or function logic
- ergonomics or use sequence
- detail/manufacturing logic
- material/color/finish read

### Comics and sequential minimums

When the chosen route is `comics-sequential`, the detailed section should cover these blocks when the evidence allows:

- page or sequence type
- panel or beat slicing
- reading order
- staging and acting
- text-image coordination
- pacing or payoff

### Fashion and styling minimums

When the chosen route is `fashion-styling`, the detailed section should cover these blocks when the evidence allows:

- look type or styling context
- silhouette or layering read
- garment/material/accessory read
- body/styling balance
- persona/brand/social signal
- wearability or styling logic

### Sculpture, installation, and craft minimums

When the chosen route is `sculpture-installation-craft`, the detailed section should cover these blocks when the evidence allows:

- work type and scale context
- volume or part slicing
- material/join/assembly read
- viewing path or site relation
- presence/meaning/ritual read
- craft-resolution read

### Game visual design minimums

When the chosen route is `game-visual-design`, the detailed section should cover these blocks when the evidence allows:

- image type and gameplay context
- scene/ui/HUD slicing
- readability and navigation cues
- environment/character/interaction clarity
- art direction vs play function
- player interpretation risk

### Scientific and medical imaging minimums

When the chosen route is `scientific-medical-imaging`, the detailed section should cover these blocks when the evidence allows:

- image/evidence type
- signal and annotation read
- clarity or artifact risk
- interpretability limits
- communication adequacy for the likely audience

Avoid pretending to provide professional diagnosis. Keep the analysis on visible evidence, labeling, and interpretability unless the user has separately provided domain context.

### Typography and lettering minimums

When the chosen route is `typography-lettering`, the detailed section should cover these blocks when the evidence allows:

- type artifact or use case
- letterform construction
- spacing/rhythm/texture
- voice or stylistic register
- legibility and performance at likely size
- system consistency if multiple samples exist

### Presentation and document minimums

When the chosen route is `presentation-document`, the detailed section should cover these blocks when the evidence allows:

- page or slide role
- argument/message slicing
- hierarchy and scan path
- chart/table/callout support quality
- page-sequence coherence if multiple pages exist
- decision-support clarity

### Film frame minimums

When the chosen route is `film-frame`, the detailed section should cover these blocks when the evidence allows:

- frame limits
- shot or camera read
- blocking or composition
- light/color/texture
- dramatic function or genre pressure

### Generic mixed minimums

When the chosen route is `generic-mixed`, the detailed section should cover these blocks:

- top route and runner-up route
- universal four-step read
- what extra context would sharpen the route

### Universal fallback minimums

When the chosen route is `universal-fallback`, the detailed section should cover these blocks:

- what kind of visual artifact this seems to be
- what visible layers or zones it contains
- how attention is organized
- what it appears to communicate, do, or evidence
- where uncertainty is high
- which named route would become useful if more context arrived

## 3. Study Report

Convert the critique into a learning plan.

Include:

- `What to Learn Now`: 2-4 concepts or habits
- `Practice Drills`: 2-3 concrete exercises
- `What to Watch For Next Time`: repeated failure modes or blind spots
- `Suggested Comparisons`: optional; mention only when the image clearly points toward a useful reference direction

The study report should help the user do something next, not just understand the critique.

## Batch rules

- For a same-series batch, include set-level consistency.
- For before/after or versioned work, explain exactly what changed.
- For mixed batches, segment the report by subgroup instead of flattening everything.
