"""Drain Touch Map Engine v0.1.

Converts source fragments into business objects, table touch maps,
change hints, metrics, and Reality Ledger style receipts.

This is intentionally dependency-light so it can run in local, Lambda,
worker, or Bridge contexts without waiting for a framework.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional


STATUS_REAL = "REAL"
STATUS_PARTIAL = "PARTIAL"
STATUS_BLOCKED = "BLOCKED"

DOMAIN_KEYWORDS = {
    "product": ["product", "offer", "package", "reading buddy", "outcome ready", "workfamily", "myneuralsignal"],
    "brand": ["brand", "site", "campaign", "identity", "logo"],
    "legal": ["legal", "consent", "privacy", "terms", "compliance", "obligation", "policy"],
    "documentation": ["readme", "document", "spec", "vignette", "manual", "guide"],
    "operations": ["workflow", "process", "pod", "handoff", "runbook", "operating"],
    "research": ["research", "paper", "study", "evidence", "atlas"],
    "sales": ["pricing", "revenue", "funnel", "cta", "customer", "monetise", "monetize"],
    "engineering": ["repo", "github", "route", "package", "api", "schema", "supabase", "vercel"],
    "widget": ["widget", "dashboard", "command centre", "surface"],
    "evidence": ["hash", "receipt", "ledger", "timestamp", "proof", "REAL", "PARTIAL", "BLOCKED"],
    "finance": ["cost", "margin", "budget", "invoice", "payment", "roi"],
}

OBJECT_PATTERNS = {
    "table_candidate": re.compile(r"\b([a-z][a-z0-9_]*_(?:registry|map|ledger|metrics|objects|sources|runs|receipts|changes|candidates))\b", re.I),
    "repo": re.compile(r"\b([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)\b"),
    "route": re.compile(r"(?<!\w)/(?:[a-zA-Z0-9_./-]+)"),
    "url": re.compile(r"https?://[^\s)]+"),
}

KNOWN_PRODUCTS = [
    "Reading Buddy",
    "Outcome Ready",
    "WorkFamilyAI",
    "MyNeuralSignal",
    "LifeGraph+",
    "ConsentX",
    "Holo-Org",
    "RATPAK",
    "NEUROPAK",
    "Command Centre",
    "Drain",
]


@dataclass
class Source:
    source_type: str
    source_uri: str
    content: str
    title: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DrainObject:
    object_type: str
    object_name: str
    object_summary: str
    extraction_confidence: float
    raw_excerpt: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Touch:
    touched_domain: str
    touched_table: str
    touched_entity: str
    touch_type: str
    confidence: float
    rationale: str


@dataclass
class DrainResult:
    run_key: str
    status: str
    score: float
    sources: List[Dict[str, Any]]
    objects: List[Dict[str, Any]]
    touches: List[Dict[str, Any]]
    table_candidates: List[str]
    metrics: Dict[str, int]
    evidence: List[Dict[str, Any]]
    gaps: List[str]
    next_action: str
    created_at: str


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def run_key_for_sources(sources: Iterable[Source]) -> str:
    payload = "|".join(f"{s.source_type}:{s.source_uri}:{content_hash(s.content)}" for s in sources)
    return "drain-" + content_hash(payload)[:16]


def excerpt(text: str, max_len: int = 280) -> str:
    cleaned = re.sub(r"\s+", " ", text).strip()
    return cleaned[:max_len]


def detect_objects(source: Source) -> List[DrainObject]:
    text = source.content
    lower = text.lower()
    objects: List[DrainObject] = []

    for product in KNOWN_PRODUCTS:
        if product.lower() in lower:
            objects.append(DrainObject(
                object_type="product",
                object_name=product,
                object_summary=f"Detected reference to {product} in {source.source_uri}.",
                extraction_confidence=0.88,
                raw_excerpt=excerpt(text),
                metadata={"source_uri": source.source_uri},
            ))

    for object_type, pattern in OBJECT_PATTERNS.items():
        for match in pattern.findall(text):
            value = match.rstrip(".,;)")
            objects.append(DrainObject(
                object_type=object_type,
                object_name=value,
                object_summary=f"Detected {object_type.replace('_', ' ')}: {value}.",
                extraction_confidence=0.76,
                raw_excerpt=excerpt(text),
                metadata={"source_uri": source.source_uri},
            ))

    for phrase in ["pricing", "revenue", "funnel", "legal", "consent", "evidence", "widget", "dashboard", "pod", "route", "schema"]:
        if phrase in lower:
            objects.append(DrainObject(
                object_type="concept",
                object_name=phrase,
                object_summary=f"Detected operational concept: {phrase}.",
                extraction_confidence=0.68,
                raw_excerpt=excerpt(text),
                metadata={"source_uri": source.source_uri},
            ))

    dedup: Dict[str, DrainObject] = {}
    for obj in objects:
        key = f"{obj.object_type}:{obj.object_name.lower()}"
        dedup[key] = obj
    return list(dedup.values())


def map_touches(objects: List[DrainObject]) -> List[Touch]:
    touches: List[Touch] = []
    for obj in objects:
        haystack = f"{obj.object_type} {obj.object_name} {obj.object_summary} {obj.raw_excerpt}".lower()
        for domain, keywords in DOMAIN_KEYWORDS.items():
            matched = [kw for kw in keywords if kw.lower() in haystack]
            if matched:
                table = f"{domain}_registry" if domain not in {"evidence", "engineering"} else ("reality_ledger" if domain == "evidence" else "repo_registry")
                touches.append(Touch(
                    touched_domain=domain,
                    touched_table=table,
                    touched_entity=obj.object_name,
                    touch_type="updates" if obj.object_type != "table_candidate" else "creates",
                    confidence=min(0.95, 0.62 + 0.07 * len(matched)),
                    rationale=f"Matched keywords: {', '.join(matched[:5])}.",
                ))
    unique: Dict[str, Touch] = {}
    for touch in touches:
        key = f"{touch.touched_domain}:{touch.touched_table}:{touch.touched_entity}:{touch.touch_type}"
        unique[key] = touch
    return list(unique.values())


def table_candidates(objects: List[DrainObject], touches: List[Touch]) -> List[str]:
    candidates = {obj.object_name.lower() for obj in objects if obj.object_type == "table_candidate"}
    candidates.update(t.touched_table for t in touches)
    candidates.update([
        "drain_runs",
        "drain_sources",
        "drain_objects",
        "drain_touch_map",
        "drain_daily_metrics",
        "drain_receipts",
    ])
    return sorted(candidates)


def score_result(objects: List[DrainObject], touches: List[Touch], candidates: List[str]) -> float:
    raw = 0.45
    raw += min(0.2, len(objects) * 0.01)
    raw += min(0.2, len(touches) * 0.01)
    raw += min(0.1, len(candidates) * 0.005)
    return round(min(0.92, raw), 2)


def run_drain(sources: List[Source]) -> DrainResult:
    run_key = run_key_for_sources(sources)
    all_objects: List[DrainObject] = []
    evidence: List[Dict[str, Any]] = []
    source_payloads: List[Dict[str, Any]] = []

    for source in sources:
        digest = content_hash(source.content)
        source_payloads.append({
            "source_type": source.source_type,
            "source_uri": source.source_uri,
            "source_title": source.title,
            "content_hash": digest,
            "metadata": source.metadata,
        })
        evidence.append({
            "type": "hash",
            "source_uri": source.source_uri,
            "sha256": digest,
            "captured_at": utc_now(),
        })
        all_objects.extend(detect_objects(source))

    touches = map_touches(all_objects)
    candidates = table_candidates(all_objects, touches)
    score = score_result(all_objects, touches, candidates)
    status = STATUS_PARTIAL if sources and all_objects and touches else STATUS_BLOCKED
    gaps: List[str] = []

    if not sources:
        gaps.append("No sources supplied.")
    if not all_objects:
        gaps.append("No semantic objects extracted.")
    if not touches:
        gaps.append("No table touch map generated.")
    gaps.extend([
        "Not yet writing to Supabase.",
        "Not yet rendering Command Centre widget.",
        "Not yet executing markdown-crawler adapter.",
    ])

    metrics = {
        "sources_crawled": len(sources),
        "objects_extracted": len(all_objects),
        "tables_touched": len({t.touched_table for t in touches}),
        "new_tables_proposed": len(candidates),
        "risks_found": sum(1 for o in all_objects if "risk" in o.object_name.lower()),
        "revenue_paths_found": sum(1 for t in touches if t.touched_domain in {"sales", "finance"}),
        "unfinished_work_recovered": sum(1 for o in all_objects if "todo" in o.raw_excerpt.lower() or "gap" in o.raw_excerpt.lower()),
        "partial_items": 1 if status == STATUS_PARTIAL else 0,
        "blocked_items": 1 if status == STATUS_BLOCKED else 0,
        "real_promotions": 0,
    }

    return DrainResult(
        run_key=run_key,
        status=status,
        score=score,
        sources=source_payloads,
        objects=[asdict(o) for o in all_objects],
        touches=[asdict(t) for t in touches],
        table_candidates=candidates,
        metrics=metrics,
        evidence=evidence,
        gaps=gaps,
        next_action="Connect runtime output to Supabase writer and Command Centre Drain dashboard.",
        created_at=utc_now(),
    )


def run_from_json(payload: Dict[str, Any]) -> Dict[str, Any]:
    sources = [Source(**item) for item in payload.get("sources", [])]
    return asdict(run_drain(sources))


if __name__ == "__main__":
    import sys

    payload = json.load(sys.stdin)
    print(json.dumps(run_from_json(payload), indent=2, sort_keys=True))
