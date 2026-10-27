"""Photo-listing boundary for TUBETU AI.

This module validates image payloads and defines a truthful unavailable-model
response. It deliberately does not pretend that heuristics recognize images.
A self-hosted vision adapter can be added behind this boundary later.
"""
from __future__ import annotations

import base64
import binascii
from typing import Any

MAX_IMAGES = 5
MAX_IMAGE_BYTES = 8 * 1024 * 1024
ALLOWED_MIME = {"image/jpeg", "image/png", "image/webp"}
SIGNATURES = {
    "image/jpeg": (b"\xff\xd8\xff",),
    "image/png": (b"\x89PNG\r\n\x1a\n",),
    "image/webp": (b"RIFF",),
}


class ImageInputError(ValueError):
    """An uploaded image is invalid or outside configured limits."""


def decode_image_data_url(value: str) -> tuple[str, bytes]:
    """Validate and decode a data URL; return (MIME type, bytes)."""
    if not isinstance(value, str) or not value.startswith("data:") or "," not in value:
        raise ImageInputError("Изображение передано в неподдерживаемом формате.")
    header, encoded = value.split(",", 1)
    mime = header[5:].split(";", 1)[0].lower()
    if mime not in ALLOWED_MIME or ";base64" not in header.lower():
        raise ImageInputError("Поддерживаются только изображения JPEG, PNG и WebP.")
    try:
        raw = base64.b64decode(encoded, validate=True)
    except (binascii.Error, ValueError):
        raise ImageInputError("Не удалось прочитать изображение.") from None
    if not raw:
        raise ImageInputError("Файл изображения пуст.")
    if len(raw) > MAX_IMAGE_BYTES:
        raise ImageInputError("Размер одной фотографии не должен превышать 8 МБ.")
    signatures = SIGNATURES[mime]
    if mime == "image/webp":
        valid = len(raw) >= 12 and raw.startswith(b"RIFF") and raw[8:12] == b"WEBP"
    else:
        valid = any(raw.startswith(sig) for sig in signatures)
    if not valid:
        raise ImageInputError("Содержимое файла не соответствует типу изображения.")
    return mime, raw


def validate_photo_request(payload: dict[str, Any]) -> list[tuple[str, bytes]]:
    """Validate up to five image data URLs without storing or echoing image data."""
    images = payload.get("images")
    if not isinstance(images, list) or not images:
        raise ImageInputError("Добавьте хотя бы одну фотографию.")
    if len(images) > MAX_IMAGES:
        raise ImageInputError("Можно добавить не более 5 фотографий за один раз.")
    return [decode_image_data_url(item) for item in images]


def unavailable_response() -> dict[str, Any]:
    """Return an explicit state until a real vision model is deployed."""
    return {
        "ok": False,
        "kind": "recognition_unavailable",
        "code": "VISION_MODEL_NOT_CONFIGURED",
        "message": "Распознавание фотографий пока не подключено. Фотографии сохранены; заполните карточку вручную.",
        "recognitionSource": None,
    }
