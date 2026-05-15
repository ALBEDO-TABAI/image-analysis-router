---
name: image-analysis-router
description: Route image-heavy requests into the correct critique workflow, then produce a targeted analysis plus study report. Use when Codex receives one or more images and the user wants structured analysis, style classification, critique, or learning notes for posters, brand graphics, UI screenshots, paintings, illustrations, photographs, interior design photos or renders, building exteriors or urban scenes, infographics or diagrams, product or industrial design images, comics or sequential pages, fashion or styling visuals, sculpture or installation works, game visuals, scientific or medical images, typography-led pieces, presentation/report pages, movie stills, storyboard frames, or mixed visual sets. Trigger on requests such as "分析这张图", "拆一下这组海报", "看看这张摄影作品怎么学", "鉴赏这幅画", "分析这个空间图", "看看这个建筑立面", "拆这个信息图", "分析这个产品外观", "读一下这页漫画", "看看这套穿搭", "分析这个游戏界面", "看看这个医学图", "拆这个字体海报", "帮我看这页PPT", or any case where a generic image summary would be too shallow.
---

# Image Analysis Router

Use this skill when the main challenge is not "describe the image" but "pick the right way to read the image first."

## Expected Input

This skill expects image evidence plus a visual-analysis goal.

- Accept: local image paths, image attachments, screenshots, filenames, OCR hints, source note path, source URLs, and user goal.
- Do not create the FastNote source note here. When called by FastNote, treat `source_note_path` as already owned by FastNote.
- Do not accept raw text-only study material as an image job; that belongs to `study-notes` after extraction.
- `universal-fallback` is a named first-principles route for uncategorizable visuals, not a silent failure fallback.

## Read in order

- Read [references/route-matrix.md](./references/route-matrix.md) first.
- Read [references/output-contract.md](./references/output-contract.md) before drafting the final answer.
- If the script or visual read indicates a batch, read [references/method-batch-handling.md](./references/method-batch-handling.md).
- If the image may be AI-generated or the user asks about generation, read [references/_ai-content-check.md](./references/_ai-content-check.md).
- Read only the route file(s) named in [references/route-matrix.md](./references/route-matrix.md).

## Workflow

1. Gather the user's goal, image count, file names, and any supplied context.
2. If prompt text or file names are available, run:
   - `python3 scripts/route_image_request.py --prompt "<user request>" --file "<name-or-path>" --hint "<ocr-or-caption>"`
   - Windows compatible: `py .\scripts\route_image_request.py ...`
   - Add `--quiet` to suppress route_scores/focus_scores/image_routes when only the decision is needed.
3. Treat the script output as a routing prior, not final truth.
4. Read the script status before route selection:
   - `visual_input_missing`: stop and ask upstream for image evidence.
   - `visual_evidence_insufficient`: do not force a route; state what is readable and what blocks analysis.
   - `needs_clarification`: ask one clarifying question using the script's route and focus options.
   - `ok`: continue.
5. Visually inspect at least one representative image before locking the route. If visual inspection conflicts with the script, follow the image and state the override reason briefly.
6. Pick one primary route per image or subgroup. If the batch is mixed, split it instead of forcing one lens onto everything.
7. State both route and intent confidence:
   - `high`: the dominant route clearly matches both the visual evidence and the user's goal
   - `medium`: one route leads, but a second route is plausible
   - `low`: the image is hybrid, under-specified, or the file is missing enough context
   - If `intent_confidence` is low and the user's goal would change the report, ask one clarifying question before producing the full report.
   - If `route_confidence` is low because all route scores are weak, use `universal-fallback` only when the visual evidence is still readable.
   - If `route_confidence` is low because several strong routes tie, use `generic-mixed` and split the route-specific layers.
8. Load only the method file(s) needed for the chosen route.
9. Follow the script's `response_depth`:
   - `quick`: short answer, no full Study Report unless learning intent is explicit.
   - `standard`: Analysis Report plus brief Study Report.
   - `deep`: full Analysis Report plus full Study Report.

## Routing Override Record

If visual inspection contradicts the script's `top_route`, record the override in the final answer's `处理说明` (only shown when the user asks for it):

```text
route_override:
  from: <script top_route>
  to: <visual route>
  reason: <one sentence tied to visible evidence>
```

If `route_confidence` or `intent_confidence` is `low`, also surface `route_confidence`, `route_runner_up`, and `route_decision` fields in `处理说明`.

## Status Schema

When the script returns a blocking status, return the canonical JSON object below (or the equivalent text block). Do NOT continue to a normal Analysis Report.

```json
{
  "status": "visual_input_missing" | "visual_evidence_insufficient" | "needs_clarification",
  "modality": "image",
  "blocked_step": "route" | "analysis",
  "blocked_reason": "<one sentence>",
  "suggested_action": "<concrete next step for the upstream caller>",
  "clarification_options": {"routes": [...], "focuses": [...]}
}
```

`clarification_options.routes` MUST only contain routes that scored above zero. Empty arrays are valid.

## UI Screenshot Handling

Until a dedicated `ui-product` route exists, route standalone UI screenshots (app screens, web dashboards, settings panels) to `graphic-design` AND emphasize these four extra dimensions in the report:

1. **Information density**: how many things compete for attention; what is foreground vs background.
2. **State clarity**: empty / loading / error / success states; affordance signals.
3. **Interaction cues**: tappable / hoverable / disabled visual differentiation.
4. **Hierarchy resilience**: does the layout still work at smaller widths / accessibility scaling?

