import asyncio
import time
from typing import Any, Callable


class Bucket(list):
    def __init__(self, limit: int = 1) -> None:
        super().__init__()
        self.processing: bool = False
        self.limit: int = limit
        self.remaining: int = limit
        self.reset: float = None
        self.semaphore = asyncio.Semaphore(limit)

    async def queue(self, request: Callable[[], None], *args, **kwargs) -> Any:
        self.append({
            "request": request,
            "args": args,
            "kwargs": kwargs
        })
        if not self.processing:
            self.processing = True
            return await self.execute()

    async def execute(self) -> Any:
        if not self:
            self.processing = False
            return

        now: float = time.time()
        if not self.reset or self.reset < now:
            self.reset = now
            self.remaining = self.limit

        if self.remaining <= 0:
            self.processing = True
            time_to_wait: float = max(0, self.reset - now)
            await asyncio.sleep(time_to_wait)
            self.processing = False
            return await self.execute()

        self.remaining -= 1

        entry: Callable[[], None] = self.pop(0)
        result = await entry["request"](*entry["args"], **entry["kwargs"])
        self.processing = False
        return result

