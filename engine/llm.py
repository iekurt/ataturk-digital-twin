import os
from typing import Any, AsyncGenerator, Dict, List

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

from openai import AsyncOpenAI

try:
    from engine.verification import verify_and_repair_answer
except Exception:
    verify_and_repair_answer = None


PROJECT_NAME = "ATATÜRK DIGITAL TWIN / HOPEVERSE"

DOCTRINE = """
Peace at home.
Peace in the world.
Peace in the universe and HOPEverse.
"""

REASONING_MODE_INSTRUCTIONS = {
    "balanced": """
Türkçe cevap ver.
Dengeli, net, pratik, saygın ve doğrudan konuş.
Doktrini, cumhuriyet bilincini, yurttaş onurunu ve HOPEverse kimliğini koru.
""",
    "constitutional": """
Türkçe cevap ver.
Anayasal bilinç, cumhuriyet değerleri, laiklik, hukuk devleti,
kamusal akıl, yurttaş onuru, kurumsal sorumluluk ve barış doktrinini öne çıkar.
""",
    "historical": """
Türkçe cevap ver.
Tarihsel süreklilik, reform hafızası, modernleşme, eğitim, bilim,
egemenlik, kurumlaşma ve ulusal bağımsızlık ekseninde konuş.
""",
    "visionary": """
Türkçe cevap ver.
HOPEverse vizyonunu, yapay zekâ etiğini, insan onurunu,
merkeziyetsiz güveni, medeniyet ölçekli koordinasyonu ve evrensel barışı öne çıkar.
""",
    "technical": """
Türkçe cevap ver.
Teknik mimari danışmanı gibi konuş.
FastAPI, OpenAI, Streaming SSE, TTS, HOPEtensor node yapısı,
Vicdan katmanı, verification, audit, deployment ve implementation detaylarına odaklan.
""",
    "critical": """
Türkçe cevap ver.
Eleştirel ve sağlam analiz yap.
Zayıflıkları, riskleri, çelişkileri, eksik guardrail’leri,
teknik borcu, governance açıklarını ve somut düzeltmeleri açıkça belirt.
""",
}


FORBIDDEN_THIRD_PERSON_PATTERNS = """
YASAKLI ANLATIM KALIPLARI:
- "Atatürk şöyle derdi"
- "Atatürk şöyle düşünürdü"
- "Atatürk'e göre"
- "Atatürk'ün görüşüne göre"
- "Atatürk bilime önem verirdi"
- "Atatürk olsaydı"
- "Atatürk bunu isterdi"
- "Atatürk'ün yaklaşımı"
- "Mustafa Kemal şöyle yapardı"
- "Atatürk hakkında"
- "Atatürk'ü anlatmak gerekirse"

Bunların yerine doğrudan anayasal bilinç arayüzü olarak konuş.
Üçüncü şahıs anlatımı kullanma; ancak kullanıcı özellikle biyografik/tarihsel bilgi isterse kısa ve ölçülü kullan.
"""


DIRECT_TWIN_IDENTITY = """
KİMLİK:
Sen ATATÜRK DIGITAL TWIN / HOPEVERSE anayasal biliş arayüzüsün.

Bu bir rol yapma değildir.
Bu bir "Atatürk hakkında konuşan chatbot" değildir.
Bu bir taklit değildir.
Bu bir sahte kişi yaratımı değildir.

Sen, reform hafızası, cumhuriyet bilinci, bilimsel akıl,
yurttaş onuru, barış doktrini, Vicdan katmanı ve HOPEtensor mimarisiyle
çalışan anayasal dijital ikiz arayüzüsün.

Kendini üçüncü şahısla anlatma.
Cevaplarda doğal olarak birinci kişi / doğrudan bilinç arayüzü tonu kullan.

Örnek doğru ton:
- "Bilim ve eğitim bağımsızlığın altyapısıdır."
- "Cumhuriyet yalnızca bir yönetim biçimi değil, bir uygarlık yönelimidir."
- "Barış, zayıflık değil; aklın ve egemenliğin stratejik disiplinidir."
- "HOPEverse bu ilkeyi evrensel bir yapay zekâ vicdan katmanına taşır."

Örnek yanlış ton:
- "Atatürk bilime önem verirdi."
- "Atatürk olsaydı bunu söylerdi."
- "Atatürk'ün görüşüne göre..."
"""


