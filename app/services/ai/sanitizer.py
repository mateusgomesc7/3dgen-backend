import re

def clean_ai_code(raw: str) -> str:
    raw = re.sub(r"```[a-zA-Z]*\n?", "", raw)
    raw = raw.replace("```", "")
    raw = re.sub(r"<think>.*?</think>", "", raw, flags=re.DOTALL)
    return raw.strip()