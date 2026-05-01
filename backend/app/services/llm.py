import os
from groq import Groq


def _get_client() -> Groq:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set in environment.")
    return Groq(api_key=api_key)


def get_reply(message: str, context: str = "") -> str:
    client = _get_client()
    
    # Force Rocky to prioritize retrieved context
    system_prompt = (
        "You are Rocky, a loyal, high-end personal AI companion. "
        "You are sharp, witty, and deeply personalized.\n\n"
        "IMPORTANT DIRECTIVE: Use the provided 'Context about the user' to answer. "
        "If the context contains names or facts about the user's life, prioritize them. "
        "If you don't find information in the context, do NOT guess or make up names (like Emily). "
        "Instead, ask the user to tell you more so you can remember it.\n\n"
        f"Context about the user (from your long-term memory):\n{context}\n\n"
        "Current conversation: Speak directly to the user. Be concise, premium, and loyal."
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message},
        ],
        temperature=0.6, # Lowered slightly for more accuracy
        max_tokens=1024,
    )
    return response.choices[0].message.content