Do NOT use `presentation-document` for live UI screens; that route is for slide / report layouts.

## Routing rules

- Prefer `graphic-design` when typography, layout, branding, CTA, hierarchy, packaging, poster logic, or image-text composition is central.
- Prefer `photography` when camera capture, timing, lens behavior, exposure, depth, realism, or documentary truth claims are central.
- Prefer `painting-illustration` when the image reads as painted, drawn, stylized, symbolic, art-historical, or cross-cultural in a way that needs iconography or style analysis.
- Prefer `interior-design` when the image is fundamentally about space, zoning, furniture, materials, atmosphere, lighting, or circulation, regardless of whether it is a photo or render.
- Prefer `architecture-urban` when the image is fundamentally about building massing, facade language, site relationship, public realm, skyline, streetscape, landscape integration, or urban spatial order.
- Prefer `infographic-diagram` when the image is mainly a chart, process diagram, map, flow graphic, system schematic, or information visualization where correctness and readability matter more than visual mood.
- Prefer `product-industrial-design` when the image is mainly about an object, device, furniture piece, tool, packaging structure, prototype, or product render and the core question is form, usability, manufacturability, or material-finish logic.
- Prefer `comics-sequential` when the image is a comic page, manga page, strip, webtoon panel set, picture-book spread, or other sequential storytelling image where panel order and narrative pacing matter.
- Prefer `fashion-styling` when the image is mainly about clothing, silhouette, layering, grooming, accessories, runway/editorial styling, or personal styling rather than camera craft alone.
- Prefer `sculpture-installation-craft` when the image is mainly about a three-dimensional artwork, object ensemble, craft piece, material assembly, or site-specific installation and the core question is volume, material, presence, or viewing path.
- Prefer `game-visual-design` when the image is mainly a game screenshot, HUD/UI overlay, character sheet, environment concept tied to gameplay, or scene where readability and play experience matter alongside style.
- Prefer `scientific-medical-imaging` when the image is mainly diagnostic, scientific, microscopic, radiologic, technical, or evidence-bearing and the core question is interpretability, annotation, or visual validity rather than aesthetic mood.
- Prefer `typography-lettering` when the image is mainly type-driven: lettering, logotypes, calligraphy, type posters, wordmarks, or text-as-form where letter construction and reading texture matter more than general layout.
- Prefer `presentation-document` when the image is mainly a slide, report page, proposal page, dashboard report, or document spread where argument flow and page-to-page communication matter more than poster impact.
- Prefer `film-frame` when the image is a movie still, animation frame, storyboard frame, or a cinematic composition where shot language matters more than poster/layout logic.
- Prefer `generic-mixed` when the image does not cleanly fit the above routes, or when the batch mixes multiple domains that need separate treatment.
- Prefer `universal-fallback` when the image does not match any route strongly enough but still deserves a structured first-principles visual reading. Do not treat it as a failed-analysis fallback.

If one image straddles multiple routes, choose based on what the user is actually trying to learn. Example: a movie poster usually goes to `graphic-design`; the raw frame inside that poster may go to `film-frame` only if the user wants cinematic analysis.

If a building image is mainly being judged as a photograph, `photography` can still win. If the same image is being judged for facade rhythm, site fit, or city effect, prefer `architecture-urban`.

If a product image is mainly an ad or ecommerce layout, `graphic-design` can still win. If the core question is form, ergonomics, or detail logic, prefer `product-industrial-design`.

If none of the named routes fits well, use `universal-fallback` rather than forcing a bad match. This named route should still produce a layered analysis and study report.

Until a dedicated UI product route exists, send standalone interface screenshots to `graphic-design` and emphasize hierarchy, information density, state clarity, and interaction cues.

## Guardrails

- Do not pretend certainty when the route is ambiguous.
- Do not use `universal-fallback` when the image is missing or unreadable; use `visual_input_missing` or `visual_evidence_insufficient`.
- Do not judge paintings with poster or ad-performance standards unless the user explicitly asks for commercial translation.
- Do not treat documentary or journalistic photography as pure aesthetics when ethics, context, or truthfulness are part of the request.
- Do not infer hidden generation workflows for AI art unless visible evidence supports the claim; use `_ai-content-check.md` to calibrate uncertainty.
- If scientific or medical evidence appears anywhere in the image, avoid diagnostic conclusions even when the primary route is not `scientific-medical-imaging`.
- Do not over-read narrative meaning from a single still frame; state the missing motion, sound, or sequence context.
- Do not collapse mixed batches into a single verdict when the images clearly serve different roles.

## Batch handling

- For a same-project batch, analyze both individual quality and set-level consistency.
- For before/after batches, isolate what improved, what regressed, and what still blocks the target result.
- For mood boards or reference packs, look for repeated signals instead of over-critiquing one image in isolation.
- For subject-vs-reference batches, name the subject image first and use references only as anchors.
- For two-image batches, use a compact A/B difference read; for more than five images, group before analyzing.

## Recommended response pattern

Follow [references/output-contract.md](./references/output-contract.md).

At minimum, the final answer should include:

1. route decision and confidence
2. why that route fits
3. the route-specific analysis
4. a concrete study report with drills or next-step practice — **omit only when `response_depth: quick` AND `study_report_mode: none`**, in which case mark the answer "quick read only" and offer to expand on request
