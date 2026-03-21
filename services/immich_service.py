import os
import random
from typing import Any, Optional

import aiohttp
from dotenv import load_dotenv

load_dotenv()

IMMICH_API_KEY = os.getenv("IMMICH_API_KEY")
IMMICH_URL = os.getenv("IMMICH_URL")
IMMICH_BRUNO_ALBUM_ID = os.getenv("IMMICH_BRUNO_ALBUM_ID")


def _get_headers() -> dict[str, str]:
    return {
        "x-api-key": IMMICH_API_KEY or "",
        "Accept": "application/json",
    }


def _get_file_extension(content_type: Optional[str]) -> str:
    mapping = {
        "image/jpeg": "jpg",
        "image/jpg": "jpg",
        "image/png": "png",
        "image/webp": "webp",
        "image/gif": "gif",
    }
    if not content_type:
        return "jpg"
    return mapping.get(content_type.lower(), "jpg")


async def get_random_bruno_image() -> Optional[dict[str, Any]]:
    if not IMMICH_API_KEY or not IMMICH_URL or not IMMICH_BRUNO_ALBUM_ID:
        return None

    album_url = f"{IMMICH_URL}/albums/{IMMICH_BRUNO_ALBUM_ID}"

    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        try:
            async with session.get(album_url, headers=_get_headers()) as response:
                if response.status != 200:
                    return None
                album_data = await response.json()
        except Exception:
            return None

        assets = album_data.get("assets", [])
        if not assets:
            return None

        asset = random.choice(assets)
        asset_id = asset.get("id")
        if not asset_id:
            return None

        thumb_url = f"{IMMICH_URL}/assets/{asset_id}/thumbnail"
        original_url = f"{IMMICH_URL}/assets/{asset_id}/original"

        for url in (thumb_url, original_url):
            try:
                async with session.get(url, headers=_get_headers()) as image_response:
                    if image_response.status != 200:
                        continue

                    image_bytes = await image_response.read()
                    if not image_bytes:
                        continue

                    content_type = image_response.headers.get("Content-Type")
                    extension = _get_file_extension(content_type)

                    return {
                        "filename": f"bruno_{asset_id}.{extension}",
                        "bytes": image_bytes,
                    }
            except Exception:
                continue

    return None
