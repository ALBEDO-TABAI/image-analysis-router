#!/usr/bin/env python3
"""Structural and routing validation for image-analysis-router."""

from __future__ import annotations

import json
import shutil
import sys
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

def _load_required_routes() -> set[str]:
    path = ROOT / "references" / "routes.json"
    if not path.exists():
        return set()
    try:
        return set(json.loads(path.read_text(encoding="utf-8")).get("routes", []))
    except json.JSONDecodeError as exc:
        # Surface as a check-time error rather than crashing module import.
        print(f"ERROR: references/routes.json is malformed JSON: {exc}", file=sys.stderr)
        return set()


_FALLBACK_REQUIRED_ROUTES = {
    "graphic-design",
    "photography",
    "painting-illustration",
    "interior-design",
    "architecture-urban",
    "infographic-diagram",
    "product-industrial-design",
    "comics-sequential",
    "fashion-styling",
    "sculpture-installation-craft",
    "game-visual-design",
    "scientific-medical-imaging",
    "typography-lettering",
    "presentation-document",
    "film-frame",
    "generic-mixed",
    "universal-fallback",
}

REQUIRED_ROUTES = _load_required_routes() or _FALLBACK_REQUIRED_ROUTES

CONFIDENCE_ORDER = {"low": 0, "medium": 1, "high": 2}
STANDARD_METHOD_SECTIONS = (
    "## Evidence ladder",
    "## Core lenses",
    "## Common failure patterns",
    "## Study report emphasis",
)
REQUIRED_RESULT_FIELDS = (
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
    "image_routes",
)


_ROUTER_MODULE = None


