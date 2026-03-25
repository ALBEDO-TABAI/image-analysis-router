# 图像分析路由器

中文文档

OpenAI Skill | 面向 AI 代理的图像分流与定向分析工具

> 不是简单地“描述图片”，而是先判断这张图该用什么方法分析，再输出有针对性的分析报告和学习报告。

## ✨ 功能特性

| 阶段 | 功能 | 说明 |
| --- | --- | --- |
| 1️⃣ | 智能分流 | 根据用户问题、文件名和补充线索，先判断最适合的分析路线 |
| 2️⃣ | 视觉复核 | 把脚本结果当作初筛，再结合实际看图确认最终路线 |
| 3️⃣ | 定向分析 | 按 17 条路线之一展开，不再用同一把尺子乱评所有图片 |
| 4️⃣ | 双报告输出 | 同时产出 `Analysis Report` 和 `Study Report`，既能看懂，也知道下一步怎么练 |

## 🚀 快速开始

### 环境要求

```bash
# 1. Python（用于本地分流脚本）
py --version

# 2. 一个支持本地 Skill 的 AI 代理环境
# 例如支持读取 SKILL.md、references/、scripts/ 的 Codex / OpenAI Agent 环境

# 3. 图片输入
# 可以是本地图片、文件名、截图，或带上下文的图像请求
```

### 安装方式

这是一个面向 AI 代理的本地 Skill。将整个目录放到你的 Skill 目录中，例如：

```bash
mkdir -p "$CODEX_HOME/skills"
cp -r ./image-analysis-router "$CODEX_HOME/skills/image-analysis-router"
```

如果你的环境使用的是别的 Skill 目录，例如 `.agents/skills/`，把目标路径替换掉就可以。

或者直接把当前文件夹复制到你的 Skill 目录下，保留以下结构：

```text
$CODEX_HOME/skills/image-analysis-router/
├── SKILL.md
├── README.zh-CN.md
├── scripts/
├── references/
└── agents/
```

### 使用方式

安装完成后，直接向代理发起图像分析请求，例如：

> “用 `image-analysis-router` 分析这张海报，重点看层级和字体。”

> “帮我拆一下这组室内效果图，顺便告诉我下一步怎么练。”

> “看看这页 PPT 应该按什么路线分析，再给我一份学习报告。”

如果你只有文件名、提示词或 OCR 文本，也可以先跑本地分流脚本：

```bash
py .\scripts\route_image_request.py --prompt "分析这张建筑立面图，看看它和街道关系处理得怎么样" --file "tower-facade-render.jpg"
```

## 🧭 智能分流流程

Skill 会先决定“该怎么读图”，再决定“怎么写分析”：

```text
图像请求
    ↓
[1️⃣ 文本与文件名初筛] ──→ route_image_request.py 生成路由 prior
    ↓
[2️⃣ 实际看图复核] ──→ 确认主路线 / 判断是否需要拆成多个子组
    ↓
[3️⃣ 选择分析方法] ──→ 17 条专用路线之一
    ↓
[4️⃣ 输出结果] ──→ Analysis Report + Study Report
```

### 分流置信度

Skill 会在结果里标出路线信心：

| 级别 | 含义 |
| --- | --- |
| `high` | 图片类型和用户目标都很明确，主路线基本没有竞争者 |
| `medium` | 有主路线，但还有一个备选方向也说得通 |
| `low` | 图片混合度高、信息不足，或者需要先拆组再分析 |

## 🗂️ 路线覆盖

目前内置 17 条分析路线，覆盖常见的图像阅读任务：

### 1. 设计与传播

- `graphic-design`：海报、品牌图、包装、UI 截图、广告创意
- `infographic-diagram`：图表、流程图、示意图、信息图
- `typography-lettering`：字体海报、字标、书法、字形研究
- `presentation-document`：PPT 页面、报告页、提案页、文档页

### 2. 影像与叙事

- `photography`：摄影作品、纪实、人像、街拍、商业拍摄
- `film-frame`：电影截图、分镜、动画帧、剧照
- `comics-sequential`：漫画页、条漫、分镜页、图文顺序叙事
- `game-visual-design`：游戏界面、HUD、关卡截图、角色面板

