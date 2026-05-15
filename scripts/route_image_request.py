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
from pathlib import Path


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
            "room",
            "客厅",
            "卧室",
            "餐厅",
            "办公室",
            "样板间",
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
            r"\broom\b",
            r"\bliving[-_ ]?room\b",
            r"\bbedroom\b",
            r"\bkitchen\b",
            r"\boffice\b",
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
            "earbuds",
            "headphones",
            "shoes",
            "sneaker",
            "bottle",
            "watch",
            "chair",
            "appliance",
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
            r"\bearbuds?\b",
            r"\bheadphones?\b",
            r"\bshoe\b",
            r"\bsneaker\b",
            r"\bbottle\b",
            r"\bwatch\b",
            r"\bchair\b",
            r"\bappliance\b",
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
            r"\bassemblage\b",
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
            "dashboard",
            "dashboard report",
            "analytics dashboard",
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
            r"\bdashboard\b",
            r"\banalytics\b",
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


def _assert_routes_consistent() -> None:
    """references/routes.json is the single source for the route LIST.
    ROUTES (this file) holds the per-route scoring data. Names must match.

    Tolerates a missing or malformed routes.json — drift is only enforced when
    the file is loadable. The validator reports a separate error for malformed JSON.
    """
    routes_json = Path(__file__).resolve().parent.parent / "references" / "routes.json"
    if not routes_json.exists():
        return
    try:
        payload = json.loads(routes_json.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return  # malformed file is the validator's problem, not the router's
    declared = {bucket.name for bucket in ROUTES}
    expected_all = set(payload.get("routes", []))
    router_only_excludes = set(payload.get("router_only_excludes", []))
    expected_router = expected_all - router_only_excludes
    if expected_router and expected_router != declared:
        raise RuntimeError(
            f"Route drift: routes.json router-relevant={sorted(expected_router)}, "
            f"route_image_request.py ROUTES={sorted(declared)}"
        )


_assert_routes_consistent()


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

VISUAL_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".gif",
    ".tif",
    ".tiff",
    ".bmp",
    ".heic",
    ".heif",
    ".psd",
    ".ai",
    ".fig",
    ".sketch",
    ".dng",
    ".raw",
    ".cr2",
    ".cr3",
    ".arw",
    ".nef",
}

INSUFFICIENT_EVIDENCE_TERMS = (
    "看不清",
    "读不清",
    "无法辨认",
    "低清",
    "糊",
    "模糊",
    "裁切",
    "裁掉",
    "遮挡",
    "压缩",
    "马赛克",
    "分辨率太低",
    "low resolution",
    "low-res",
    "lowres",
    "blurry",
    "blurred",
    "cropped",
    "occluded",
    "blocked",
    "compressed",
    "unreadable",
)

AI_CONTENT_TERMS = (
    # Bare "ai" was removed because it matches .ai (Illustrator) filenames.
    # Use specific tool names or compound phrases instead.
    "aigc",
    "midjourney",
    "stable diffusion",
    "comfyui",
    "ai生成",
    "ai 生成",
    "ai-generated",
    "ai generated",
    "ai 出图",
    "真假",
    "生成感",
    "手指异常",
    "文字异常",
    "伪影",
)

MEDICAL_EVIDENCE_TERMS = (
    "x-ray",
    "xray",
    "ct",
    "mri",
    "ultrasound",
    "pathology",
    "microscope",
    "scan",
    "医学",
    "医疗",
    "诊断",
    "病理",
    "显微",
    "x 光",
    "x光",
)

DEEP_CUES = ("深入", "深度", "详细", "完整拆解", "怎么学", "临摹", "学习", "练习")
QUICK_CUES = ("简单", "快速", "快看", "一句话", "这是什么", "怎么样")


def normalize(parts: list[str]) -> str:
    return " ".join(part for part in parts if part).casefold()


def keyword_matches(keyword: str, corpus: str) -> bool:
    folded = keyword.casefold()
    if re.fullmatch(r"[a-z0-9_-]+", folded):
        pattern = rf"(?<![a-z0-9]){re.escape(folded)}(?![a-z0-9])"
        return re.search(pattern, corpus) is not None
    return folded in corpus


