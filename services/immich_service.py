import os
import random
import logging
from typing import Any, Optional

import aiohttp
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

IMMICH_API_KEY = os.getenv("IMMICH_API_KEY")
IMMICH_URL = os.getenv("IMMICH_URL")
IMMICH_BRUNO_ALBUM_ID = os.getenv("IMMICH_BRUNO_ALBUM_ID")
IMMICH_DEBUG = os.getenv("IMMICH_DEBUG", "false").lower() in {"1", "true", "yes", "on"}


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
    image, _ = await get_random_bruno_image_with_reason()
    return image


async def get_random_bruno_image_with_reason() -> tuple[Optional[dict[str, Any]], Optional[str]]:
    if not IMMICH_API_KEY or not IMMICH_URL or not IMMICH_BRUNO_ALBUM_ID:
        reason = "Immich config missing"
        if IMMICH_DEBUG:
            logger.warning(reason)
        return None, reason

    album_url = f"{IMMICH_URL}/albums/{IMMICH_BRUNO_ALBUM_ID}"

    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        try:
            async with session.get(album_url, headers=_get_headers()) as response:
                if response.status != 200:
                    reason = f"Album request failed (HTTP {response.status})"
                    if IMMICH_DEBUG:
                        logger.warning(reason)
                    return None, reason
                album_data = await response.json()
        except Exception as error:
            reason = f"Album request error ({type(error).__name__})"
            if IMMICH_DEBUG:
                logger.exception(reason)
            return None, reason

        assets = album_data.get("assets", [])
        if not assets:
            reason = "Album has no assets"
            if IMMICH_DEBUG:
                logger.warning(reason)
            return None, reason

        asset = random.choice(assets)
        asset_id = asset.get("id")
        if not asset_id:
            reason = "Selected asset missing id"
            if IMMICH_DEBUG:
                logger.warning(reason)
            return None, reason

        thumb_url = f"{IMMICH_URL}/assets/{asset_id}/thumbnail"
        original_url = f"{IMMICH_URL}/assets/{asset_id}/original"

        for url in (thumb_url, original_url):
            try:
                async with session.get(url, headers=_get_headers()) as image_response:
                    if image_response.status != 200:
                        if IMMICH_DEBUG:
                            logger.warning("Asset request failed (HTTP %s) for %s", image_response.status, url)
                        continue

                    image_bytes = await image_response.read()
                    if not image_bytes:
                        if IMMICH_DEBUG:
                            logger.warning("Asset response empty for %s", url)
                        continue

                    content_type = image_response.headers.get("Content-Type")
                    extension = _get_file_extension(content_type)

                    return {
                        "filename": f"bruno_{asset_id}.{extension}",
                        "bytes": image_bytes,
                    }, None
            except Exception as error:
                if IMMICH_DEBUG:
                    logger.exception("Asset request error (%s) for %s", type(error).__name__, url)
                continue

    return None, "Asset download failed"
