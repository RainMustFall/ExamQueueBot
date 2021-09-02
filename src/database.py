import aioredis
import typing as tp


class Database:
    def __init__(self, url: str, password: str):
        self._connection = aioredis.from_url(url=url, password=password,
                                             encoding="utf-8", decode_responses=True)

    async def set(self, key: int, value: tp.List[str]) -> None:
        await self._connection.set(key, "\n".join(value))

    async def get(self, key: int) -> tp.Optional[tp.List[str]]:
        value = await self._connection.get(key)
        if value:
            return value.split("\n")
        return None
