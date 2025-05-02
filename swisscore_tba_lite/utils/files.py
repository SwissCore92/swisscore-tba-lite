import os
import mimetypes
import typing as t
import json
from secrets import token_urlsafe
from pathlib import Path

import aiofiles

from ..bot_api import objects as tg
from ..core.exceptions import FileProcessingError

class InputFile(t.TypedDict, total=False):
    filename: str
    content: bytes

HttpXFile = tuple[str, bytes, str]

def is_local_file(path: str | Path) -> bool:
    """Check if a string represents a valid local file path."""
    path = path if isinstance(path, Path) else Path(path)
    return path.exists() and path.is_file()

def get_file_size(file: str | Path | bytes) -> int:
    """Get size of a file in bytes"""
    if isinstance(file, bytes):
        return len(file)
    return os.stat(file).st_size

async def read_json_file(path: str | Path) -> dict | t.Any:
    """asynchonously read json file"""
    path = path if isinstance(path, Path) else Path(path)
    async with aiofiles.open(path, "r") as f:
        return json.loads(await f.read())

async def write_json_file(path: str | Path, data, *, indent: int | str | None = None, separators: tuple[str, str] = None) -> None:
    """asynchonously write json file"""
    path = path if isinstance(path, Path) else Path(path)
    async with aiofiles.open(path, "w") as f:
        await f.write(json.dumps(data, indent=indent, separators=separators))

async def read_file(path: Path) -> bytes:
    """Read file as bytes asynchronously."""
    async with aiofiles.open(path, "rb") as f:
        return await f.read()

async def prepare_files(params: dict[str, t.Any], check_files, check_media) -> tuple[dict[str, t.Any], dict[str, HttpXFile] | None]:
    try:
        params, files_1 = await prepare_input_files(check_files, params)
        params, files_2 = await prepare_input_media(check_media, params)
        return params, {**files_1, **files_2} or None

    except Exception as e:
        raise FileProcessingError(f"Error while preparing files: {e}") from e

async def prepare_input_files(check_files: list[str] | None, params: dict[str, t.Any]) -> tuple[dict[str, t.Any], dict[str, HttpXFile]]:
    if not check_files: 
        return params, {}
    
    files: dict[str, HttpXFile] = {}
    
    for key in check_files:

        if key not in params:
            continue

        val = params[key]

        filename: str | None = None

        if isinstance(val, str):
            if is_local_file(val):
                val = Path(val)
            else:
                continue

        if isinstance(val, Path):
            if not val.exists():
                raise FileNotFoundError(f"{val} was not found.")
            
            filename = val.name
            val = await read_file(val)
        
        if isinstance(val, dict) and "content" in val and "filename" in val:
            filename = val["filename"]
            val = val["content"]

        if not isinstance(val, bytes):
            raise TypeError(f"{key!r} was of the wrong type. expected one of (str, Path, bytes, InputFile) but got {type(val)}")
        
        if not filename:
            filename = token_urlsafe()

        params[key] = f"attach://{key}"

        files[key] = (filename, val, mimetypes.guess_type(filename)[0] or "application/octet-stream")
    
    return params, files


async def prepare_input_media(check_media: list[str] | None, params: dict[str, t.Any]) -> tuple[dict[str, t.Any], dict[str, HttpXFile]]:
    if not check_media:
        return params, {}
    
    files: dict[str, HttpXFile] = {}

    for key in check_media:
        if key not in params:
            continue

        val = params[key]

        if not isinstance(val, (list, dict)):
            raise TypeError(f"{key!r} was of the wrong type. expected one of (list, dict) but got {type(val)}")
        
        is_single = False
        if isinstance(val, dict):
            is_single = True
            val = [val]
        
        for media in val:
            if not "media" in media:
                raise TypeError("field 'media' is missing.")

            file_ref = media["media"]

            if isinstance(file_ref, str):
                if is_local_file(file_ref):
                    file_ref = Path(file_ref)
                else:
                    continue
            
            file_id = f"media_{len(files)}"
            
            if isinstance(file_ref, Path):
                if not file_ref.exists():
                    raise FileNotFoundError(f"{file_ref} was not found.")
                filename = file_ref.name
                file_ref = await read_file(file_ref)

                files[file_id] = (filename, file_ref, mimetypes.guess_type(filename)[0] or "application/octet-stream")
                media["media"] = f"attach://{file_id}"
            
            elif isinstance(file_ref, (bytes, dict)):
                filename: str |None = None
                if isinstance(file_ref, dict):
                    if "content" in file_ref and "filename" in file_ref:
                        filename = file_ref["filename"]
                        file_ref = file_ref["content"]
                    else:
                        raise TypeError("invalid InputFile")
                
                if not filename:
                    filename = token_urlsafe()

                files[file_id] = (filename, file_ref, mimetypes.guess_type(filename)[0] or "application/octet-stream")
                media["media"] = f"attach://{file_id}"
        
        params[key] = json.dumps(val[0] if is_single else val)

    return params, files
