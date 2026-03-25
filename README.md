# Image Analysis Router

[中文文档](README.zh-CN.md) | English

<div align="center">

**🖼️ OpenAI + Claude Skill** | Route first, analyze second

[![Type: OpenAI + Claude Skill](https://img.shields.io/badge/Type-OpenAI%20%2B%20Claude%20Skill-6f42c1)](./SKILL.md)
[![Routes: 17](https://img.shields.io/badge/Routes-17-1f6feb)](./references/route-matrix.md)
[![Python: 3.13+ tested](https://img.shields.io/badge/Python-3.13%2B%20tested-2ea44f)](./scripts/route_image_request.py)

</div>

> 🎯 This skill does not treat every image like the same homework. It decides how the image should be read first, then returns a targeted critique and a practical study plan.

## ✨ Features

| Stage | Function | Description |
|-------|----------|-------------|
| 1️⃣ | **Smart Routing** | Read the request, filenames, and hints first to narrow down the right lens |
| 2️⃣ | **Visual Check** | Treat the script as a prior, then confirm with actual visual evidence |
| 3️⃣ | **Targeted Analysis** | Use one of 17 routes instead of forcing one standard onto every image |
| 4️⃣ | **Dual Output** | Return both an `Analysis Report` and a `Study Report` |

## 🚀 Quick Start

### Prerequisites

```bash
# 1. Python for the local routing script
py --version

# 2. An AI agent environment that can read local skills
# For example: an environment that can load SKILL.md, references/, scripts/, and image input

# 3. Image input
# Local images, screenshots, filenames, OCR text, or image-heavy requests with context
```

### Usage

🧩 This is a local skill for OpenAI- and Claude-based agent environments. Put the whole folder into your skill directory:

```bash
mkdir -p "$CODEX_HOME/skills"
cp -r ./image-analysis-router "$CODEX_HOME/skills/image-analysis-router"
```

📁 If your agent uses a different skill folder, such as `.agents/skills/`, replace the target path and keep the same folder structure.

💬 Then call the skill with a real image request, for example:

> "Use `image-analysis-router` to review this poster. Focus on hierarchy and typography."

> "Break down this batch of interior renders and tell me what to practice next."

> "Figure out which route fits this slide first, then give me a study report."

🔎 If you only have text clues, filenames, or OCR, run the routing script first:

```bash
py .\scripts\route_image_request.py --prompt "Analyze this tower facade and check how it meets the street" --file "tower-facade-render.jpg"
```

## 🧭 How Routing Works

🛣️ The skill answers one question before anything else: what is the right way to read this image?

```text
Image request
    ↓
[1️⃣ Text and filename pass] ──→ route_image_request.py generates a routing prior
    ↓
[2️⃣ Visual confirmation] ──→ confirm the main route or split the batch
    ↓
[3️⃣ Method selection] ──→ choose 1 of 17 specialized routes
    ↓
[4️⃣ Final output] ──→ Analysis Report + Study Report
```

### Route Confidence

🧠 The skill marks how sure it is about the route before moving on:

| Level | Meaning |
|-------|---------|
| `high` | The image type and user goal point clearly to one route |
| `medium` | One route leads, but another one still makes sense |
| `low` | The batch is mixed, the clues are thin, or the images need regrouping first |

## 🗂️ Route Coverage

🖍️ The skill currently ships with 17 routes for common image-reading jobs.

### Design and communication

- `graphic-design`: posters, brand visuals, packaging, UI screenshots, ad creatives
- `infographic-diagram`: charts, maps, process diagrams, information graphics
- `typography-lettering`: type posters, lettering, logotypes, calligraphy, letterform study
- `presentation-document`: slides, report pages, proposal pages, document spreads

### Image and narrative

- `photography`: documentary, portrait, street, editorial, commercial photography
- `film-frame`: movie stills, animation frames, storyboard shots, cinematic compositions
- `comics-sequential`: comic pages, manga, strips, webtoon panels, sequence storytelling
- `game-visual-design`: game UI, HUD, level screenshots, character panels

### Art and space

- `painting-illustration`: paintings, illustrations, concept art, stylized image work
- `interior-design`: interior renders, room photos, material and furniture studies
- `architecture-urban`: facades, street views, public space, urban and site relationships
- `sculpture-installation-craft`: sculpture, installation, ceramics, craft-based 3D work

### Objects and specialist imagery

- `product-industrial-design`: products, prototypes, object form, packaging structure
- `fashion-styling`: outfits, silhouettes, accessories, lookbooks, styling visuals
- `scientific-medical-imaging`: medical scans, microscopy, technical and research imagery

### Fallback routes

- `generic-mixed`: mixed batches that need grouping before critique
- `universal-fallback`: images that do not fit cleanly anywhere else but still need a structured read

## 🧠 What You Get

📌 Every run starts with a route decision: which route won, how confident the skill is, and why that route fits better than the alternatives.

📝 The `Analysis Report` gives a quick read, a route-specific breakdown, and a final judgment about what the image is trying to do and where it actually lands.

📚 The `Study Report` turns that into next steps: what to learn now, what drills to run, what to watch next time, and what comparisons are worth making.

## 📁 Project Structure

```text
image-analysis-router/
├── SKILL.md
├── README.md
├── README.zh-CN.md
├── agents/
│   └── openai.yaml
├── scripts/
│   └── route_image_request.py
└── references/
    ├── route-matrix.md
    ├── output-contract.md
    └── method-*.md
```

## ⚙️ Configuration

🛠️ The skill does not require a separate config file for the default workflow.

🔤 If you only want a local routing guess before the full image review, you can call the script directly:

```bash
py .\scripts\route_image_request.py --prompt "<user goal>" --file "<file name or path>" --hint "<OCR or extra clue>"
```

📎 Parameters:

- `--prompt`: the user's goal or question
- `--file`: image file name or path, repeatable
- `--hint`: OCR text, title, note, or any extra clue, repeatable

## 📄 Output

📦 A normal run gives you two core outputs:

| Output | Content |
|--------|---------|
| `Analysis Report` | route decision, key findings, detailed critique, overall judgment |
| `Study Report` | learning focus, drills, likely mistakes, next-step practice |

🧪 For batches, the skill can also comment on set-level consistency, before/after changes, and whether the images should be split into subgroups first.

## ⚠️ Ground Rules

🧱 The script output is a starting point, not the final answer.

👀 Important judgments have to go back to visible evidence.

📐 Different image types should not be judged with the same standard.

🤝 When the route is unclear, the skill should say so instead of bluffing.

## ✅ Supported Environments

💻 This skill works best in AI agent environments that can load local skill folders and accept image input.

| Environment | Status |
|-------------|--------|
| Agents that can read `SKILL.md` and local reference files | ✅ Supported |
| Agents that can inspect screenshots, local images, or image attachments | ✅ Supported |
| Text-only chat environments with no access to local skill files | ⚠️ Limited |

## 🔗 Related Files

📚 Key files in this repo:

- [README.zh-CN.md](./README.zh-CN.md)
- [SKILL.md](./SKILL.md)
- [references/route-matrix.md](./references/route-matrix.md)
- [references/output-contract.md](./references/output-contract.md)
- [scripts/route_image_request.py](./scripts/route_image_request.py)