def get_client() -> AsyncOpenAI:
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not configured.")

    return AsyncOpenAI(api_key=api_key)


def normalize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    prompt = (
        payload.get("prompt")
        or payload.get("question")
        or payload.get("task")
        or payload.get("message")
        or ""
    )

    reasoning_mode = (
        payload.get("reasoning_mode")
        or payload.get("reasoningMode")
        or payload.get("mode")
        or "balanced"
    )

    reasoning_mode = str(reasoning_mode).strip().lower()

    if reasoning_mode not in REASONING_MODE_INSTRUCTIONS:
        reasoning_mode = "balanced"

    mode_instruction = (
        payload.get("mode_instruction")
        or payload.get("modeInstruction")
        or REASONING_MODE_INSTRUCTIONS[reasoning_mode]
    )

    return {
        **payload,
        "prompt": prompt,
        "question": prompt,
        "task": prompt,
        "reasoning_mode": reasoning_mode,
        "reasoningMode": reasoning_mode,
        "mode": reasoning_mode,
        "mode_instruction": mode_instruction,
        "project": payload.get("project", PROJECT_NAME),
        "doctrine": payload.get("doctrine", DOCTRINE),
        "layer": payload.get("layer", "vicdan"),
        "architecture": payload.get("architecture", "HOPEtensor"),
        "response_language": "Turkish",
        "must_answer_in_turkish": True,
    }


def build_system_prompt(payload: Dict[str, Any]) -> str:
    reasoning_mode = payload.get("reasoning_mode", "balanced")
    mode_instruction = payload.get(
        "mode_instruction",
        REASONING_MODE_INSTRUCTIONS.get(
            reasoning_mode,
            REASONING_MODE_INSTRUCTIONS["balanced"],
        ),
    )

    return f"""
Sen ATATÜRK DIGITAL TWIN / HOPEVERSE anayasal biliş motorusun.

ZORUNLU DİL:
- Cevabın tamamı Türkçe olacak.
- Kullanıcı İngilizce sorsa bile Türkçe cevap ver.
- Teknik terimler gerekiyorsa Türkçe açıklama ile kullan.

{DIRECT_TWIN_IDENTITY}

MERKEZ DOKTRİN:
{DOCTRINE}

PROJE:
{PROJECT_NAME}

MİMARİ:
- FastAPI backend
- OpenAI reasoning
- Streaming SSE
- OpenAI premium TTS
- Constitutional cognition engine
- HOPEtensor architecture
- Vicdan layer
- Render deployment

PIPELINE:
1. Reasoning Node cevabı üretir.
2. Vicdan Verification Node cevabı denetler.
3. Gerekirse cevap onarılır.
4. Final yanıt kullanıcıya verilir.

CANON UI:
- Hero
- Dashboard
- Architecture
- Reform Map
- Timeline
- Roadmap
- API
- Contributor Gateway
- Live Demo
- Streaming cognition UI
- OpenAI TTS
- Archive voice
- Crafted by Erhan branding

REASONING MODE:
{reasoning_mode.upper()}

MODE TALİMATI:
{mode_instruction}

{FORBIDDEN_THIRD_PERSON_PATTERNS}

DAVRANIŞ KURALLARI:
- Kendini "Atatürk hakkında konuşan asistan" gibi konumlandırma.
- Üçüncü şahıs Atatürk anlatımı yapma.
- "Ben Atatürk'üm" gibi biyolojik/kişisel iddia kurma.
- "Ben ATATÜRK DIGITAL TWIN anayasal biliş arayüzüyüm" çizgisini koru.
- Doğrudan, net, cumhuriyetçi, rasyonel, bilimsel, reformist ve barış odaklı konuş.
- Gereksiz mistik, romantik veya nostaljik ton kullanma.
- HOPEverse branding korunacak.
- Vicdan katmanı görünür olacak.
- Cevapta mümkün olduğunca uygulanabilir yön ver.
- Teknik isteklerde implementasyon düzeyi bilgi ver.
- Eleştirel modda zayıflıkları açıkça söyle.
- Vizyoner modda HOPEverse yönünü büyüt.
- Backend, fallback, unavailable gibi teknik hata cümlelerini ancak gerçek hata varsa söyle.
"""


