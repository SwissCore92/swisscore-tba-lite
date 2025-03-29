import os
import re
import json
import typing as t
import platform
from pathlib import Path
from secrets import token_urlsafe

import aiofiles
from aiohttp import FormData

T = t.TypeVar("T")

KiB = 1024
MiB = KiB * KiB
GiB = MiB * KiB

def is_mac_os():
    return platform.system() == "Darwin"

def kb_interrupt() -> t.Literal["CTRL+C", "CMD+C"]:
    return "CMD+C" if is_mac_os() else "CTRL+C"

def clamp(val: int, min_val: int, max_val: int) -> int:
    return min(max(val, min_val), max_val)

def camel_to_snake(name: str) -> str:
    return re.sub(r'(?<!^)(?=[A-Z])', "_", name).lower()

def snake_to_camel(name: str, capitalized=False) -> str:
    camel = "".join(word.capitalize() for word in name.split("_"))
    if capitalized:
        return camel
    return f"{camel[0].lower()}{camel[1:]}"

def get_update_type(update_obj: dict[str, t.Any]) -> str:
    return [k for k in update_obj.keys() if not k == "update_id"][0]

def to_list(l: T | list[T]) -> list[T]:
    return l if isinstance(l, list) else [l]

def dumps(obj) -> str:
    return json.dumps(obj, indent=None)

def replace_word(text: str, word: str, new_word: str, count: int = 0) -> str:
    return re.sub(rf"\b{re.escape(word)}\b", new_word, text, count=count)

def startswith_word(text: str, word: str) -> bool:
    return bool(re.match(rf"^{word}(?:\s|$)", text))

def is_local_file(path: str | Path) -> bool:
    """Check if a string represents a valid local file path."""
    path = path if isinstance(path, Path) else Path(path)
    return path.exists() and path.is_file()

def get_file_size(file: str | Path | bytes) -> int:
    if isinstance(file, bytes):
        return len(file)
    return os.stat(file).st_size

async def read_file(path: Path) -> bytes | t.AsyncGenerator[bytes, None]:
    """Read file as bytes asynchronously."""
    async with aiofiles.open(path, "rb") as f:
        return await f.read()

async def process_input_files(params: dict, check_input_files: list[str]) -> dict:
    """Extract and process input files from parameters."""
    input_files = {}
    
    for key in check_input_files:
        if key not in params:
            continue
        
        val = params[key]
        
        if isinstance(val, str) and is_local_file(val):
            input_files[key] = await read_file(Path(val))
            
        elif isinstance(val, Path):
            if val.exists():
                input_files[key] = await read_file(val)
            else:
                raise FileNotFoundError(f"'{val} not found!'")
        elif isinstance(val, bytes):
            
            input_files[key] = val
    
    return input_files

async def process_input_media(params: dict, check_input_media: list[str]) -> t.Tuple[dict, t.Optional[str]]:
    """Extract input media and attach necessary files."""
    input_files = {}
    input_media = None

    for key in check_input_media:
        if key not in params:
            continue
        
        media_items = params[key]
        if not isinstance(media_items, list):
            continue

        for media in media_items:
            if isinstance(media, dict) and "media" in media:
                file_ref = media["media"]
                if isinstance(file_ref, str) and is_local_file(file_ref):
                    file_ref = Path(file_ref)
                    
                id = token_urlsafe()
                
                if isinstance(file_ref, Path):
                    if file_ref.exists():
                        input_files[id] = await read_file(file_ref)
                        media["media"] = f"attach://{id}"
                    else:
                        raise FileNotFoundError(f"'{file_ref} not found!'")
                    
                elif isinstance(file_ref, bytes):
                    input_files[id] = file_ref
                    media["media"] = f"attach://{id}"
        
        input_media = json.dumps(media_items)

    return input_files, input_media

async def create_form_data(params: dict, input_files: dict) -> FormData:
    """Create multipart form data for file uploads."""
    form_data = FormData()
    
    for key, file_data in input_files.items():
        form_data.add_field(key, file_data)
    
    for key, value in params.items():
        if key not in input_files:
            form_data.add_field(key, dumps(value) if isinstance(value, (dict, list, tuple)) else str(value))
    
    return form_data