def has_any(corpus: str, terms: tuple[str, ...]) -> bool:
    return any(keyword_matches(term, corpus) for term in terms)


def compact_len(text: str) -> int:
    return len(re.sub(r"[\s，。！？,.!?：:；;、\"'`~\-_/\\()\[\]{}<>]+", "", text))


VISUAL_ATTACHED_PHRASES = (
    "image attached",
    "attached image",
    "screenshot attached",
    "attached screenshot",
    "see the attached",
    "视觉证据",
    "图片已附",
    "截图已附",
    "图像已附",
    "如图所示",
    "如图",
    "见图",
)


def has_visual_input(prompt: str, files: list[str], hints: list[str]) -> bool:
    # File path with a known visual extension counts; arbitrary names like notes.txt do not.
    for name in files or ():
        lower = name.lower()
        if any(lower.endswith(ext) for ext in VISUAL_EXTENSIONS):
            return True
    # The user may have attached an image without giving us the filename — accept hint and prompt mentions.
    combined = normalize([prompt, *(hints or [])])
    return has_any(combined, VISUAL_ATTACHED_PHRASES)


def visual_evidence_insufficient(corpus: str) -> bool:
    return has_any(corpus, INSUFFICIENT_EVIDENCE_TERMS)


def prompt_specificity(prompt: str, focus_scores: list[dict[str, object]]) -> str:
    prompt_corpus = normalize([prompt])
    prompt_route_scores = [score_bucket(bucket, prompt_corpus, []) for bucket in ROUTES]
    best_prompt_score = max(int(item["score"]) for item in prompt_route_scores)
    if (
        focus_scores
        or best_prompt_score >= 2
        or has_any(prompt_corpus, MEDICAL_EVIDENCE_TERMS)
        or has_any(prompt_corpus, ("主要", "不是", "按", "从", "对比", "主图", "参考图"))
    ):
        return "high"
    if compact_len(prompt) >= 15:
        return "medium"
    return "low"


def response_depth(prompt: str, focus_scores: list[dict[str, object]]) -> str:
    prompt_corpus = normalize([prompt])
    if has_any(prompt_corpus, DEEP_CUES):
        return "deep"
    if has_any(prompt_corpus, QUICK_CUES) or compact_len(prompt) < 15:
        return "quick"
    if focus_scores and str(focus_scores[0]["name"]) == "learning-report":
        return "deep"
    return "standard"


def study_report_mode(depth: str, focus_scores: list[dict[str, object]]) -> str:
    focus_names = {str(item["name"]) for item in focus_scores}
    if depth == "deep" or "learning-report" in focus_names:
        return "full"
    if depth == "quick" and "learning-report" not in focus_names:
        return "none"
    return "brief"


def score_bucket(bucket: Bucket, corpus: str, file_names: list[str]) -> dict[str, object]:
    matched: list[str] = []
    score = 0

    for keyword in bucket.keywords:
        if keyword_matches(keyword, corpus):
            matched.append(keyword)
            score += 2

    # Only score against the basename (not the directory path), so e.g.
    # /designs/posters/foo.png does not contribute "posters" to every route via path noise.
    basenames = [name.rsplit("/", 1)[-1].rsplit("\\", 1)[-1] for name in file_names]
    for pattern in bucket.filename_patterns:
        regex = re.compile(pattern, re.IGNORECASE)
        if any(regex.search(name) for name in basenames):
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