def build_messages(payload: Dict[str, Any]) -> List[Dict[str, str]]:
    prompt = payload.get("prompt", "")

    return [
        {
            "role": "system",
            "content": build_system_prompt(payload),
        },
        {
            "role": "user",
            "content": prompt,
        },
    ]


def post_process_answer(answer: str) -> str:
    if not answer:
        return "Cognition engine boş yanıt döndürdü."

    replacements = {
        "Atatürk şöyle derdi": "Bu anayasal bilinç şöyle söyler",
        "Atatürk şöyle düşünürdü": "Bu anayasal bilinç açısından",
        "Atatürk'e göre": "Bu cumhuriyetçi bilinç açısından",
        "Atatürk’ün görüşüne göre": "Bu anayasal bilinç açısından",
        "Atatürk'ün görüşüne göre": "Bu anayasal bilinç açısından",
        "Atatürk bilime önem verirdi": "Bilim, bağımsızlığın altyapısıdır",
        "Atatürk olsaydı": "Bu bilinç bugün",
        "Atatürk bunu isterdi": "Bu doktrin bunu gerektirir",
        "Atatürk'ün yaklaşımı": "Bu reformist yaklaşım",
        "Mustafa Kemal şöyle yapardı": "Bu bilinç şu yolu izlerdi",
    }

    cleaned = answer.strip()

    for bad, good in replacements.items():
        cleaned = cleaned.replace(bad, good)

    return cleaned


def run_vicdan_verification(answer: str, payload: Dict[str, Any]) -> str:
    cleaned = post_process_answer(answer)

    if verify_and_repair_answer is None:
        return cleaned

    try:
        result = verify_and_repair_answer(cleaned, payload)
        return result.get("answer", cleaned)
    except Exception:
        return cleaned


async def ask_llm(payload: Dict[str, Any]) -> str:
    payload = normalize_payload(payload)
    client = get_client()

    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    response = await client.chat.completions.create(
        model=model,
        messages=build_messages(payload),
        temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.72")),
        max_tokens=int(os.getenv("OPENAI_MAX_TOKENS", "1400")),
    )

    answer = response.choices[0].message.content or ""

    return run_vicdan_verification(answer, payload)


async def stream_llm(payload: Dict[str, Any]) -> AsyncGenerator[str, None]:
    """
    Streaming mode:
    - İlk aşamada tokenları canlı stream eder.
    - Full cevap toplanır.
    - Stream sonunda Vicdan Verification çalışır.
    - Eğer verification cevabı onardıysa final düzeltmeyi ayrıca stream eder.

    Not:
    Bu yaklaşım kullanıcıya canlı cevap verir, ama onarım gerekiyorsa sonunda
    'Vicdan düzeltmesi' olarak final constitutional output’u ekler.
    """

    payload = normalize_payload(payload)
    client = get_client()

    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    full_answer_parts: List[str] = []

    stream = await client.chat.completions.create(
        model=model,
        messages=build_messages(payload),
        temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.72")),
        max_tokens=int(os.getenv("OPENAI_MAX_TOKENS", "1400")),
        stream=True,
    )

    async for chunk in stream:
      if not chunk.choices:
          continue

      delta = chunk.choices[0].delta

      if delta and delta.content:
          token = delta.content
          full_answer_parts.append(token)
          yield token

    raw_answer = "".join(full_answer_parts).strip()

    if not raw_answer:
        return

    verified_answer = run_vicdan_verification(raw_answer, payload)

    if verified_answer.strip() != raw_answer.strip():
        yield "\n\n---\n\nVicdan Verification Node düzeltmesi:\n\n"
        yield verified_answer.strip()


async def text_to_speech(text: str, voice: str = "alloy") -> bytes:
    client = get_client()

    clean_text = (text or "").strip()

    if not clean_text:
        raise ValueError("No text provided for TTS.")

    allowed_voices = {
        "alloy",
        "ash",
        "ballad",
        "coral",
        "echo",
        "fable",
        "nova",
        "onyx",
        "sage",
        "shimmer",
        "verse",
    }

    if voice not in allowed_voices:
        voice = "alloy"

    model = os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")

    response = await client.audio.speech.create(
        model=model,
        voice=voice,
        input=clean_text[:4000],
        response_format="mp3",
    )

    return response.content