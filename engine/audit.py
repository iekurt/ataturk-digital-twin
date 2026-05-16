import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional


PROJECT_NAME = "ATATÜRK DIGITAL TWIN / HOPEVERSE"
AUDIT_DIR = Path(os.getenv("HOPE_AUDIT_DIR", "data/audit"))
AUDIT_FILE = AUDIT_DIR / "cognition_audit.jsonl"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_audit_dir() -> None:
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)


def safe_len(value: Any) -> int:
    if value is None:
        return 0
    return len(str(value))


def extract_reasoning_mode(payload: Dict[str, Any]) -> str:
    return str(
        payload.get("reasoning_mode")
        or payload.get("reasoningMode")
        or payload.get("mode")
        or "balanced"
    ).strip().lower()


def extract_prompt(payload: Dict[str, Any]) -> str:
    return str(
        payload.get("prompt")
        or payload.get("question")
        or payload.get("task")
        or payload.get("message")
        or ""
    )


def build_audit_record(
    payload: Dict[str, Any],
    answer: str = "",
    verification: Optional[Dict[str, Any]] = None,
    status: str = "ok",
    transport: str = "reason",
    error: Optional[str] = None,
) -> Dict[str, Any]:
    prompt = extract_prompt(payload)
    reasoning_mode = extract_reasoning_mode(payload)

    return {
        "audit_id": str(uuid.uuid4()),
        "timestamp_utc": utc_now_iso(),
        "project": PROJECT_NAME,
        "status": status,
        "transport": transport,
        "reasoning_mode": reasoning_mode,
        "layer": payload.get("layer", "vicdan"),
        "architecture": payload.get("architecture", "HOPEtensor"),
        "prompt_preview": prompt[:500],
        "prompt_length": safe_len(prompt),
        "answer_preview": str(answer or "")[:700],
        "answer_length": safe_len(answer),
        "verification": verification or {},
        "error": error,
        "pipeline": [
            "input",
            "reasoning_node",
            "vicdan_verification_node",
            "observer_audit_node",
            "delivery",
        ],
        "doctrine": [
            "Peace at home.",
            "Peace in the world.",
            "Peace in the universe and HOPEverse.",
        ],
    }


def write_audit_record(record: Dict[str, Any]) -> Dict[str, Any]:
    ensure_audit_dir()

    with AUDIT_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    return record


def audit_cognition(
    payload: Dict[str, Any],
    answer: str = "",
    verification: Optional[Dict[str, Any]] = None,
    status: str = "ok",
    transport: str = "reason",
    error: Optional[str] = None,
) -> Dict[str, Any]:
    record = build_audit_record(
        payload=payload,
        answer=answer,
        verification=verification,
        status=status,
        transport=transport,
        error=error,
    )

    return write_audit_record(record)


def read_recent_audits(limit: int = 20) -> Dict[str, Any]:
    ensure_audit_dir()

    if not AUDIT_FILE.exists():
        return {
            "status": "empty",
            "records": [],
            "count": 0,
            "audit_file": str(AUDIT_FILE),
        }

    lines = AUDIT_FILE.read_text(encoding="utf-8").splitlines()
    selected = lines[-limit:]

    records = []

    for line in selected:
        try:
            records.append(json.loads(line))
        except Exception:
            continue

    return {
        "status": "ok",
        "records": records,
        "count": len(records),
        "audit_file": str(AUDIT_FILE),
    }


def summarize_audits(limit: int = 50) -> Dict[str, Any]:
    recent = read_recent_audits(limit=limit)
    records = recent.get("records", [])

    by_mode: Dict[str, int] = {}
    by_status: Dict[str, int] = {}
    by_transport: Dict[str, int] = {}
    total_answer_length = 0

    for record in records:
        mode = record.get("reasoning_mode", "unknown")
        status = record.get("status", "unknown")
        transport = record.get("transport", "unknown")

        by_mode[mode] = by_mode.get(mode, 0) + 1
        by_status[status] = by_status.get(status, 0) + 1
        by_transport[transport] = by_transport.get(transport, 0) + 1
        total_answer_length += int(record.get("answer_length") or 0)

    avg_answer_length = (
        round(total_answer_length / len(records), 2)
        if records
        else 0
    )

    return {
        "status": "ok",
        "count": len(records),
        "by_mode": by_mode,
        "by_status": by_status,
        "by_transport": by_transport,
        "avg_answer_length": avg_answer_length,
        "audit_file": str(AUDIT_FILE),
    }