def apply_goal_adjustments(
    route_scores: list[dict[str, object]],
    prompt: str,
    corpus: str,
) -> None:
    prompt_corpus = normalize([prompt])

    def add(route: str, delta: int, reason: str) -> None:
        for item in route_scores:
            if item["name"] == route:
                item["score"] = int(item["score"]) + delta
                matched = list(item["matched"])
                matched.append(f"adjust:{reason}:{delta:+d}")
                item["matched"] = matched
                break

    photo_goal = has_any(prompt_corpus, ("摄影", "照片", "构图", "光线", "镜头", "曝光", "photo", "photography"))
    architecture_specific_goal = has_any(
        prompt_corpus,
        ("立面", "比例", "街道关系", "街道", "城市", "site", "facade", "massing", "public realm"),
    )
    architecture_goal = architecture_specific_goal or (
        has_any(prompt_corpus, ("建筑", "楼体")) and not photo_goal
    )
    commercial_layout_goal = has_any(
        prompt_corpus,
        ("广告", "海报", "转化", "说服力", "营销", "传播", "cta", "版式", "层级", "poster", "ad"),
    )
    product_form_goal = has_any(
        prompt_corpus,
        ("外观", "形态", "材质", "工艺", "结构", "人体工学", "cmf", "ergonomic", "material", "form"),
    )
    dashboard_goal = has_any(prompt_corpus, ("dashboard", "看板", "汇报页", "报告页", "数据屏", "经营页"))
    # D5: chart correctness / data encoding / misreading risk → infographic-diagram.
    # Use compound phrases or require an explicit data/chart cue alongside generic "可读性".
    data_correctness_goal = (
        has_any(prompt_corpus, ("数据编码", "误读", "chart correctness", "data encoding", "图表准确"))
        or (has_any(prompt_corpus, ("可读性",)) and has_any(prompt_corpus, ("图表", "chart", "数据", "data")))
    )
    # D4: explicit type-poster intent. Use compound phrases only to avoid catching
    # any "字体" / "字形" substring in unrelated copy.
    type_poster_goal = has_any(
        prompt_corpus,
        ("字体海报", "type poster", "字形海报", "lettering poster", "letterform"),
    )
    # D6: game menu / HUD UI. Require an explicit game context cue so bare "hud"
    # in a general UI critique doesn't reroute to game-visual-design.
    game_ui_goal = (
        has_any(prompt_corpus, ("游戏菜单", "游戏界面", "游戏ui", "战斗界面", "关卡界面", "副本界面", "技能栏", "背包界面"))
        or (has_any(prompt_corpus, ("hud",)) and has_any(prompt_corpus, ("游戏", "game", "gameplay", "副本", "关卡")))
    )

    if photo_goal and not architecture_specific_goal:
        add("photography", 6, "photo-goal")
        add("architecture-urban", -2, "photo-goal")
    if architecture_goal:
        add("architecture-urban", 5, "architecture-goal")
    # "海报" alone triggers commercial-layout-goal, but a "字体海报" should not — typography wins.
    if commercial_layout_goal and not type_poster_goal:
        add("graphic-design", 5, "commercial-layout-goal")
        add("product-industrial-design", -2, "commercial-layout-goal")
        add("scientific-medical-imaging", -2, "commercial-layout-goal")
    if product_form_goal and not commercial_layout_goal:
        add("product-industrial-design", 5, "product-form-goal")
    if dashboard_goal and not data_correctness_goal:
        add("presentation-document", 5, "dashboard-report-goal")
        add("graphic-design", -1, "dashboard-report-goal")
    # data-correctness-goal must not steal from scientific-medical-imaging when the corpus
    # contains medical evidence terms ("可读性" also appears in the medical-evidence heuristic).
    medical_present = has_any(corpus, MEDICAL_EVIDENCE_TERMS)
    if data_correctness_goal and not medical_present:
        add("infographic-diagram", 6, "data-correctness-goal")
        add("presentation-document", -2, "data-correctness-goal")
    if type_poster_goal:
        # Type-poster intent must beat the generic commercial-layout-goal that also fires on "海报".
        add("typography-lettering", 9, "type-poster-goal")
        add("graphic-design", -4, "type-poster-goal")
    if game_ui_goal:
        add("game-visual-design", 6, "game-ui-goal")
        add("graphic-design", -2, "game-ui-goal")
    if has_any(corpus, MEDICAL_EVIDENCE_TERMS) and has_any(
        prompt_corpus, ("诊断", "标注", "可读性", "医学", "科研", "evidence", "interpretability")
    ):
        add("scientific-medical-imaging", 4, "medical-evidence-goal")


