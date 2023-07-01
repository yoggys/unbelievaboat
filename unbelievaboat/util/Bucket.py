import time
import asyncio
from typing import Callable


class Bucket(list):
    def __init__(self, limit: int = 1) -> None:
        super().__init__()
        self.processing: bool = False
        self.limit: int = limit
        self.remaining: int = limit
        self.reset: float = None
        self.semaphore = asyncio.Semaphore(limit)

    def queue(self, request: Callable[[], None]) -> None:
        self.append(request)
        if not self.processing:
            self.processing = True
            self.execute()

    async def execute(self) -> None:
        if not self:
            self.processing = False
            return

        now: float = time.time()
        if not self.reset or self.reset < now:
            self.reset = now
            self.remaining = self.limit

        if self.remaining <= 0:
            self.processing = self.execute
            time_to_wait: float = max(0, self.reset - now)
            await asyncio.sleep(time_to_wait)
            return

        self.remaining -= 1

        request: Callable[[], None] = self.pop(0)
        await request(self.execute)
