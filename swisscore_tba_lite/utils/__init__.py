import os
import re
import json
import typing as t
import platform

T = t.TypeVar("T")

KiB = 1024
MiB = KiB * KiB
GiB = MiB * KiB

def readable_file_size(b: int) -> str:
    if b <= 0:
        return "Unknown"
    if b < KiB:
        return f"{b}Bytes"
    if b < MiB:
        return f"{b/KiB:.02f}KiB"
    if b < GiB:
        return f"{b/MiB:.02f}MiB"
    
    return f"{b/GiB:.02f}GiB"

def kb_interrupt() -> t.Literal["CTRL+C", "CMD+C"]:
    return "CMD+C" if platform.system() == "Darwin" else "CTRL+C"

def clamp(val: int, min_val: int, max_val: int) -> int:
    return min(max(val, min_val), max_val)

def camel_to_snake(name: str) -> str:
    return re.sub(r'(?<!^)(?=[A-Z])', "_", name).lower()

def snake_to_camel(name: str, capitalized=False) -> str:
    camel = "".join(word.capitalize() for word in name.split("_"))
    if capitalized:
        return camel
    return f"{camel[0].lower()}{camel[1:]}"

def sanitize_token(text: str) -> str:
    return re.sub(r"\d{6,}:[A-Za-z0-9_-]{28,}\b", "<token>", str(text))

def is_valid_bot_api_token(token: str) -> bool:
    pattern = r"^\d{6,}:[A-Za-z0-9_-]+$"
    return bool(re.match(pattern, token))

def get_update_type(update_obj: dict[str, t.Any]) -> str:
    return [k for k in update_obj.keys() if not k == "update_id"][0]

def dumps(obj) -> str:
    return json.dumps(obj, indent=None, separators=(",", ":"))

def replace_word(text: str, word: str, new_word: str, count: int = 0) -> str:
    return re.sub(rf"\b{re.escape(word)}\b", new_word, text, count=count)

def startswith_word(text: str, word: str) -> bool:
    """Check if a str starts with a specific word or substring (with boundary)"""
    return bool(re.match(rf"^{word}(?:\s|$)", text))
