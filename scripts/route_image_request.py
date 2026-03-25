#!/usr/bin/env python3
"""Lightweight keyword router for image-analysis-router.

Use this script as a deterministic routing prior from prompt text, file names,
and optional hints. Always confirm the route with actual visual inspection.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Bucket:
    name: str
    keywords: tuple[str, ...]
    filename_patterns: tuple[str, ...]


ROUTES: tuple[Bucket, ...] = (
    Bucket(
        "graphic-design",
        (
            "graphic design",
            "平面设计",
            "海报",
            "poster",
            "banner",
            "kv",
            "主视觉",
            "品牌",
            "brand",
            "包装",
            "packaging",
            "版式",
            "typography",
            "字体",
            "排版",
            "layout",
            "ui",
            "ui界面",
            "应用界面",
            "app screen",
            "landing page",
            "广告",
            "ad creative",
            "cta",
        ),
        (
            r"\bposter\b",
            r"\bbanner\b",
            r"\bbrand\b",
            r"\bpackag",
            r"\bui\b",
            r"\bscreen\b",
            r"\bkv\b",
            r"\bdeck\b",
            r"\bcarousel\b",
            r"\.psd$",
            r"\.ai$",
            r"\.fig$",
            r"\.sketch$",
        ),
    ),
    Bucket(
        "photography",
        (
            "photography",
            "photo",
            "摄影",
            "照片",
            "portrait",
            "人像",
            "street",
            "街拍",
            "landscape",
            "风光",
            "documentary",
            "纪实",
            "fashion",
            "时尚摄影",
            "product photo",
            "商业摄影",
            "exposure",
            "曝光",
            "焦距",
            "景深",
            "bokeh",
            "raw",
        ),
        (
            r"\bdsc\b",
            r"\bimg[_-]?\d+",
            r"\bportrait\b",
            r"\bstreet\b",
            r"\blandscape\b",
            r"\braw\b",
            r"\.cr2$",
            r"\.cr3$",
            r"\.arw$",
            r"\.nef$",
            r"\.dng$",
        ),
    ),
    Bucket(
        "painting-illustration",
        (
            "painting",
            "绘画",
            "画作",
            "illustration",
            "插画",
            "concept art",
            "概念设计",
            "oil painting",
            "油画",
            "watercolor",
            "水彩",
            "ink painting",
            "水墨",
            "国画",
            "艺术风格",
            "风格分析",
            "symbolism",
            "图像学",
            "cross-cultural",
            "跨文化",
            "ai art",
            "aigc",
        ),
        (
            r"\billustration\b",
            r"\bconcept[-_ ]?art\b",
            r"\bpainting\b",
            r"\boil\b",
            r"\bwatercolor\b",
            r"\bink\b",
        ),
    ),
    Bucket(
        "interior-design",
        (
            "interior",
            "室内",
            "室内设计",
            "space design",
            "空间",
            "客厅",
            "卧室",
            "餐厅",
            "办公室",
            "样板间",
            "render",
            "渲染图",
            "材质",
            "动线",
            "zoning",
            "lighting plan",
            "软装",
            "家具",
        ),
        (
            r"\binterior\b",
            r"\bliving[-_ ]?room\b",
            r"\bbedroom\b",
            r"\bkitchen\b",
            r"\boffice\b",
            r"\brender\b",
            r"\bfloorplan\b",
            r"\bspace\b",
        ),
    ),
    Bucket(
        "architecture-urban",
        (
            "architecture",
            "architectural",
            "建筑",
            "立面",
            "façade",
            "facade",
            "elevation",
            "tower",
            "skyscraper",
            "urban design",
            "urban",
            "cityscape",
            "streetscape",
            "plaza",
            "masterplan",
            "site plan",
            "公共空间",
            "城市设计",
            "街景",
            "楼体",
        ),
        (
            r"\bfacade\b",
            r"\belevation\b",
            r"\bmasterplan\b",
            r"\bsite[-_ ]?plan\b",
            r"\bbuilding\b",
            r"\btower\b",
            r"\bplaza\b",
            r"\burban\b",
        ),
    ),
    Bucket(
        "infographic-diagram",
        (
            "infographic",
            "信息图",
            "chart",
            "graph",
            "diagram",
            "flowchart",
            "流程图",
            "示意图",
            "map",
            "地图",
            "data visualization",
            "数据可视化",
            "schema",
            "schematic",
            "network diagram",
            "流程",
            "legend",
            "axis",
            "坐标轴",
        ),
        (
            r"\bchart\b",
            r"\bgraph\b",
            r"\bdiagram\b",
            r"\bflow\b",
            r"\bmap\b",
            r"\bschematic\b",
            r"\btopology\b",
        ),
    ),
    Bucket(
        "product-industrial-design",
        (
            "product design",
            "industrial design",
            "产品设计",
            "工业设计",
            "cmf",
            "prototype",
            "原型",
            "device",
            "产品外观",
            "ergonomic",
            "ergonomics",
            "manufacturing",
            "工艺",
            "材质工艺",
            "furniture object",
            "packaging structure",
            "包装结构",
            "rendered product",
            "object design",
        ),
        (
            r"\bprototype\b",
            r"\bdevice\b",
            r"\bproduct\b",
            r"\bcmf\b",
            r"\bpackaging[-_ ]?structure\b",
            r"\bmockup\b",
        ),
    ),
    Bucket(
        "comics-sequential",
        (
            "comic",
            "comics",
            "漫画",
            "条漫",
            "manga",
            "manhua",
            "webtoon",
            "panel",
            "panels",
            "speech bubble",
            "balloon",
            "caption box",
            "gutter",
            "顺序叙事",
            "分格",
            "页漫",
            "comic page",
            "strip",
        ),
        (
            r"\bcomic\b",
            r"\bmanga\b",
            r"\bwebtoon\b",
            r"\bpanel\b",
            r"\bstrip\b",
            r"\bcomic[-_ ]?page\b",
        ),
    ),
    Bucket(
        "fashion-styling",
        (
            "fashion",
            "styling",
            "outfit",
            "lookbook",
            "runway",
            "穿搭",
            "造型",
            "服装",
            "搭配",
            "配饰",
            "时装",
            "look",
            "editorial look",
            "beauty look",
        ),
        (
            r"\boutfit\b",
            r"\brunway\b",
            r"\blookbook\b",
            r"\bstyling\b",
            r"\bgarment\b",
        ),
    ),
    Bucket(
        "sculpture-installation-craft",
        (
            "sculpture",
            "installation",
            "ceramic",
            "craft",
            "assemblage",
            "雕塑",
            "装置",
            "陶艺",
            "手工艺",
            "工艺作品",
            "gallery piece",
            "site specific",
            "立体作品",
        ),
        (
            r"\bsculpture\b",
            r"\binstallation\b",
            r"\bceramic\b",
            r"\bassamblage\b",
            r"\bgallery\b",
        ),
    ),
    Bucket(
        "game-visual-design",
        (
            "game ui",
            "game screen",
            "gameplay",
            "hud",
            "inventory",
            "minimap",
            "character sheet",
            "游戏界面",
            "游戏画面",
            "游戏截图",
            "游戏美术",
            "关卡",
            "任务界面",
            "技能栏",
            "ui overlay",
        ),
        (
            r"\bhud\b",
            r"\bgameplay\b",
            r"\binventory\b",
            r"\bminimap\b",
            r"\bquest\b",
        ),
    ),
    Bucket(
        "scientific-medical-imaging",
        (
            "medical image",
            "scientific image",
            "x-ray",
            "ct",
            "mri",
            "ultrasound",
            "microscope",
            "pathology",
            "satellite",
            "remote sensing",
            "医学图像",
            "科研图",
            "显微图",
            "病理图",
            "遥感图",
            "实验图",
            "scan",
        ),
        (
            r"\bx[-_ ]?ray\b",
            r"\bct\b",
            r"\bmri\b",
            r"\bmicroscope\b",
            r"\bpathology\b",
            r"\bsatellite\b",
            r"\bscan\b",
        ),
    ),
    Bucket(
        "typography-lettering",
        (
            "typography",
            "lettering",
            "wordmark",
            "logotype",
            "calligraphy",
            "font proof",
            "字标",
            "字体设计",
            "排字",
            "书法",
            "字形",
            "字效",
            "type poster",
        ),
        (
            r"\btypography\b",
            r"\blettering\b",
            r"\bwordmark\b",
            r"\blogotype\b",
            r"\bcalligraphy\b",
            r"\bfont\b",
        ),
    ),
    Bucket(
        "presentation-document",
        (
            "presentation",
            "slide",
            "deck",
            "report page",
            "proposal",
            "executive summary",
            "ppt",
            "pptx",
            "汇报页",
            "报告页",
            "演示文稿",
            "幻灯片",
            "提案页",
            "文档页",
            "研究报告",
        ),
        (
            r"\bppt\b",
            r"\bslide\b",
            r"\bdeck\b",
            r"\breport\b",
            r"\bproposal\b",
            r"\bpptx\b",
        ),
    ),
    Bucket(
        "film-frame",
        (
            "film still",
            "movie still",
            "影视",
            "电影截图",
            "剧照",
            "frame",
            "shot",
            "scene",
            "分镜",
            "storyboard",
            "cinematic",
            "镜头语言",
            "构图镜头",
            "动画分镜",
            "anime frame",
        ),
        (
            r"\bstill\b",
            r"\bframe\b",
            r"\bscene\b",
            r"\bshot\b",
            r"\bstoryboard\b",
            r"\bsubtitle\b",
        ),
    ),
)


FOCUSES: tuple[Bucket, ...] = (
    Bucket(
        "learning-report",
        ("学习", "怎么学", "study", "learn", "拆解", "临摹", "练习", "improve"),
        (),
    ),
    Bucket(
        "style-classification",
        ("风格", "流派", "style", "genre", "归类", "属于什么"),
        (),
    ),
    Bucket(
        "technical-diagnosis",
        ("问题", "诊断", "technical", "曝光", "构图", "光线", "材质", "版式"),
        (),
    ),
    Bucket(
        "commercial-effectiveness",
        ("转化", "品牌", "传播", "cta", "受众", "营销", "广告"),
        (),
    ),
)


def normalize(parts: list[str]) -> str:
    return " ".join(part for part in parts if part).casefold()


def keyword_matches(keyword: str, corpus: str) -> bool:
    folded = keyword.casefold()
    if re.fullmatch(r"[a-z0-9_-]+", folded):
        pattern = rf"(?<![a-z0-9]){re.escape(folded)}(?![a-z0-9])"
        return re.search(pattern, corpus) is not None
    return folded in corpus


def score_bucket(bucket: Bucket, corpus: str, file_names: list[str]) -> dict[str, object]:
    matched: list[str] = []
    score = 0

    for keyword in bucket.keywords:
        if keyword_matches(keyword, corpus):
            matched.append(keyword)
            score += 2

    for pattern in bucket.filename_patterns:
        regex = re.compile(pattern, re.IGNORECASE)
        if any(regex.search(name) for name in file_names):
            matched.append(f"pattern:{pattern}")
            score += 3

    if bucket.name == "interior-design" and "render" in corpus and "interior" in corpus:
        score += 2
    if bucket.name == "film-frame" and "poster" in corpus:
        score -= 1
    if bucket.name == "architecture-urban" and "interior" in corpus:
        score -= 1
    if bucket.name == "product-industrial-design" and "广告" in corpus:
        score -= 1
    if bucket.name == "graphic-design" and "chart" in corpus:
        score -= 1
    if bucket.name == "film-frame" and "comic" in corpus:
        score -= 2
    if bucket.name == "fashion-styling" and "摄影" in corpus and "造型" not in corpus:
        score -= 1
    if bucket.name == "sculpture-installation-craft" and "产品" in corpus:
        score -= 1
    if bucket.name == "game-visual-design" and "电影" in corpus:
        score -= 1
    if bucket.name == "presentation-document" and "海报" in corpus:
        score -= 1
    if bucket.name == "typography-lettering" and "版式" in corpus:
        score -= 1

    return {"name": bucket.name, "score": score, "matched": matched}


def classify(prompt: str, files: list[str], hints: list[str]) -> dict[str, object]:
    corpus = normalize([prompt, *files, *hints])
    file_names = [name.casefold() for name in files]

    route_scores = [score_bucket(bucket, corpus, file_names) for bucket in ROUTES]
    route_scores.sort(key=lambda item: (-int(item["score"]), str(item["name"])))

    top = route_scores[0]
    runner_up = route_scores[1] if len(route_scores) > 1 else {"name": None, "score": 0}
    top_score = int(top["score"])
    top_ties = [item for item in route_scores if int(item["score"]) == top_score and top_score > 0]

    if top_score <= 0:
        top_route = "universal-fallback"
        confidence = "low"
    elif len(top_ties) > 1:
        top_route = "generic-mixed"
        confidence = "low"
    else:
        top_route = str(top["name"])
        gap = top_score - int(runner_up["score"])
        confidence = "high" if gap >= 4 else "medium" if gap >= 2 else "low"

    focus_scores = [score_bucket(bucket, corpus, file_names) for bucket in FOCUSES]
    focus_scores = [item for item in focus_scores if int(item["score"]) > 0]
    focus_scores.sort(key=lambda item: (-int(item["score"]), str(item["name"])))

    notes = [
        "Use the result as a routing prior only.",
        "Confirm the chosen route with actual visual inspection before writing the report.",
    ]
    if top_route == "universal-fallback":
        notes.append(
            "No named route scored above zero; use the universal fallback method and keep route guesses provisional."
        )
    elif top_route == "generic-mixed":
        tied_routes = ", ".join(str(item["name"]) for item in top_ties)
        notes.append(
            f"Multiple routes tie at the top ({tied_routes}); fall back to generic triage before committing."
        )
    elif confidence == "low":
        notes.append(
            f"Top route '{top_route}' is only weakly separated from '{runner_up['name']}'."
        )

    return {
        "top_route": top_route,
        "confidence": confidence,
        "route_scores": route_scores,
        "focus_scores": focus_scores,
        "notes": notes,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a routing prior for image-analysis-router."
    )
    parser.add_argument("--prompt", default="", help="User request or question.")
    parser.add_argument(
        "--file",
        dest="files",
        action="append",
        default=[],
        help="File name or path. Repeat for multiple files.",
    )
    parser.add_argument(
        "--hint",
        dest="hints",
        action="append",
        default=[],
        help="Optional OCR, caption, or metadata hint. Repeat as needed.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = classify(args.prompt, args.files, args.hints)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