def score_routes(prompt: str, files: list[str], hints: list[str]) -> list[dict[str, object]]:
    corpus = normalize([prompt, *files, *hints])
    file_names = [name.casefold() for name in files]
    route_scores = [score_bucket(bucket, corpus, file_names) for bucket in ROUTES]
    apply_goal_adjustments(route_scores, prompt, corpus)
    route_scores.sort(key=lambda item: (-int(item["score"]), str(item["name"])))
    return route_scores


def choose_route(route_scores: list[dict[str, object]]) -> tuple[str, str, list[dict[str, object]]]:
    top = route_scores[0]
    runner_up = route_scores[1] if len(route_scores) > 1 else {"name": None, "score": 0}
    top_score = int(top["score"])
    top_cluster = [
        item for item in route_scores if top_score > 0 and int(item["score"]) >= 4 and top_score - int(item["score"]) <= 1
    ]

    if top_score <= 1:
        top_route = "universal-fallback"
        route_confidence = "low"
    elif len(top_cluster) > 1:
        top_route = "generic-mixed"
        route_confidence = "low"
    else:
        top_route = str(top["name"])
        gap = top_score - int(runner_up["score"])
        route_confidence = "high" if gap >= 4 else "medium" if gap >= 2 else "low"
    return top_route, route_confidence, top_cluster


def score_focuses(prompt: str, files: list[str], hints: list[str]) -> list[dict[str, object]]:
    corpus = normalize([prompt, *files, *hints])
    file_names = [name.casefold() for name in files]
    focus_scores = [score_bucket(bucket, corpus, file_names) for bucket in FOCUSES]
    focus_scores = [item for item in focus_scores if int(item["score"]) > 0]
    focus_scores.sort(key=lambda item: (-int(item["score"]), str(item["name"])))
    return focus_scores


def classify_one(prompt: str, file_name: str, hints: list[str]) -> dict[str, object]:
    route_scores = score_routes(prompt, [file_name], hints)
    top_route, route_confidence, _ = choose_route(route_scores)
    return {
        "file": file_name,
        "top_route": top_route,
        "route_confidence": route_confidence,
        "score": int(route_scores[0]["score"]),
        "route_scores": route_scores[:5],
    }


def detect_batch_type(prompt: str, files: list[str], image_routes: list[dict[str, object]]) -> str:
    prompt_corpus = normalize([prompt, *files])
    if not files and has_any(prompt_corpus, ("这组", "几张", "多张", "对比", "before", "after", "reference")):
        return "unknown"
    if len(files) <= 1:
        return "single"
    if has_any(prompt_corpus, ("before", "after", "前后", "改前", "改后", "v1", "v2", "version", "版本")):
        return "versioned"
    if has_any(prompt_corpus, ("moodboard", "mood board", "参考包", "灵感", "风格板", "reference pack")):
        return "reference_pack"
    # D3: subject_vs_reference requires BOTH a subject role cue AND a reference role cue;
    # "主视觉" is a graphic-design keyword (key visual), not a subject role marker — excluded.
    subject_cue = has_any(prompt_corpus, ("主图", "以第一张", "对标", "anchor", "我的图", "我这张"))
    reference_cue = has_any(prompt_corpus, ("参考图", "reference image", "参考图对比", "reference pack"))
    if subject_cue and reference_cue:
        return "subject_vs_reference"
    if reference_cue or has_any(prompt_corpus, ("参考图", "reference")):
        return "reference_pack"
    stable_routes = {
        str(item["top_route"])
        for item in image_routes
        if item["top_route"] not in {"universal-fallback", "generic-mixed", None}
        and item["route_confidence"] in {"medium", "high"}
    }
    if len(stable_routes) > 1:
        return "mixed_domain"
    if len(stable_routes) == 1:
        return "same_series"
    return "unknown"


def batch_size_rule(files: list[str], batch_type: str) -> str:
    if batch_type == "single":
        return "single"
    count = len(files)
    if count == 0:
        return "visual-inspection-required"
    if count == 2:
        return "ab-difference"
    if 3 <= count <= 5:
        return "standard-batch"
    return "grouped-batch"


