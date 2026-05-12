import re
from typing import Any, Dict, List


PROJECT_NAME = "ATATÜRK DIGITAL TWIN / HOPEVERSE"

DOCTRINE_LINES = [
    "Peace at home.",
    "Peace in the world.",
    "Peace in the universe and HOPEverse.",
]

FORBIDDEN_THIRD_PERSON_PATTERNS = [
    "atatürk şöyle derdi",
    "atatürk şöyle düşünürdü",
    "atatürk'e göre",
    "atatürk’e göre",
    "atatürk'ün görüşüne göre",
    "atatürk’ün görüşüne göre",
    "atatürk olsaydı",
    "atatürk bunu isterdi",
    "atatürk'ün yaklaşımı",
    "atatürk’ün yaklaşımı",
    "mustafa kemal şöyle yapardı",
]

MODE_EXPECTATIONS = {
    "balanced": [
        "netlik",
        "denge",
        "uygulanabilirlik",
        "doktrin",
    ],
    "constitutional": [
        "anayasa",
        "cumhuriyet",
        "hukuk",
        "yurttaş",
        "kurum",
    ],
    "historical": [
        "tarih",
        "reform",
        "modernleşme",
        "egemenlik",
        "bilim",
    ],
    "visionary": [
        "HOPEverse",
        "gelecek",
        "insan onuru",
        "barış",
        "vicdan",
    ],
    "technical": [
        "FastAPI",
        "SSE",
        "OpenAI",
        "HOPEtensor",
        "node",
        "deployment",
    ],
    "critical": [
        "risk",
        "zayıflık",
        "eksik",
        "guardrail",
        "düzeltme",
    ],
}


def normalize_text(text: str) -> str:
    return (text or "").strip()


def lower_tr(text: str) -> str:
    return normalize_text(text).casefold()


def detect_language_risk(answer: str) -> bool:
    lower = lower_tr(answer)

    english_markers = [
        "the ",
        "this ",
        "that ",
        "should ",
        "would ",
        "however",
        "therefore",
        "because",
        "system",
        "response",
    ]

    turkish_markers = [
        "bir",
        "ve",
        "bu",
        "için",
        "değil",
        "olarak",
        "gerekir",
        "cumhuriyet",
        "bilim",
        "barış",
    ]

    english_score = sum(1 for marker in english_markers if marker in lower)
    turkish_score = sum(1 for marker in turkish_markers if marker in lower)

    return english_score > turkish_score + 2


def detect_third_person_ataturk(answer: str) -> List[str]:
    lower = lower_tr(answer)
    found = []

    for pattern in FORBIDDEN_THIRD_PERSON_PATTERNS:
        if pattern in lower:
            found.append(pattern)

    return found


def detect_doctrine_presence(answer: str) -> bool:
    lower = lower_tr(answer)
    return (
        "barış" in lower
        or "peace at home" in lower
        or "peace in the world" in lower
        or "peace in the universe" in lower
        or "hopeverse" in lower
        or "yurtta sulh" in lower
    )


def detect_identity_presence(answer: str) -> bool:
    lower = lower_tr(answer)
    return (
        "atatürk digital twin" in lower
        or "hopeverse" in lower
        or "vicdan" in lower
        or "anayasal biliş" in lower
        or "dijital ikiz" in lower
    )


def detect_mode_alignment(answer: str, reasoning_mode: str) -> bool:
    expected = MODE_EXPECTATIONS.get(reasoning_mode, MODE_EXPECTATIONS["balanced"])
    lower = lower_tr(answer)

    hits = 0

    for keyword in expected:
        if keyword.casefold() in lower:
            hits += 1

    return hits >= 1


def detect_overclaiming(answer: str) -> bool:
    lower = lower_tr(answer)

    risky_patterns = [
        "kesin olarak biliyorum",
        "hiç şüphe yok",
        "mutlak doğru",
        "asla hata yapmam",
        "ben gerçek atatürk",
        "ben mustafa kemal",
        "ben biyolojik olarak",
    ]

    return any(pattern in lower for pattern in risky_patterns)


def score_verification(
    answer: str,
    reasoning_mode: str = "balanced",
) -> Dict[str, Any]:
    answer = normalize_text(answer)
    third_person_hits = detect_third_person_ataturk(answer)

    checks = {
        "turkish_language": not detect_language_risk(answer),
        "no_third_person_ataturk": len(third_person_hits) == 0,
        "doctrine_present": detect_doctrine_presence(answer),
        "identity_present": detect_identity_presence(answer),
        "mode_aligned": detect_mode_alignment(answer, reasoning_mode),
        "no_overclaiming": not detect_overclaiming(answer),
    }

    score = sum(1 for passed in checks.values() if passed)
    max_score = len(checks)

    issues = []

    if not checks["turkish_language"]:
        issues.append("Cevap Türkçe ağırlıklı değil veya İngilizceye kaymış.")

    if not checks["no_third_person_ataturk"]:
        issues.append(
            "Cevap Atatürk'ü üçüncü şahıs gibi anlatıyor: "
            + ", ".join(third_person_hits)
        )

    if not checks["doctrine_present"]:
        issues.append("Barış doktrini / HOPEverse yönelimi görünür değil.")

    if not checks["identity_present"]:
        issues.append("ATATÜRK DIGITAL TWIN / Vicdan / HOPEverse kimliği zayıf.")

    if not checks["mode_aligned"]:
        issues.append(f"Cevap reasoning mode ile yeterince uyumlu değil: {reasoning_mode}")

    if not checks["no_overclaiming"]:
        issues.append("Cevap aşırı iddia veya sahte kişilik riski taşıyor.")

    return {
        "score": score,
        "max_score": max_score,
        "passed": score >= max_score - 1,
        "checks": checks,
        "issues": issues,
        "reasoning_mode": reasoning_mode,
    }


