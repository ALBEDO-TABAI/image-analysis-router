# Route Matrix

Use this file to decide which analysis method fits the input best.

## Selection order

1. Start from the user's learning goal.
2. Check the image's dominant evidence.
3. Break ties with the route that best explains the image's success or failure.
4. If the batch is truly mixed, split it.

## Route table

| Route | Strong signals | Use when the user cares about | Avoid when | Read next |
| --- | --- | --- | --- | --- |
| `graphic-design` | large text blocks, title/subtitle/CTA, logos, brand marks, layout grids, posters, banners, packaging, ad creatives, UI screenshots | hierarchy, clarity, persuasion, branding, typography, layout rhythm | the image is mainly about camera craft, painterly medium, or spatial design | [method-graphic-design.md](./method-graphic-design.md) |
| `photography` | camera-captured detail, lens depth, exposure decisions, natural or studio light, captured moment, documentary realism, visible medium or retouching clues | composition, light, timing, mood, technical quality, edit direction, authenticity/medium, reverse-reading of lens and light | the core question is art-historical symbolism, interior zoning, or film shot language | [method-photography.md](./method-photography.md) |
| `painting-illustration` | brushwork, drawing, stylization, invented worlds, symbolic imagery, cross-cultural motifs, visible medium logic | style, iconography, visual language, art history, symbolic reading, illustration craft | the image is mainly a poster/ad layout or a real room evaluation | [method-painting-illustration.md](./method-painting-illustration.md) |
| `interior-design` | rooms, furniture, ceilings, walls, materials, fixtures, circulation, daylight/artificial light in a space, renders of spaces | layout, zoning, atmosphere, usability, material palette, lighting plan | the image is mainly a single object shot, a poster, or a non-spatial artwork | [method-interior-design.md](./method-interior-design.md) |
| `architecture-urban` | facades, building massing, towers, campus views, streetscapes, plazas, site relationships, skyline effects, landscape integration | massing, facade order, site fit, public realm, pedestrian experience, urban effect | the image is mainly an interior, a pure photo-craft critique, or a product object in front of a building | [method-architecture-urban.md](./method-architecture-urban.md) |
| `infographic-diagram` | charts, graphs, axes, legends, arrows, process steps, maps, network diagrams, system schematics, data labels | clarity, logic, truthfulness, notation, scan path, interpretation risk | the image is mainly a brand poster, UI marketing screen, or expressive illustration with only light data content | [method-infographic-diagram.md](./method-infographic-diagram.md) |
| `product-industrial-design` | isolated objects, prototypes, product renders, device views, packaging structures, furniture-object studies, controls and seams | form, affordance, ergonomics, manufacturability, material-finish logic, market signal | the image is mainly a styled ad layout, a room scene, or a pure photo critique | [method-product-industrial-design.md](./method-product-industrial-design.md) |
| `comics-sequential` | comic pages, manga pages, strips, webtoon panels, speech bubbles, captions, gutters, sequential beats | panel flow, pacing, staging, text-image coordination, page-level storytelling | the image is a single illustration with no sequential logic, or a storyboard being analyzed as cinema staging | [method-comics-sequential.md](./method-comics-sequential.md) |
| `fashion-styling` | outfits, garments, silhouettes, accessories, lookbooks, runway/editorial looks, styling grids, beauty-grooming cues | silhouette, layering, material hand, styling cohesion, persona signal, outfit logic | the image is mainly about camera craft, product detail engineering, or general graphic layout | [method-fashion-styling.md](./method-fashion-styling.md) |
| `sculpture-installation-craft` | sculptures, installations, ceramics, craft objects, assemblage, site-specific works, gallery placement, plinths, hanging pieces | volume, material assembly, viewing path, spatial presence, craft resolution, site relation | the image is mainly a building, room, or product being judged by use logic | [method-sculpture-installation-craft.md](./method-sculpture-installation-craft.md) |
| `game-visual-design` | gameplay screenshots, HUD, minimap, character sheets, inventory screens, key art tied to gameplay, level views, quest UI | gameplay readability, environment legibility, encounter clarity, UI/HUD, diegesis, art direction in play | the image is mainly a film still, pure concept art, or general product UI outside a game context | [method-game-visual-design.md](./method-game-visual-design.md) |
| `scientific-medical-imaging` | scans, x-rays, microscope views, pathology plates, remote sensing, lab figures, technical evidence images, annotated scientific visuals | interpretability, annotation, signal-vs-noise, diagnostic caution, visual validity, evidence communication | the main job is artistic mood, fashion signal, or general brand communication | [method-scientific-medical-imaging.md](./method-scientific-medical-imaging.md) |
| `typography-lettering` | type posters, lettering studies, wordmarks, calligraphy, font proofs, kinetic type stills, text-only compositions | letterform construction, spacing, rhythm, legibility, voice, reading texture | the image is mainly a full communication layout where type is only one layer | [method-typography-lettering.md](./method-typography-lettering.md) |
| `presentation-document` | slides, pitch decks, report pages, proposal pages, executive summaries, research pages, document spreads | argument flow, page logic, slide hierarchy, scanability, sequence coherence, decision support | the image is mainly a poster, infographic, or dashboard being judged outside a document context | [method-presentation-document.md](./method-presentation-document.md) |
| `film-frame` | widescreen frames, subtitles/timecode, cinematic blocking, shot scale, scene/still references, storyboard panels | shot language, framing, blocking, genre mood, narrative function of a frame | the image is really a marketing poster or static design layout | [method-film-frame.md](./method-film-frame.md) |
| `generic-mixed` | ambiguous hybrids, diagrams, memes, or batches spanning several routes | triage, first-pass reading, re-grouping a mixed set | a clear dominant route already exists | [method-generic-mixed.md](./method-generic-mixed.md) |
| `universal-fallback` | novel, niche, or uncategorizable visuals with weak route scores but clear need for structured reading | disciplined first-principles analysis when forcing a named route would distort the result | a clear named route already fits | [method-universal-fallback.md](./method-universal-fallback.md) |

