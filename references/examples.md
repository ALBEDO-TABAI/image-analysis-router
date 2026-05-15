# High-risk Examples

These are compact anchors for cases where route choice often drifts. They are not exhaustive examples for every route.

## Batch mixed domain

Input: `poster.jpg`, `room-render.png`, `xray.png`; prompt says "分析这组混合参考图".

- Route: `generic-mixed`
- Batch type: `mixed_domain`
- Output: group poster under `graphic-design`, room render under `interior-design`, x-ray under `scientific-medical-imaging`, then synthesize why these references do or do not belong together.

## Architecture vs photography

Input: `tower-facade-photo.jpg`.

- If prompt says "看摄影构图和光线", route to `photography`.
- If prompt says "看建筑立面比例和街道关系", route to `architecture-urban`.

The same image can route differently because the user's lens changes the useful critique.

## Product ad vs product design

Input: `earbuds-render.jpg`.

- If prompt asks about ad persuasion, CTA, layout, or selling power, route to `graphic-design`.
- If prompt asks about form, material, CMF, ergonomics, seams, or manufacturing, route to `product-industrial-design`.

## Medical evidence inside a graphic

Input: `xray-health-campaign-poster.jpg`; prompt asks about poster persuasion.

- Primary route can be `graphic-design`.
- Medical safety still applies because the visual evidence contains an x-ray.
- Avoid diagnostic language and judge the poster's communication instead.

## Dashboard and UI

Input: `sales-dashboard-report.png`.

- If the prompt asks about reporting, decision support, KPI scan path, or executive readability, route to `presentation-document`.
- If the prompt asks about standalone app state, controls, and interaction clarity, route to `graphic-design` until a dedicated UI route exists.