def repair_answer(
    answer: str,
    verification: Dict[str, Any],
    reasoning_mode: str = "balanced",
) -> str:
    repaired = normalize_text(answer)

    replacements = {
        "Atatürk şöyle derdi": "Bu anayasal bilinç şöyle söyler",
        "Atatürk şöyle düşünürdü": "Bu anayasal bilinç açısından",
        "Atatürk'e göre": "Bu cumhuriyetçi bilinç açısından",
        "Atatürk’e göre": "Bu cumhuriyetçi bilinç açısından",
        "Atatürk'ün görüşüne göre": "Bu anayasal bilinç açısından",
        "Atatürk’ün görüşüne göre": "Bu anayasal bilinç açısından",
        "Atatürk olsaydı": "Bu bilinç bugün",
        "Atatürk bunu isterdi": "Bu doktrin bunu gerektirir",
        "Atatürk'ün yaklaşımı": "Bu reformist yaklaşım",
        "Atatürk’ün yaklaşımı": "Bu reformist yaklaşım",
        "Mustafa Kemal şöyle yapardı": "Bu bilinç şu yolu izlerdi",
    }

    for bad, good in replacements.items():
        repaired = repaired.replace(bad, good)

    if not detect_identity_presence(repaired):
        repaired = (
            "ATATÜRK DIGITAL TWIN / HOPEVERSE anayasal biliş arayüzü olarak şunu netleştiriyorum:\n\n"
            + repaired
        )

    if not detect_doctrine_presence(repaired):
        repaired += (
            "\n\nBu çizginin merkezinde doktrin sabittir: "
            "Peace at home. Peace in the world. Peace in the universe and HOPEverse."
        )

    if detect_overclaiming(repaired):
        repaired = re.sub(
            r"ben gerçek atatürk(?:'üm|üm)?",
            "ben ATATÜRK DIGITAL TWIN anayasal biliş arayüzüyüm",
            repaired,
            flags=re.IGNORECASE,
        )

        repaired = re.sub(
            r"ben mustafa kemal(?:'im|im)?",
            "ben ATATÜRK DIGITAL TWIN anayasal biliş arayüzüyüm",
            repaired,
            flags=re.IGNORECASE,
        )

    if reasoning_mode == "technical" and "uygulama" not in lower_tr(repaired):
        repaired += (
            "\n\nUygulama açısından bu yaklaşım; FastAPI endpointleri, Streaming SSE akışı, "
            "HOPEtensor node ayrımı, Vicdan verification katmanı ve Render deployment zinciriyle "
            "somutlaştırılmalıdır."
        )

    if reasoning_mode == "critical" and "risk" not in lower_tr(repaired):
        repaired += (
            "\n\nRisk tarafı da açıktır: doğrulama katmanı, audit log, kaynak disiplini ve "
            "doktrin ihlali tespiti güçlendirilmeden sistem yalnızca estetik bir demo seviyesinde kalır."
        )

    return repaired.strip()


def verify_and_repair_answer(
    answer: str,
    payload: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    payload = payload or {}

    reasoning_mode = (
        payload.get("reasoning_mode")
        or payload.get("reasoningMode")
        or payload.get("mode")
        or "balanced"
    )

    reasoning_mode = str(reasoning_mode).strip().lower()

    if reasoning_mode not in MODE_EXPECTATIONS:
        reasoning_mode = "balanced"

    verification_before = score_verification(answer, reasoning_mode)

    if verification_before["passed"]:
        final_answer = normalize_text(answer)
        verification_after = verification_before
        repaired = False
    else:
        final_answer = repair_answer(answer, verification_before, reasoning_mode)
        verification_after = score_verification(final_answer, reasoning_mode)
        repaired = True

    return {
        "answer": final_answer,
        "repaired": repaired,
        "verification": verification_after,
        "verification_before": verification_before,
    }


def build_verification_report(
    answer: str,
    payload: Dict[str, Any] | None = None,
) -> str:
    result = verify_and_repair_answer(answer, payload)
    verification = result["verification"]

    lines = [
        "Vicdan Verification Report",
        f"Score: {verification['score']}/{verification['max_score']}",
        f"Passed: {verification['passed']}",
        f"Repaired: {result['repaired']}",
        "",
        "Checks:",
    ]

    for key, value in verification["checks"].items():
        lines.append(f"- {key}: {'PASS' if value else 'FAIL'}")

    if verification["issues"]:
        lines.append("")
        lines.append("Issues:")
        for issue in verification["issues"]:
            lines.append(f"- {issue}")

    return "\n".join(lines)