### 3. 艺术与空间

- `painting-illustration`：绘画、插画、概念图、AI 艺术图
- `interior-design`：室内效果图、空间照片、样板间、家具空间
- `architecture-urban`：建筑外立面、街景、公共空间、城市设计图
- `sculpture-installation-craft`：雕塑、装置、陶艺、立体工艺作品

### 4. 对象与专业图像

- `product-industrial-design`：产品外观、工业设计、原型、包装结构
- `fashion-styling`：穿搭、造型、lookbook、时尚视觉
- `scientific-medical-imaging`：医学图像、显微图、科研图、技术图像

### 5. 兜底路线

- `generic-mixed`：图像组很杂，需要先拆组再分析
- `universal-fallback`：没有明显归属，但仍值得做结构化阅读

## 🧠 分析与学习框架

### 1. Route Decision（先选对尺子）

每次分析都会先给出：

- 选择了哪条路线
- 当前信心高不高
- 为什么是这条路线，而不是别的路线

### 2. Analysis Report（分析报告）

分析报告至少包含：

- `Quick Read`：先用 3 到 5 条把重点说清楚
- `Detailed Analysis`：按当前路线的专用维度展开
- `Overall Judgment`：总结这张图哪里强，哪里拖后腿，它到底在试图完成什么

### 3. Study Report（学习报告）

学习报告会把结论转成行动建议，包括：

- `What to Learn Now`
- `Practice Drills`
- `What to Watch For Next Time`
- `Suggested Comparisons`（只在有必要时给）

## 📁 项目结构

```text
image-analysis-router/
├── SKILL.md                                   # 核心 Skill 入口与工作流
├── README.zh-CN.md                            # 中文项目说明
├── agents/
│   └── openai.yaml                            # Skill 展示与默认提示
├── scripts/
│   └── route_image_request.py                 # 本地分流脚本
└── references/
    ├── route-matrix.md                        # 路线选择矩阵
    ├── output-contract.md                     # 统一输出格式
    ├── method-graphic-design.md               # 平面设计分析方法
    ├── method-photography.md                  # 摄影分析方法
    ├── method-painting-illustration.md        # 绘画 / 插画分析方法
    ├── method-interior-design.md              # 室内设计分析方法
    ├── method-architecture-urban.md           # 建筑 / 城市分析方法
    ├── method-infographic-diagram.md          # 信息图 / 图表分析方法
    ├── method-product-industrial-design.md    # 产品 / 工业设计分析方法
    ├── method-comics-sequential.md            # 漫画 / 顺序叙事分析方法
    ├── method-fashion-styling.md              # 时尚 / 造型分析方法
    ├── method-sculpture-installation-craft.md # 雕塑 / 装置 / 工艺分析方法
    ├── method-game-visual-design.md           # 游戏视觉分析方法
    ├── method-scientific-medical-imaging.md   # 科学 / 医学图像分析方法
    ├── method-typography-lettering.md         # 字体 / 字形分析方法
    ├── method-presentation-document.md        # 演示文档分析方法
    ├── method-film-frame.md                   # 电影帧分析方法
    ├── method-generic-mixed.md                # 混合批次分组方法
    └── method-universal-fallback.md           # 通用兜底方法
```

## ⚙️ 配置说明

这个 Skill 默认不依赖额外配置文件。

如果你只想做“先分流再确认”的本地预判，可以直接使用脚本：

```bash
py .\scripts\route_image_request.py --prompt "<用户问题>" --file "<文件名或路径>" --hint "<OCR 或补充线索>"
```

参数说明：

- `--prompt`：用户问题或任务目标
- `--file`：图片文件名或路径，可重复传入多个
- `--hint`：OCR 文本、说明文字、标题等辅助线索，可重复传入多个

## 🧾 输出内容

分析完成后，至少会得到两份核心结果：

| 输出 | 内容 |
| --- | --- |
| `Analysis Report` | 路线判断、关键发现、详细分析、整体结论 |
| `Study Report` | 该补什么、怎么练、下次容易踩什么坑 |

