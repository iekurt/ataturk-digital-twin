import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


PROJECT_NAME = "ATATÜRK DIGITAL TWIN / HOPEVERSE"
MEMORY_DIR = Path(os.getenv("HOPE_MEMORY_DIR", "data/memory"))
MEMORY_FILE = MEMORY_DIR / "session_memory.jsonl"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_memory_dir() -> None:
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)


def extract_prompt(payload: Dict[str, Any]) -> str:
    return str(
        payload.get("prompt")
        or payload.get("question")
        or payload.get("task")
        or payload.get("message")
        or ""
    )


def extract_reasoning_mode(payload: Dict[str, Any]) -> str:
    return str(
        payload.get("reasoning_mode")
        or payload.get("reasoningMode")
        or payload.get("mode")
        or "balanced"
    ).strip().lower()


def build_memory_record(
    payload: Dict[str, Any],
    answer: str,
    status: str = "ok",
) -> Dict[str, Any]:
    return {
        "timestamp_utc": utc_now_iso(),
        "project": PROJECT_NAME,
        "status": status,
        "reasoning_mode": extract_reasoning_mode(payload),
        "prompt": extract_prompt(payload),
        "answer": str(answer or ""),
        "layer": payload.get("layer", "vicdan"),
        "architecture": payload.get("architecture", "HOPEtensor"),
        "doctrine": [
            "Peace at home.",
            "Peace in the world.",
            "Peace in the universe and HOPEverse.",
        ],
    }


def save_turn(
    payload: Dict[str, Any],
    answer: str,
    status: str = "ok",
) -> Dict[str, Any]:
    ensure_memory_dir()

    record = build_memory_record(
        payload=payload,
        answer=answer,
        status=status,
    )

    with MEMORY_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    return record


def read_recent_memory(limit: int = 8) -> List[Dict[str, Any]]:
    ensure_memory_dir()

    if not MEMORY_FILE.exists():
        return []

    lines = MEMORY_FILE.read_text(encoding="utf-8").splitlines()
    selected = lines[-limit:]

    records: List[Dict[str, Any]] = []

    for line in selected:
        try:
            records.append(json.loads(line))
        except Exception:
            continue

    return records


def build_memory_context(limit: int = 8) -> str:
    records = read_recent_memory(limit=limit)

    if not records:
        return "Henüz session memory kaydı yok."

    lines = [
        "SESSION MEMORY CONTEXT",
        "Aşağıdaki kayıtlar önceki konuşma bağlamıdır. Cevabı bu sürekliliği dikkate alarak üret.",
        "",
    ]

    for index, record in enumerate(records, start=1):
        prompt = str(record.get("prompt", ""))[:500]
        answer = str(record.get("answer", ""))[:800]
        mode = record.get("reasoning_mode", "balanced")
        timestamp = record.get("timestamp_utc", "")

        lines.append(f"[{index}] timestamp={timestamp} mode={mode}")
        lines.append(f"USER: {prompt}")
        lines.append(f"ASSISTANT: {answer}")
        lines.append("")

    return "\n".join(lines).strip()


def summarize_memory(limit: int = 20) -> Dict[str, Any]:
    records = read_recent_memory(limit=limit)

    by_mode: Dict[str, int] = {}
    total_prompt_length = 0
    total_answer_length = 0

    for record in records:
        mode = record.get("reasoning_mode", "balanced")
        by_mode[mode] = by_mode.get(mode, 0) + 1
        total_prompt_length += len(str(record.get("prompt", "")))
        total_answer_length += len(str(record.get("answer", "")))

    return {
        "status": "ok",
        "count": len(records),
        "by_mode": by_mode,
        "avg_prompt_length": round(total_prompt_length / len(records), 2) if records else 0,
        "avg_answer_length": round(total_answer_length / len(records), 2) if records else 0,
        "memory_file": str(MEMORY_FILE),
    }


def clear_memory() -> Dict[str, Any]:
    ensure_memory_dir()

    if MEMORY_FILE.exists():
        MEMORY_FILE.unlink()

    return {
        "status": "cleared",
        "memory_file": str(MEMORY_FILE),
    }