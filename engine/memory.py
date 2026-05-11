from collections import defaultdict

conversation_memory = defaultdict(list)

MAX_MEMORY = 12


def add_memory(session_id: str, role: str, content: str):

    conversation_memory[session_id].append({
        "role": role,
        "content": content
    })

    if len(conversation_memory[session_id]) > MAX_MEMORY:
        conversation_memory[session_id] = conversation_memory[session_id][-MAX_MEMORY:]


def get_memory(session_id: str):
    return conversation_memory[session_id]


def clear_memory(session_id: str):
    conversation_memory[session_id] = []