def confidence_summary(status: str, route_confidence: str, intent_confidence: str) -> str:
    if status != "ok":
        return "low"
    if "low" in {route_confidence, intent_confidence}:
        return "low"
    if "medium" in {route_confidence, intent_confidence}:
        return "medium"
    return "high"


def classify(prompt: str, files: list[str], hints: list[str]) -> dict[str, object]:
    corpus = normalize([prompt, *files, *hints])
    route_scores = score_routes(prompt, files, hints)
    focus_scores = score_focuses(prompt, files, hints)
    top_route, route_confidence, top_cluster = choose_route(route_scores)
    intent_confidence = prompt_specificity(prompt, focus_scores)
    depth = response_depth(prompt, focus_scores)
    image_routes = [classify_one(prompt, file_name, hints) for file_name in files]
    batch_type = detect_batch_type(prompt, files, image_routes)

    status = "ok"
    if not has_visual_input(prompt, files, hints):
        status = "visual_input_missing"
        top_route = None
        route_confidence = "low"
    elif visual_evidence_insufficient(corpus):
        status = "visual_evidence_insufficient"
        top_route = None
        route_confidence = "low"
    elif (
        # Original case: generic-mixed on a single image with unclear intent.
        batch_type in {"single", "unknown"}
        and top_route == "generic-mixed"
        and intent_confidence == "low"
    ):
        status = "needs_clarification"
    elif (
        # D1 broaden: two strong route scores tied AND intent ambiguous on a non-batch input.
        batch_type in {"single", "unknown"}
        and route_confidence == "low"
        and intent_confidence == "low"
        and len(route_scores) >= 2
        and int(route_scores[0].get("score", 0)) >= 4
        and int(route_scores[1].get("score", 0)) >= 4
        and int(route_scores[0].get("score", 0)) - int(route_scores[1].get("score", 0)) <= 1
    ):
        status = "needs_clarification"

    confidence = confidence_summary(status, route_confidence, intent_confidence)

    notes = [
        "Use the result as a routing prior only.",
        "Confirm the chosen route with actual visual inspection before writing the report.",
    ]
    if status == "visual_input_missing":
        notes.append("No visual input was provided to the router; ask upstream for image evidence.")
    elif status == "visual_evidence_insufficient":
        notes.append("Visual evidence appears too limited to route reliably; do not force fallback.")
    elif status == "needs_clarification":
        notes.append("The image can be read, but the user's intended lens is unclear enough to ask first.")
    elif top_route == "universal-fallback":
        notes.append(
            "No named route scored above zero; use the universal-fallback method and keep route guesses provisional."
        )
    elif top_route == "generic-mixed":
        tied_routes = ", ".join(str(item["name"]) for item in top_cluster)
        notes.append(
            f"Multiple routes tie at the top ({tied_routes}); use generic-mixed triage before committing."
        )
    elif route_confidence == "low":
        runner_up = route_scores[1] if len(route_scores) > 1 else {"name": None}
        notes.append(
            f"Top route '{top_route}' is only weakly separated from '{runner_up['name']}'."
        )

    if batch_type != "single":
        notes.append(f"Batch type prior: {batch_type}; verify count and grouping visually.")

    # Only surface routes/focuses that actually scored above 0 as clarification options.
    # When no route scored (e.g. image missing entirely), return an empty routes list
    # rather than the alphabetic first-three (which had no visible evidence behind them).
    scored_routes = [str(item["name"]) for item in route_scores if int(item.get("score", 0)) > 0][:3]
    scored_focuses = [str(item["name"]) for item in focus_scores if int(item.get("score", 0)) > 0][:3]
    clarification_options = {
        "routes": scored_routes,
        "focuses": scored_focuses or [
            "learning-report",
            "style-classification",
            "technical-diagnosis",
            "commercial-effectiveness",
        ],
    }

    medical_safety = has_any(corpus, MEDICAL_EVIDENCE_TERMS)
    # D2: three tiers matching references/_ai-content-check.md
    # - "stated":  the corpus explicitly says the image IS AI-generated
    # - "visible": the corpus names visible artifact signals worth checking
    # - "not_indicated": nothing in the corpus points at AI generation
    ai_stated_phrases = (
        "ai-generated", "ai generated", "midjourney 生成", "sd 生成", "comfyui 生成",
        "ai 出图", "ai生成的", "这是 ai", "this is ai", "by midjourney", "by stable diffusion",
    )
    ai_visible_signal_phrases = (
        "手指异常", "断指", "畸形", "纹理重复", "边缘", "反光异常", "文字异常",
        "broken text", "extra finger", "edge artifact", "uncanny",
    )
    if has_any(corpus, ai_stated_phrases):
        ai_content_check = "stated"
    elif has_any(corpus, ai_visible_signal_phrases):
        ai_content_check = "visible"
    elif has_any(corpus, AI_CONTENT_TERMS):
        ai_content_check = "visible"  # generic AI mention without explicit "stated" or specific signal
    else:
        ai_content_check = "not_indicated"

    return {
        "status": status,
        "top_route": top_route,
        "confidence": confidence,
        "route_confidence": route_confidence,
        "intent_confidence": intent_confidence,
        "response_depth": depth,
        "study_report_mode": study_report_mode(depth, focus_scores),
        "batch_type": batch_type,
        "batch_size_rule": batch_size_rule(files, batch_type),
        "medical_safety": medical_safety,
        "ai_content_check": ai_content_check,
        "clarification_options": clarification_options,
        "image_routes": image_routes,
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
    parser.add_argument(
        "--source-note-path",
        dest="source_note_path",
        default="",
        help="Path to a source note created by FastNote (informational; not used by the keyword router).",
    )
    parser.add_argument(
        "--source-url",
        dest="source_urls",
        action="append",
        default=[],
        help="Source URL(s) for the image (informational).",
    )
    parser.add_argument(
        "--attachment",
        dest="attachments",
        action="append",
        default=[],
        help="Local attachment path; treated like --file for routing.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress route_scores/focus_scores/image_routes from output.",
    )
    parser.add_argument(
        "--strict-files",
        action="store_true",
        help="If set, require every --file/--attachment path to exist on disk.",
    )
    parser.add_argument(
        "--strict-exit",
        action="store_true",
        help="If set, exit non-zero on blocking statuses (10/11/12). Default: always exit 0.",
    )
    return parser.parse_args()


QUIET_FIELDS = (
    "status",
    "top_route",
    "confidence",
    "route_confidence",
    "intent_confidence",
    "response_depth",
    "study_report_mode",
    "batch_type",
    "batch_size_rule",
    "medical_safety",
    "ai_content_check",
    "clarification_options",
)

# Process exit codes: 0 = ok routing. Non-zero codes give callers a machine-readable
# distinction between blocking conditions without parsing JSON.
STATUS_EXIT_CODES = {
    "ok": 0,
    "needs_clarification": 10,
    "visual_evidence_insufficient": 11,
    "visual_input_missing": 12,
}


def main() -> int:
    args = parse_args()
    # --attachment is just an extra --file (kept separate so the CLI labels stay clear).
    merged_files = list(args.files) + list(args.attachments)
    if args.strict_files:
        from pathlib import Path as _P
        missing = [p for p in merged_files if p and not _P(p).exists()]
        if missing:
            print(json.dumps({
                "status": "visual_input_missing",
                "blocked_step": "file-check",
                "blocked_reason": f"missing file(s): {missing}",
            }, ensure_ascii=False))
            return STATUS_EXIT_CODES["visual_input_missing"] if args.strict_exit else 0
    result = classify(args.prompt, merged_files, args.hints)
    if args.source_note_path:
        result["source_note_path"] = args.source_note_path
    if args.source_urls:
        result["source_urls"] = args.source_urls
    if args.quiet:
        result = {k: result.get(k) for k in QUIET_FIELDS if k in result}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not args.strict_exit:
        return 0
    return STATUS_EXIT_CODES.get(str(result.get("status", "ok")), 0)


if __name__ == "__main__":
    import sys as _sys
    _sys.exit(main())
