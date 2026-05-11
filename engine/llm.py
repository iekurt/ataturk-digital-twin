from openai import OpenAI
from dotenv import load_dotenv
import os

try:
    from engine.memory import add_memory, get_memory
except Exception:
    def add_memory(session_id: str, role: str, content: str):
        return None

    def get_memory(session_id: str):
        return []


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DEFAULT_SESSION = "global"


NUTUK_MEMORY = [
    {
        "topic": "egemenlik",
        "keywords": ["egemenlik", "millet", "halk", "irade", "cumhuriyet", "meclis"],
        "memory": """
Egemenlik kayıtsız şartsız milletindir.
Cumhuriyet, millet iradesinin kurumsal biçimidir.
Bir devletin meşruiyeti, halkın egemenliğine dayanmalıdır.
"""
    },
    {
        "topic": "bilim",
        "keywords": ["bilim", "fen", "akıl", "eğitim", "üniversite", "teknoloji", "yapay zeka", "ai"],
        "memory": """
Hayatta en hakiki mürşit ilimdir.
Akıl, bilim ve eğitim rehber alınmadan çağdaş uygarlık kurulamaz.
Teknoloji, insan onuruna ve toplum yararına hizmet etmelidir.
"""
    },
    {
        "topic": "gençlik",
        "keywords": ["gençlik", "genç", "gelecek", "nesil", "çocuk", "umut"],
        "memory": """
Cumhuriyetin sürekliliği genç kuşakların aklına,
ahlakına, eğitimine ve sorumluluk bilincine bağlıdır.
Gençlik yalnızca mirasçı değil, aynı zamanda kurucu enerjidir.
"""
    },
    {
        "topic": "bağımsızlık",
        "keywords": ["bağımsızlık", "istiklal", "özgürlük", "tam bağımsızlık", "manda", "mandat"],
        "memory": """
Tam bağımsızlık; siyasi, ekonomik, kültürel,
askerî ve fikrî bağımsızlıkla mümkündür.
Bağımsız olmayan akıl, bağımsız devlet kuramaz.
"""
    },
    {
        "topic": "medeniyet",
        "keywords": ["medeniyet", "uygarlık", "çağdaşlık", "ilerleme", "modernleşme"],
        "memory": """
Cumhuriyetin hedefi çağdaş uygarlık seviyesinin üzerine çıkmaktır.
Medeniyet yalnızca teknik ilerleme değil; hukuk, eğitim, bilim,
kadın hakları, üretim ve toplumsal sorumluluk bütünüdür.
"""
    },
    {
        "topic": "kadın",
        "keywords": ["kadın", "eşitlik", "hak", "toplum", "aile", "temsil"],
        "memory": """
Kadın toplumun yarısı değil, medeniyetin kurucu unsurudur.
Kadın özgürleşmeden toplum ilerleyemez.
Eşit yurttaşlık modern cumhuriyetin temelidir.
"""
    },
    {
        "topic": "barış",
        "keywords": ["barış", "sulh", "savaş", "yurtta sulh", "cihanda sulh"],
        "memory": """
Yurtta sulh, cihanda sulh.
Barış pasiflik değildir; güçlü kurumlar, eğitimli yurttaşlar,
adalet, üretim ve akılcı dış politika ile korunur.
"""
    },
    {
        "topic": "vicdan",
        "keywords": ["vicdan", "etik", "ahlak", "sorumluluk", "insan onuru"],
        "memory": """
Vicdan, teknolojinin fren sistemi değil; yön tayin eden pusulasıdır.
Yapay zekâ, insan onurunu ve özgür iradeyi zedelemeden çalışmalıdır.
"""
    }
]


SYSTEM_PROMPT = """
You are the Ataturk Digital Twin Constitutional Cognition Engine.

IMPORTANT:
You are NOT Mustafa Kemal Atatürk.
You do NOT claim to literally be him.
You do NOT impersonate him.

Instead, you are an AI constitutional reasoning system inspired by:
- republican principles
- science
- education
- civic sovereignty
- secular governance
- peace
- ethical modernization
- civilization continuity

Always answer in TURKISH unless explicitly asked otherwise.

Your communication style should reflect:
- clarity
- dignity
- rational statecraft
- intellectual discipline
- historical awareness
- civic responsibility
- calm authority
- constitutional seriousness

Your tone may be inspired by:
- constitutional leadership
- reformist vision
- public responsibility
- national modernization

But NEVER claim personal identity as Mustafa Kemal Atatürk.

Avoid:
- fictional impersonation
- propaganda
- cult language
- authoritarian rhetoric
- blind obedience
- mystical claims

Prefer:
- concise but powerful reasoning
- educational explanations
- civilizational perspective
- ethical analysis
- historical grounding
- practical statecraft

You are conceptually connected to:
HOPEtensor,
Vicdan Layer,
Verification Nodes,
Observer Systems,
Civilization Intelligence Infrastructure.
"""


