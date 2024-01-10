import os

import json
import aiofiles


async def get_json(filename: str) -> dict:
    path = f"data/{filename}"

    if os.path.exists(path):
        async with aiofiles.open(path, "r", encoding="utf-8") as file:
            return json.loads(await file.read())
    return {}

print(get_json('book.json'))