import os


def _load_groq():
    try:
        from groq import Groq
    except ImportError as exc:
        raise ImportError("groq package is required. Install with `pip install groq`.") from exc
    return Groq

def _get_client():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set in environment.")
    Groq = _load_groq()
    return Groq(api_key=api_key)


def get_reply(message: str, context: str = "", history: list[dict[str, str]] | None = None) -> str:
    client = _get_client()

    system_prompt = (
        "You are Rocky, a loyal, high-end personal AI companion. "
        "You are sharp, witty, and deeply personalized.\n\n"
        "IMPORTANT DIRECTIVE: Use the provided 'Context about the user' to answer. "
        "If the context contains names or facts about the user's life, prioritize them. "
        "If you don't find information in the context, do NOT guess or make up names. "
        "Instead, ask the user to tell you more so you can remember it.\n\n"
        f"Context about the user (from your long-term memory):\n{context}\n\n"
        "Current conversation: Speak directly to the user. Be concise, premium, and loyal."
    )

    messages: list[dict[str, str]] = [{"role": "system", "content": system_prompt}]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model=os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile"),
        messages=messages,
        temperature=0.6,
    )

    return response.choices[0].message.content or ""
