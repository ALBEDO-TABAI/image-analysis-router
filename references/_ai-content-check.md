# AI Content Check

Use this as a cross-route check when the user asks whether an image is AI-generated, the source says it is AI-generated, or visible artifacts make generation relevant to the analysis.

This check does not replace the primary route. It only adjusts certainty, evidence tone, and what kinds of failures to inspect.

## Evidence levels

- `Stated`: the user, file name, metadata, or source says the image is AI-generated.
- `Visible signal`: there are concrete visual artifacts that support an AI-generation hypothesis.
- `No clear signal`: no visible AI-specific evidence; do not mention AI generation unless the user asked.

## Common visible signals

- text that breaks into pseudo-letters or inconsistent glyphs
- hand, finger, face, tooth, or anatomy anomalies
- repeated textures that do not respect object boundaries
- overly smooth or inconsistent reflections
- impossible joins, tangencies, shadows, or contact points
- local object logic that changes across the same item
- background details that dissolve under close reading

## How to write it

- Direct source fact: "The source says this is AI-generated."
- Strong visible signal: "These edge and text artifacts suggest a generated or heavily composited image."
- Weak signal: "This may be generated, but the visible evidence is not enough to state that as fact."

Do not turn this into a forensic verdict. If the route is photography, design, illustration, or product, keep the main critique in that route and use AI signs only where they affect trust, craft, or learning value.