如果是成组图片，Skill 还会额外处理这些情况：

- 同项目多张图：补一段“整组是否一致”的判断
- before / after 对比：单独指出进步、退步和还没解决的点
- 混合图集：先拆成多个子组，再分别分析

## ⚠️ 使用原则

为了避免“看起来很懂，实际全说偏”，这个 Skill 有几条硬规则：

- 脚本结果只是初筛，不是最终结论
- 重要判断必须回到可见证据，不靠空想
- 不同图像类型不能混用同一套标准
- 路线不明确时，要老实承认不确定，而不是硬编

## ✅ 支持环境

这是一个面向 AI 代理的本地 Skill，适用于：

| 环境 | 状态 |
| --- | --- |
| 支持本地 Skill 目录、可读取 `SKILL.md` 的代理环境 | ✅ 支持 |
| 支持图片输入、截图分析、本地文件分析的代理环境 | ✅ 支持 |
| 仅能做纯文本问答、不能访问本地 Skill 文件的环境 | ⚠️ 能力受限 |

## 🔗 相关文件

- [SKILL.md](./SKILL.md)
- [references/route-matrix.md](./references/route-matrix.md)
- [references/output-contract.md](./references/output-contract.md)
- [scripts/route_image_request.py](./scripts/route_image_request.py)

## 🔗 相关文献

艺术批评与鉴赏理论

Feldman's Model of Art Criticism — Edmund Burke Feldman，可搜索 Becoming Human Through Art (1970)
Panofsky's Iconological Method — Erwin Panofsky，Studies in Iconology (1939)
Wölfflin's Principles of Art History — Heinrich Wölfflin，Principles of Art History (1915)
谢赫六法 — 南齐谢赫《古画品录》
Terry Barrett's Photography Criticism — Criticizing Photographs (多版本)
Roland Barthes, Studium & Punctum — Camera Lucida / 明室 (1980)


知识库与分类系统

Getty Art & Architecture Thesaurus (AAT) → getty.edu/research/tools/vocabularies/aat
Getty ULAN (Union List of Artist Names) → getty.edu/research/tools/vocabularies/ulan
Iconclass → iconclass.org
CIDOC-CRM → cidoc-crm.org


计算机视觉模型

CenterNet → arxiv.org/abs/1904.07850
YOLOv8 → github.com/ultralytics/ultralytics
SqueezeNet → arxiv.org/abs/1602.07360
DenseNet → arxiv.org/abs/1608.06993
CLIP → arxiv.org/abs/2103.00020
SAM (Segment Anything Model) → arxiv.org/abs/2304.02643
Stable Diffusion → arxiv.org/abs/2112.10752
StyleGAN3 → arxiv.org/abs/2106.12423
LoRA → arxiv.org/abs/2106.09685
Pix2Struct → arxiv.org/abs/2210.03347


美学评估模型与数据集

NIMA (Neural Image Assessment) → arxiv.org/abs/1709.05424
AVA Dataset → 可搜索 AVA: A Large-Scale Database for Aesthetic Visual Analysis (Murray et al., CVPR 2012)
ArtEmis Dataset → artemisdataset.org
TANet (Theme-Aware Network) → 可搜索 TAD66K 数据集相关论文
HumanAesExpert / HumanBeauty → 可搜索 Human Image Aesthetic Assessment 相关论文
WP-CLIP → 可搜索 Wölfflin Principles + CLIP 相关工作
DesignBench → 可搜索 DesignBench: A Multimodal Benchmark for Visual Design


可解释性AI

RISE → arxiv.org/abs/1806.07421
Grad-CAM → arxiv.org/abs/1610.02391
XAIxArts → 可搜索 Explainable AI for the Arts，相关论文发表于 ACM Creativity & Cognition


其他工具与框架

Visual Thinking Strategies (VTS) → vtshome.org
EyeEm Aesthetic Algorithm → 可搜索 EyeEm AI aesthetic research
LangChain → langchain.com
Pinecone → pinecone.io