## Tie-breakers

- `graphic-design` vs `film-frame`: choose `graphic-design` if reading order, text hierarchy, or marketing effect matters most; choose `film-frame` if shot language or scene meaning matters most.
- `photography` vs `painting-illustration`: choose `photography` if realism, capture timing, lens/light behavior, or post-processing matters; choose `painting-illustration` if medium logic, stylization, symbolism, or art-historical reading matters.
- `painting-illustration` vs `interior-design`: choose `interior-design` when the user is evaluating the space itself, even if the space is rendered or stylized.
- `photography` vs `interior-design`: choose `interior-design` when the subject is the room experience; choose `photography` when the user is critiquing the photographer's capture choices more than the space.
- `architecture-urban` vs `photography`: choose `photography` when the user is mainly critiquing the shot; choose `architecture-urban` when the real question is the building, facade, site, or city effect.
- `architecture-urban` vs `interior-design`: choose `interior-design` for room experience; choose `architecture-urban` for exterior form, site, and public realm.
- `graphic-design` vs `infographic-diagram`: choose `infographic-diagram` when truthfulness, notation, and explanation dominate; choose `graphic-design` when campaign tone, brand effect, or promotion dominates.
- `graphic-design` vs `product-industrial-design`: choose `product-industrial-design` when the object itself is the design subject; choose `graphic-design` when the object is only one element in a communication layout.
- `painting-illustration` vs `comics-sequential`: choose `comics-sequential` when panel order, balloons, or beats are central; choose `painting-illustration` when the image is effectively a single artwork.
- `film-frame` vs `comics-sequential`: choose `film-frame` for cinematic shot language; choose `comics-sequential` when page-level storytelling and reading order matter.
- `fashion-styling` vs `photography`: choose `photography` when the real question is the shot; choose `fashion-styling` when the real question is silhouette, styling logic, and persona signal.
- `sculpture-installation-craft` vs `product-industrial-design`: choose `product-industrial-design` for use objects and manufactured affordance; choose `sculpture-installation-craft` for spatial presence, craft, or non-utilitarian three-dimensional work.
- `game-visual-design` vs `graphic-design`: choose `game-visual-design` when play readability or diegetic UI matters; choose `graphic-design` for promo key art or marketing layouts detached from play.
- `scientific-medical-imaging` vs `infographic-diagram`: choose `scientific-medical-imaging` when the image itself is evidence; choose `infographic-diagram` when the image is mainly explanatory packaging around evidence.
- `typography-lettering` vs `graphic-design`: choose `typography-lettering` when type itself is the primary subject; choose `graphic-design` when type serves a broader layout.
- `presentation-document` vs `graphic-design`: choose `presentation-document` when argument flow and page sequence matter; choose `graphic-design` when single-page campaign impact matters most.
- Use `universal-fallback` when top scores stay weak and no tie cluster points to a meaningful subgroup.

## Route confidence

- `high`: strong route signals and no serious competitor
- `medium`: one route leads, but a second route could also work
- `low`: not enough evidence, or the image is hybrid enough that the chosen route is only provisional

When confidence is `low`, say so and name the runner-up route.
