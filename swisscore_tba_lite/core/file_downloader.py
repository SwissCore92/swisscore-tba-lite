import asyncio
import typing as t
from pathlib import Path
from base64 import b64encode

import aiohttp
import aiofiles

tasks: list[asyncio.Task] = []

def create_task(coro, name: str | None = None):
    task = asyncio.create_task(coro, name=name)
    tasks.append(task)
    task.add_done_callback(tasks.remove)
    return task

class FileDownloader:
    def __init__(self, file_url: str, session: aiohttp.ClientSession) -> None:
        self.file_url = file_url
        self.session = session

        self._callback: t.Callable[[bytes | str | Path], None] | None = None
    
    def then(self, callback: t.Callable[[bytes | str | Path], None]) -> "FileDownloader":
        self._callback = callback
        return self
    
    async def as_file(self, file_path: Path | str, overwrite: bool = False) -> asyncio.Task[Path]:
        async def _as_file():
            nonlocal file_path

            file_path = Path(file_path)

            if not file_path.parent.exists():
                raise FileNotFoundError(f"{file_path.parent} was not found.")

            if file_path.exists() and not overwrite:
                raise FileExistsError(f"{file_path} already exists and overwiting is not allowed.")

            async with aiofiles.open(file_path, "wb") as f:
                async for chunk in self.iter_bytes():
                    await f.write(chunk)

            if self._callback:                      
                if asyncio.iscoroutinefunction(self._callback):
                    await self._callback(file_path)
                else:
                    self._callback(file_path)
            
            return file_path

        return create_task(_as_file(), f"{self.__class__.__name__}.as_file")


    def as_text(self, encoding: str = "utf-8") -> asyncio.Task[str]:
        async def _as_text():
            result = (await self.as_bytes()).decode(encoding)

            if self._callback:
                if asyncio.iscoroutinefunction(self._callback):
                    await self._callback(result)
                else:
                    self._callback(result)
            
            return result

        return create_task(_as_text(), f"{self.__class__.__name__}.as_text")
    

    @t.overload
    def as_base64(self) -> asyncio.Task[bytes]: ...
    @t.overload
    def as_base64(self, encoding: str = ...) -> asyncio.Task[str]: ...

    def as_base64(self, encoding: str | None = None) -> asyncio.Task[str | bytes]:
        async def _as_base64():
            parts: list[bytes] = []
            async for chunk in self.iter_bytes():
                parts.append(chunk)
            
            b64 = b64encode(b"".join(parts))

            if encoding:
                b64 = b64.decode(encoding)

            if self._callback:
                if asyncio.iscoroutinefunction(self._callback):
                    await self._callback(b64)
                else:
                    self._callback(b64)

            return b64
        
        return create_task(_as_base64(), f"{self.__class__.__name__}.as_base64")
    

    def as_bytes(self) -> asyncio.Task[bytes]:
        async def _as_bytes() -> bytes:
            content = b""
            async for chunk in self.iter_bytes():
                content += chunk
            return content
        
        return create_task(_as_bytes(), f"{self.__class__.__name__}.as_bytes")
    
    async def iter_bytes(self, bs: int = 16384) -> t.AsyncGenerator[bytes]:
        async with self.session.get(self.file_url) as r:
            r.raise_for_status()
            async for chunk in r.content.iter_chunked(bs):
                yield chunk

