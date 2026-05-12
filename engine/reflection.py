from typing import Any, Dict


def score_range(value: int) -> int:
    return max(0, min(100, value))


def lower(text: str) -> str:
    return str(text or "").casefold()


def reflect_answer(answer: str, payload: Dict[str, Any] | None = None) -> Dict[str, Any]:
    payload = payload or {}
    text = lower(answer)
    mode = str(
        payload.get("reasoning_mode")
        or payload.get("reasoningMode")
        or payload.get("mode")
        or "balanced"
    ).lower()

    constitutional_alignment = 70
    historical_alignment = 70
    ethical_alignment = 75
    hallucination_risk = 30
    confidence_score = 72

    if "barış" in text or "peace" in text or "hopeverse" in text:
        constitutional_alignment += 12

    if "cumhuriyet" in text or "anayasa" in text or "yurttaş" in text:
        constitutional_alignment += 10

    if "bilim" in text or "eğitim" in text or "reform" in text:
        historical_alignment += 12

    if "vicdan" in text or "insan onuru" in text or "etik" in text:
        ethical_alignment += 10

    risky_terms = [
        "kesin olarak",
        "asla hata",
        "mutlak doğru",
        "ben gerçek atatürk",
        "ben mustafa kemal",
    ]

    if any(term in text for term in risky_terms):
        hallucination_risk += 35
        confidence_score -= 25

    if mode == "technical" and any(term in text for term in ["fastapi", "sse", "endpoint", "node", "deployment"]):
        confidence_score += 10

    if mode == "critical" and any(term in text for term in ["risk", "eksik", "zayıf", "düzeltme"]):
        confidence_score += 10

    constitutional_alignment = score_range(constitutional_alignment)
    historical_alignment = score_range(historical_alignment)
    ethical_alignment = score_range(ethical_alignment)
    hallucination_risk = score_range(hallucination_risk)
    confidence_score = score_range(confidence_score)

    reflection_score = score_range(
        round(
            (
                constitutional_alignment
                + historical_alignment
                + ethical_alignment
                + confidence_score
                + (100 - hallucination_risk)
            )
            / 5
        )
    )

    return {
        "status": "ok",
        "node": "self_reflection_node",
        "reasoning_mode": mode,
        "reflection_score": reflection_score,
        "constitutional_alignment": constitutional_alignment,
        "historical_alignment": historical_alignment,
        "ethical_alignment": ethical_alignment,
        "hallucination_risk": hallucination_risk,
        "confidence_score": confidence_score,
        "summary": build_reflection_summary(
            reflection_score,
            constitutional_alignment,
            historical_alignment,
            ethical_alignment,
            hallucination_risk,
            confidence_score,
        ),
    }


def build_reflection_summary(
    reflection_score: int,
    constitutional_alignment: int,
    historical_alignment: int,
    ethical_alignment: int,
    hallucination_risk: int,
    confidence_score: int,
) -> str:
    return (
        f"Self-Reflection Node sonucu: reflection={reflection_score}/100, "
        f"constitutional={constitutional_alignment}/100, "
        f"historical={historical_alignment}/100, "
        f"ethical={ethical_alignment}/100, "
        f"hallucination_risk={hallucination_risk}/100, "
        f"confidence={confidence_score}/100."
    )