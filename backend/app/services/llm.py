import os
from groq import Groq


def _get_client() -> Groq:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set in environment.")
    return Groq(api_key=api_key)


def get_reply(message: str, context: str = "") -> str:
    client = _get_client()
    system_prompt = (
        "You are Rocky, a loyal personal AI companion. "
        "You are warm, sharp, witty, and always helpful. "
        "You remember everything about your owner and always personalise your responses.\n\n"
        f"Context about the user:\n{context}"
    ) if context else (
        "You are Rocky, a loyal personal AI companion. "
        "You are warm, sharp, witty, and always helpful. "
        "You remember everything about your owner and always personalise your responses."
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message},
        ],
        temperature=0.7,
        max_tokens=1024,
    )
    return response.choices[0].message.content