def load_router():
    global _ROUTER_MODULE
    if _ROUTER_MODULE is not None:
        return _ROUTER_MODULE
    path = ROOT / "scripts" / "route_image_request.py"
    spec = spec_from_file_location("route_image_request", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load route_image_request.py")
    module = module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    _ROUTER_MODULE = module
    return module


def check_required_files(errors: list[str]) -> None:
    required = [
        "SKILL.md",
        "references/route-matrix.md",
        "references/output-contract.md",
        "references/method-batch-handling.md",
        "references/_ai-content-check.md",
        "references/examples.md",
        "references/routes.json",
        "scripts/route_image_request.py",
        "evals/evals.json",
    ]
    for route in REQUIRED_ROUTES:
        required.append(f"references/method-{route}.md")
    for relative in required:
        if not (ROOT / relative).exists():
            errors.append(f"Missing required file: {relative}")


def check_route_consistency(errors: list[str]) -> None:
    method_routes = {
        path.stem.removeprefix("method-")
        for path in (ROOT / "references").glob("method-*.md")
        if path.stem != "method-batch-handling"
    }
    if method_routes != REQUIRED_ROUTES:
        errors.append(
            "Method route set mismatch: "
            f"missing={sorted(REQUIRED_ROUTES - method_routes)}, extra={sorted(method_routes - REQUIRED_ROUTES)}"
        )

    router = load_router()
    script_routes = {bucket.name for bucket in router.ROUTES}
    expected_script_routes = REQUIRED_ROUTES - {"generic-mixed", "universal-fallback"}
    if script_routes != expected_script_routes:
        errors.append(
            "Router route set mismatch: "
            f"missing={sorted(expected_script_routes - script_routes)}, extra={sorted(script_routes - expected_script_routes)}"
        )

    route_matrix = (ROOT / "references" / "route-matrix.md").read_text(encoding="utf-8")
    for route in REQUIRED_ROUTES:
        if f"`{route}`" not in route_matrix:
            errors.append(f"route-matrix.md does not mention route: {route}")


def check_method_structure(errors: list[str]) -> None:
    for path in sorted((ROOT / "references").glob("method-*.md")):
        route = path.stem.removeprefix("method-")
        if route == "batch-handling":
            continue
        text = path.read_text(encoding="utf-8")
        if route not in {"generic-mixed", "universal-fallback"}:
            for section in STANDARD_METHOD_SECTIONS:
                if section not in text:
                    errors.append(f"{path.relative_to(ROOT)} is missing section: {section}")
        for section in ("## Route-specific failure modes", "## Actionable drill format"):
            if section not in text:
                errors.append(f"{path.relative_to(ROOT)} is missing section: {section}")
        if "Do:" not in text or "Finish:" not in text:
            errors.append(f"{path.relative_to(ROOT)} drill format must include Do: and Finish:")


def check_continuity_contracts(errors: list[str]) -> None:
    skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    route_text = (ROOT / "references" / "route-matrix.md").read_text(encoding="utf-8")
    output_text = (ROOT / "references" / "output-contract.md").read_text(encoding="utf-8")
    ai_text = (ROOT / "references" / "_ai-content-check.md").read_text(encoding="utf-8")
    batch_text = (ROOT / "references" / "method-batch-handling.md").read_text(encoding="utf-8")

    required_skill_snippets = (
        "visual_input_missing",
        "visual_evidence_insufficient",
        "needs_clarification",
        "intent_confidence",
        "response_depth",
        "_ai-content-check.md",
        "method-batch-handling.md",
    )
    for snippet in required_skill_snippets:
        if snippet not in skill_text:
            errors.append(f"SKILL.md is missing contract snippet: {snippet}")

    required_route_snippets = (
        "Status gate",
        "generic-mixed",
        "universal-fallback",
        "Batch type rules",
        "visual_evidence_insufficient",
    )
    for snippet in required_route_snippets:
        if snippet not in route_text:
            errors.append(f"route-matrix.md is missing rule snippet: {snippet}")

    required_output_snippets = (
        "Blocking States",
        "Evidence Tone",
        "AI Content Check",
        "Scientific and Medical Safety",
        "visual_input_missing",
        "visual_evidence_insufficient",
        "needs_clarification",
        "what counts as finished",
        "subject-vs-reference",
    )
    for snippet in required_output_snippets:
        if snippet not in output_text:
            errors.append(f"output-contract.md is missing contract snippet: {snippet}")

    for snippet in ("Evidence levels", "Common visible signals", "Do not turn this into a forensic verdict"):
        if snippet not in ai_text:
            errors.append(f"_ai-content-check.md is missing snippet: {snippet}")

    for snippet in ("same_series", "versioned", "reference_pack", "subject_vs_reference", "mixed_domain", "Size rules"):
        if snippet not in batch_text:
            errors.append(f"method-batch-handling.md is missing snippet: {snippet}")


def check_eval_coverage(evals: list[dict[str, object]], errors: list[str]) -> None:
    if len(evals) < 15:
        errors.append(f"Expected at least 15 image router evals, found {len(evals)}")
    covered_routes = {item.get("expected_route") for item in evals if item.get("expected_route")}
    important_routes = {
        "graphic-design",
        "photography",
        "architecture-urban",
        "product-industrial-design",
        "presentation-document",
        "scientific-medical-imaging",
        "generic-mixed",
        "universal-fallback",
    }
    missing = important_routes - covered_routes
    if missing:
        errors.append(f"Missing eval coverage for important routes: {sorted(missing)}")
    for field in ("expected_status", "expected_batch_type", "expected_response_depth"):
        if not any(field in item for item in evals):
            errors.append(f"Missing eval coverage field: {field}")


def expect_equal(errors: list[str], prefix: str, result: dict[str, object], key: str, expected: object) -> None:
    if key in result and result.get(key) == expected:
        return
    errors.append(f"{prefix}: expected {key}={expected}, got {result.get(key)}")


def run_router_evals(errors: list[str]) -> None:
    router = load_router()
    data = json.loads((ROOT / "evals" / "evals.json").read_text(encoding="utf-8"))
    evals = data.get("evals", [])
    check_eval_coverage(evals, errors)

    for item in evals:
        result = router.classify(
            item.get("prompt", ""),
            item.get("files", []),
            item.get("hints", []),
        )
        prefix = f"Eval {item.get('id')} ({item.get('name', 'unnamed')})"

        for field in REQUIRED_RESULT_FIELDS:
            if field not in result:
                errors.append(f"{prefix}: router result missing field {field}")

        checks = {
            "expected_route": "top_route",
            "expected_status": "status",
            "expected_confidence": "confidence",
            "expected_route_confidence": "route_confidence",
            "expected_intent_confidence": "intent_confidence",
            "expected_batch_type": "batch_type",
            "expected_response_depth": "response_depth",
            "expected_study_report_mode": "study_report_mode",
            "expected_medical_safety": "medical_safety",
            "expected_ai_content_check": "ai_content_check",
        }
        for expected_key, result_key in checks.items():
            if expected_key in item:
                expect_equal(errors, prefix, result, result_key, item[expected_key])

        min_confidence = item.get("min_confidence")
        if min_confidence:
            actual = str(result.get("confidence"))
            if CONFIDENCE_ORDER.get(actual, -1) < CONFIDENCE_ORDER[min_confidence]:
                errors.append(f"{prefix}: expected confidence >= {min_confidence}, got {actual}")


def clean_pycache() -> None:
    for path in ROOT.rglob("__pycache__"):
        shutil.rmtree(path)


def _safe_run(label: str, fn, errors: list[str]) -> None:
    try:
        fn(errors)
    except FileNotFoundError as exc:
        errors.append(f"{label}: missing dependency file: {exc}")
    except Exception as exc:  # noqa: BLE001
        errors.append(f"{label}: unexpected error: {exc!r}")


def report_manual_checks() -> None:
    """E2: surface evals manual_checks / clarification fields as TODO output."""
    evals_path = ROOT / "evals" / "evals.json"
    if not evals_path.exists():
        return
    try:
        data = json.loads(evals_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return
    todos = []
    for item in data.get("evals", []):
        manual = item.get("manual_checks")
        if manual:
            todos.append((item.get("id"), item.get("name"), manual))
    if todos:
        print("INFO: manual_checks (require LLM/human review, not auto-validated):")
        for id_, name, items in todos:
            print(f"TODO  Eval {id_} ({name}):")
            for line in items:
                print(f"TODO    - {line}")


def main() -> None:
    errors: list[str] = []
    try:
        check_required_files(errors)
        _safe_run("route_consistency", check_route_consistency, errors)
        _safe_run("method_structure", check_method_structure, errors)
        _safe_run("continuity_contracts", check_continuity_contracts, errors)
        _safe_run("router_evals", run_router_evals, errors)
    finally:
        clean_pycache()

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)

    report_manual_checks()
    print("image-analysis-router validation passed")


if __name__ == "__main__":
    main()
