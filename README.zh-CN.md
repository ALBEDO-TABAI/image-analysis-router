# 图像分析路由器

中文文档 | [English](README.md)

<div align="center">

**🖼️ OpenAI + Claude Skill** | 先选读图方法，再给分析结论

[![类型: OpenAI + Claude Skill](https://img.shields.io/badge/类型-OpenAI%20%2B%20Claude%20Skill-6f42c1)](./SKILL.md)
[![路线数量: 17](https://img.shields.io/badge/路线-17-1f6feb)](./references/route-matrix.md)
[![Python: 3.13+ 已验证](https://img.shields.io/badge/Python-3.13%2B%20已验证-2ea44f)](./scripts/route_image_request.py)

</div>

> 🎯 这个 Skill 不会把所有图片都按同一套模板硬拆一遍。它会先判断这张图该怎么读，再给出对路的分析和能落地的练习建议。

## ✨ 功能特性

| 阶段 | 功能 | 说明 |
|-------|----------|-------------|
| 1️⃣ | **智能分流** | 先读用户问题、文件名和补充线索，缩小判断范围 |
| 2️⃣ | **视觉复核** | 把脚本结果当作初筛，再回到实际图像确认 |
| 3️⃣ | **定向分析** | 用 17 条路线里的合适方法，不拿一把尺子量所有图 |
| 4️⃣ | **双份输出** | 同时给出 `Analysis Report` 和 `Study Report` |

## 🚀 快速开始

### 环境要求

```bash
# 1. Python（用于本地分流脚本）
py --version

# 2. 一个支持本地 Skill 的 AI 代理环境
# 例如能读取 SKILL.md、references/、scripts/，并接受图片输入的环境

# 3. 图片输入
# 本地图片、截图、文件名、OCR 文本，或带上下文的图像请求都可以
```

### 使用方式

🧩 这是一个本地 Skill，适用于 OpenAI 和 Claude 生态里的代理环境。把整个目录放进你的 Skill 目录里：

```bash
mkdir -p "$CODEX_HOME/skills"
cp -r ./image-analysis-router "$CODEX_HOME/skills/image-analysis-router"
```

📁 如果你的代理用的是别的 Skill 目录，比如 `.agents/skills/`，把目标路径换掉就行，目录结构保持不变。

💬 安装好以后，直接向代理发图像分析请求，比如：

> "用 `image-analysis-router` 分析这张海报，重点看层级和字体。"

> "帮我拆一下这组室内效果图，顺便告诉我下一步怎么练。"

> "先判断这页 PPT 该走哪条路线，再给我一份学习报告。"

🔎 如果你手里只有文件名、提示词或 OCR 文本，也可以先跑分流脚本：

```bash
py .\scripts\route_image_request.py --prompt "分析这张建筑立面图，看看它和街道关系处理得怎么样" --file "tower-facade-render.jpg"
```

## 🧭 分流怎么工作

🛣️ 这个 Skill 先回答一个更关键的问题：这张图到底该用什么方法看。

```text
图像请求
    ↓
[1️⃣ 文本与文件名初筛] ──→ route_image_request.py 生成路由 prior
    ↓
[2️⃣ 实际看图复核] ──→ 确认主路线，或先把混合批次拆开
    ↓
[3️⃣ 选择分析方法] ──→ 从 17 条专用路线里选最合适的一条
    ↓
[4️⃣ 最终输出] ──→ Analysis Report + Study Report
```

### 路线信心

🧠 在正式展开分析前，Skill 会先标出自己对路线判断有多确定：

| 级别 | 含义 |
|-------|---------|
| `high` | 图片类型和用户目标都很清楚，基本就是这一条路 |
| `medium` | 有主路线，但还有一个备选方向也说得通 |
| `low` | 图片太杂、线索太少，或者得先拆组再看 |

## 🗂️ 路线覆盖

🖍️ 现在内置了 17 条路线，够覆盖大多数常见的读图任务。

### 设计与传播

- `graphic-design`：海报、品牌图、包装、UI 截图、广告创意
- `infographic-diagram`：图表、地图、流程图、信息图
- `typography-lettering`：字体海报、字标、书法、字形研究
- `presentation-document`：PPT 页面、报告页、提案页、文档页

### 影像与叙事

- `photography`：纪实、人像、街拍、商业摄影
- `film-frame`：电影截图、动画帧、分镜、剧照式画面
- `comics-sequential`：漫画页、条漫、分镜页、顺序叙事
- `game-visual-design`：游戏界面、HUD、关卡截图、角色面板

### 艺术与空间

- `painting-illustration`：绘画、插画、概念图、风格化图像
- `interior-design`：室内效果图、空间照片、材质和家具研究
- `architecture-urban`：建筑立面、街景、公共空间、场地关系
- `sculpture-installation-craft`：雕塑、装置、陶艺、工艺类立体作品

### 对象与专业图像

- `product-industrial-design`：产品外观、原型、物件形态、包装结构
- `fashion-styling`：穿搭、造型、配饰、lookbook、时尚视觉
- `scientific-medical-imaging`：医学图像、显微图、科研图、技术图像

### 兜底路线

- `generic-mixed`：图像组太杂，得先分组再分析
- `universal-fallback`：没有明显归类，但仍然值得结构化阅读

## 🧠 你会拿到什么

📌 每次分析都会先告诉你：最后选了哪条路线、把握有多大、为什么这条比别的路线更合适。

📝 `Analysis Report` 会给你一个很快能抓住重点的判断，再展开按路线细拆，最后落到整体评价：这张图想做什么，它到底做到了多少。

📚 `Study Report` 会把结论翻成下一步动作，包括现在该补什么、适合练什么、下次最容易犯什么错，以及必要时该对照哪些参考。

## 📁 项目结构

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

## ⚙️ 配置说明

🛠️ 默认流程不需要额外配置文件，拿来就能用。

🔤 如果你只是想先做一次本地分流预判，也可以直接跑脚本：

```bash
py .\scripts\route_image_request.py --prompt "<用户目标>" --file "<文件名或路径>" --hint "<OCR 或补充线索>"
```

📎 参数说明：

- `--prompt`：用户问题或目标
- `--file`：图片文件名或路径，可重复传入
- `--hint`：OCR 文本、标题、备注等补充线索，可重复传入

## 📄 输出内容

📦 正常一次分析，至少会有两份核心结果：

| 输出 | 内容 |
|--------|---------|
| `Analysis Report` | 路线判断、关键发现、详细分析、整体结论 |
| `Study Report` | 学习重点、练习方向、容易踩的坑、下一步建议 |

🧪 如果是成组图片，它还会补充整组一致性、前后变化，以及要不要先拆成几个子组。

## ⚠️ 使用原则

🧱 脚本结果只是起点，不是最后答案。

👀 重要判断必须回到能看见的证据。

📐 不同类型的图，不能用同一套标准硬套。

🤝 路线拿不准时，就老实说不确定，不硬编。

## ✅ 支持环境

💻 这个 Skill 最适合用在能读取本地 Skill 目录、也能接收图片输入的 AI 代理环境里。

| 环境 | 状态 |
|-------------|--------|
| 能读取 `SKILL.md` 和本地参考文件的代理环境 | ✅ 支持 |
| 能处理截图、本地图片或图片附件的代理环境 | ✅ 支持 |
| 只能纯文本聊天、读不到本地 Skill 文件的环境 | ⚠️ 能力受限 |

## 🔗 相关文件

📚 这个仓库里最关键的文件在这里：

- [README.md](./README.md)
- [SKILL.md](./SKILL.md)
- [references/route-matrix.md](./references/route-matrix.md)
- [references/output-contract.md](./references/output-contract.md)
- [scripts/route_image_request.py](./scripts/route_image_request.py)
