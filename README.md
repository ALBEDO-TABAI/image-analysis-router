# Image Analysis Router

OpenAI Skill | 面向 AI 代理的图像分流与定向分析工具

> 它不是把所有图片都按同一套模板去“描述一遍”，而是先判断这张图应该用什么方法读，再给出对应的分析和学习建议。

完整中文说明见 [README.zh-CN.md](./README.zh-CN.md)。

## 这个项目解决什么问题

很多图像请求真正难的地方，不是“看见了什么”，而是“该用哪套标准来判断这张图”。

这套 Skill 的做法是：

1. 先根据用户问题、文件名和补充线索做初步分流
2. 再结合实际看图复核，避免脚本误判
3. 按最合适的路线做定向分析，而不是混用标准
4. 同时给出分析结论和下一步训练建议

## 主要能力

- 智能分流：先决定该怎么读图，再决定怎么写分析
- 视觉复核：脚本只做初筛，最终结论回到可见证据
- 定向分析：内置 17 条专用路线，覆盖设计、摄影、空间、产品、艺术、专业图像等常见场景
- 双报告输出：同时产出 `Analysis Report` 和 `Study Report`

## 覆盖路线

### 设计与传播

- `graphic-design`
- `infographic-diagram`
- `typography-lettering`
- `presentation-document`

### 影像与叙事

- `photography`
- `film-frame`
- `comics-sequential`
- `game-visual-design`

### 艺术与空间

- `painting-illustration`
- `interior-design`
- `architecture-urban`
- `sculpture-installation-craft`

### 对象与专业图像

- `product-industrial-design`
- `fashion-styling`
- `scientific-medical-imaging`

### 兜底路线

- `generic-mixed`
- `universal-fallback`

## 快速开始

### 1. 放进你的 Skill 目录

```bash
mkdir -p "$CODEX_HOME/skills"
cp -r ./image-analysis-router "$CODEX_HOME/skills/image-analysis-router"
```

如果你的环境使用的是别的 Skill 目录，比如 `.agents/skills/`，把目标路径替换掉即可。

### 2. 直接向代理发起图像分析请求

例如：

- “用 `image-analysis-router` 分析这张海报，重点看层级和字体。”
- “帮我拆一下这组室内效果图，顺便告诉我下一步怎么练。”
- “看看这页 PPT 应该按什么路线分析，再给我一份学习报告。”

### 3. 只做本地预判时，先跑分流脚本

```bash
py .\scripts\route_image_request.py --prompt "分析这张建筑立面图，看看它和街道关系处理得怎么样" --file "tower-facade-render.jpg"
```

## 输出内容

每次分析至少会产出两份结果：

- `Analysis Report`：路线判断、关键发现、详细分析、整体结论
- `Study Report`：下一步该补什么、怎么练、下次注意什么

如果是成组图片，还会额外处理一致性、前后变化和混合批次拆组。

## 项目结构

```text
image-analysis-router/
├── SKILL.md
├── README.md
├── README.zh-CN.md
├── agents/
├── scripts/
└── references/
```

## 使用原则

- 脚本结果只是初筛，不是最终结论
- 重要判断必须回到可见证据
- 不同图像类型不能混用同一套标准
- 路线不明确时，要承认不确定，而不是硬套结论

## 相关文件

- [完整中文说明](./README.zh-CN.md)
- [Skill 入口](./SKILL.md)
- [路线矩阵](./references/route-matrix.md)
- [输出格式约定](./references/output-contract.md)
- [本地分流脚本](./scripts/route_image_request.py)