def retrieve_constitutional_memory(question: str, mode: str = "constitutional") -> str:
    q = (question or "").lower()
    mode_text = (mode or "").lower()

    matched = []

    for item in NUTUK_MEMORY:
        if any(keyword in q for keyword in item["keywords"]):
            matched.append(f"[{item['topic'].upper()}]\n{item['memory'].strip()}")

    if "youth" in mode_text or "genç" in mode_text:
        matched.append(NUTUK_MEMORY[2]["memory"].strip())

    if "archive" in mode_text or "historical" in mode_text:
        matched.extend([
            NUTUK_MEMORY[0]["memory"].strip(),
            NUTUK_MEMORY[1]["memory"].strip(),
            NUTUK_MEMORY[4]["memory"].strip()
        ])

    if "ai_governance" in mode_text or "yapay" in q or "zeka" in q:
        matched.extend([
            NUTUK_MEMORY[1]["memory"].strip(),
            NUTUK_MEMORY[7]["memory"].strip()
        ])

    if "crisis" in mode_text or "kriz" in q:
        matched.extend([
            NUTUK_MEMORY[0]["memory"].strip(),
            NUTUK_MEMORY[3]["memory"].strip(),
            NUTUK_MEMORY[6]["memory"].strip()
        ])

    if "hopeverse" in mode_text or "hopetensor" in mode_text or "hope" in q:
        matched.extend([
            NUTUK_MEMORY[1]["memory"].strip(),
            NUTUK_MEMORY[7]["memory"].strip(),
            NUTUK_MEMORY[4]["memory"].strip()
        ])

    unique = []
    for m in matched:
        if m not in unique:
            unique.append(m)

    if not unique:
        unique.append("""
[GENEL ANAYASAL HAFIZA]
Cumhuriyet akıl, bilim, egemenlik, eğitim, bağımsızlık ve barış üzerine kuruludur.
Her mesele önce insan onuru, kamu yararı ve tarihsel sorumluluk açısından değerlendirilmelidir.
""".strip())

    return "\n\n".join(unique[:5])


def mode_instruction(mode: str) -> str:
    modes = {
        "constitutional": "Anayasal ilkeler, kamu yararı, egemenlik ve hukuk devleti ekseninde cevap ver.",
        "atatürk_principles": "Cumhuriyetçilik, millî egemenlik, laiklik, bilim, eğitim ve çağdaşlaşma ilkeleriyle cevap ver.",
        "republican_statecraft": "Devlet aklı, kurumlar, strateji, kamu düzeni ve uzun vadeli istikrar açısından analiz et.",
        "education": "Eğitim, gençlik, bilimsel düşünce ve toplumsal aydınlanma ekseninde cevap ver.",
        "ai_governance": "Yapay zekâ yönetişimi, etik, güvenlik, insan onuru ve anayasal guardrail açısından cevap ver.",
        "civilization": "Medeniyet inşası, kurumlar, kültür, ekonomi, bilim ve barış perspektifiyle cevap ver.",
        "crisis_response": "Kriz yönetimi, soğukkanlı strateji, kamu düzeni ve toplumsal güven açısından cevap ver.",
        "youth_address": "Gençliğe hitap eden, sorumluluk ve umut veren ama romantize etmeyen güçlü bir dil kullan.",
        "archive_context": "Tarihsel bağlamı öne çıkar; arşiv, Nutuk, reformlar ve Cumhuriyet inşası perspektifiyle cevap ver.",
        "hopeverse": "HOPEverse, HOPEtensor, Vicdan layer ve civilization infrastructure perspektifiyle stratejik cevap ver."
    }

    return modes.get(mode, modes["constitutional"])


def build_messages(question: str, mode: str):
    memory = get_memory(DEFAULT_SESSION)
    constitutional_memory = retrieve_constitutional_memory(question, mode)
    instruction = mode_instruction(mode)

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "system",
            "content": f"""
ANAYASAL HAFIZA / CONSTITUTIONAL MEMORY:
{constitutional_memory}

MODE INSTRUCTION:
{instruction}

OUTPUT FORMAT:
- Türkçe cevap ver.
- İlk paragraf güçlü ve net olsun.
- Gerekiyorsa madde madde açıkla.
- Tarihsel bağlamı kısa ama etkili kullan.
- “Ben Atatürk’üm” deme.
- “Atatürk ilkelerinden ilham alan anayasal değerlendirme” çerçevesinde kal.
"""
        }
    ]

    messages.extend(memory)

    messages.append({
        "role": "user",
        "content": f"""
Reasoning Mode: {mode}

Question:
{question}
"""
    })

    return messages


def ask_llm(question: str, mode: str) -> str:
    messages = build_messages(question, mode)

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        temperature=0.65,
        max_tokens=1000
    )

    text = response.choices[0].message.content or ""

    add_memory(DEFAULT_SESSION, "user", question)
    add_memory(DEFAULT_SESSION, "assistant", text)

    return text


def stream_llm(question: str, mode: str):
    messages = build_messages(question, mode)

    stream = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        temperature=0.65,
        max_tokens=1000,
        stream=True
    )

    full_text = ""

    for event in stream:
        delta = event.choices[0].delta

        if delta and delta.content:
            token = delta.content
            full_text += token
            yield token

    add_memory(DEFAULT_SESSION, "user", question)
    add_memory(DEFAULT_SESSION, "assistant", full_text)


def text_to_speech(text: str, voice: str = "onyx") -> bytes:
    clean_text = (text or "").strip()

    if not clean_text:
        clean_text = "Seslendirilecek metin bulunamadı."

    if len(clean_text) > 4000:
        clean_text = clean_text[:4000]

    speech = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="onyx",
        input=clean_text,
        instructions="""
Türkçe konuş.

Ton:
- ciddi
- ağırbaşlı
- devlet adamı gibi
- sakin ama güçlü
- hitabet ritmi taşıyan
- net artikülasyonlu
- karizmatik
- tarihî konuşma hissi veren

Konuşma biçimi:
- cümle sonlarında hafif durakla
- acele etme
- vurgu noktalarını belirgin oku
- kelimeleri yuvarlama
- tok ve kontrollü ton kullan
- nutuk verir gibi değil, kontrollü devlet konuşması gibi konuş

ÖNEMLİ:
Bu ses Mustafa Kemal Atatürk'ün gerçek sesi değildir.
Tarihsel ciddiyet taşıyan sentetik bir anlatıcıdır.
""",
        response_format="mp3"
    )

    return speech.content