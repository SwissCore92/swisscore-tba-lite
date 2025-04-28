import typing as t
from pathlib import Path
from base64 import b64encode

import aiohttp
import aiofiles

class FileDownloader:
    def __init__(self, file_url: str, session: aiohttp.ClientSession):
        self.file_url = file_url
        self.session = session
        self._response: aiohttp.ClientResponse | None = None 
    
    async def __aenter__(self) -> "FileDownloader":
        self._response = await self.session.get(self.file_url)
        self._response.raise_for_status()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self._response:
            await self._response.release()
    
    async def as_file(self, file_path: Path | str, overwrite: bool = True) -> None:
        file_path = Path(file_path)

        if not file_path.parent.exists():
            raise FileNotFoundError(f"{file_path.parent} was not found.")

        if file_path.exists() and not overwrite:
            raise FileExistsError(f"{file_path} already exists and overwiting is not allowed.")

        async with aiofiles.open(file_path, "wb") as f:
            async for chunk in self.iter_bytes():
                await f.write(chunk)

    async def as_text(self, encoding: str = "utf-8") -> str:
        return (await self.as_bytes()).decode(encoding)
    
    @t.overload
    async def as_base64(self) -> bytes: ...
    
    @t.overload
    async def as_base64(self, encoding: str = ...) -> str: ...

    async def as_base64(self, encoding: str | None = None) -> str | bytes:
        b64 = b64encode(await self.as_bytes())
        return b64 if not encoding else b64.decode(encoding)
    
    async def as_bytes(self) -> bytes:
        content = b""
        async for chunk in self.iter_bytes():
            content += chunk
        return content
    
    async def iter_bytes(self, bs: int = 16384) -> t.AsyncGenerator[bytes]:
        if not self._response:
            async with self.session.get(self.file_url) as r:
                r.raise_for_status()
                async for chunk in r.content.iter_chunked(bs):
                    yield chunk
            return
        
        async for chunk in self._response.content.iter_chunked(bs):
            yield chunk

