"""Optional self-hosted vision adapter for TUBETU AI.

Install the optional dependencies from requirements-vision.txt and set
TUBETU_VISION_MODEL_ID to enable it. No third-party inference API is called.
"""
from __future__ import annotations

import io
import json
import os
import threading
from typing import Any


MODEL_ID = os.getenv("TUBETU_VISION_MODEL_ID", "").strip()
_lock = threading.Lock()
_processor = None
_model = None
_device = None

CATEGORIES = [
    "Проекты и идеи", "Игры", "Контент", "Товары и ресурсы", "Услуги",
    "Логистика и перевозки", "Финансы", "Недвижимость", "Транспорт",
    "Сельское хозяйство", "Техника и оборудование", "Образование и опыт",
    "Сообщества",
]


def model_ready() -> bool:
    return bool(MODEL_ID)


def _load_model():
    global _processor, _model, _device
    if not MODEL_ID:
        return None, None, None
    if _model is not None and _processor is not None:
        return _processor, _model, _device
    with _lock:
        if _model is not None and _processor is not None:
            return _processor, _model, _device
        try:
            import torch
            from transformers import AutoProcessor, AutoModelForVision2Seq
        except ImportError as exc:
            raise RuntimeError(
                "Vision dependencies are missing. Install ai-core/requirements-vision.txt."
            ) from exc
        _device = "cuda" if torch.cuda.is_available() else "cpu"
        dtype = torch.float16 if _device == "cuda" else torch.float32
        _processor = AutoProcessor.from_pretrained(MODEL_ID)
        _model = AutoModelForVision2Seq.from_pretrained(
            MODEL_ID, torch_dtype=dtype, low_cpu_mem_usage=True
        ).to(_device)
        _model.eval()
    return _processor, _model, _device


def _image_from_bytes(raw: bytes):
    from PIL import Image
    with Image.open(io.BytesIO(raw)) as image:
        image.verify()
    with Image.open(io.BytesIO(raw)) as image:
        image = image.convert("RGB")
        image.thumbnail((1024, 1024))
        return image.copy()


def recognize(images: list[tuple[str, bytes]], note: str = "") -> dict[str, Any]:
    """Return an editable draft; never invent price or location."""
    if not MODEL_ID:
        return {
            "ok": False,
            "kind": "recognition_unavailable",
            "code": "VISION_MODEL_NOT_CONFIGURED",
            "message": "Модель распознавания не настроена на сервере. Фото не потеряны; заполните поля вручную.",
            "recognitionSource": None,
        }
    processor, model, device = _load_model()
    import torch

    pil_images = [_image_from_bytes(raw) for _, raw in images]
    prompt = (
        "You are TUBETU listing assistant. Analyze the provided photos together. "
        "Return ONLY valid JSON with keys recognizedObject, category, title, description, "
        "confidence, unknowns. category MUST be exactly one of: "
        + "; ".join(CATEGORIES)
        + ". Describe only visible facts. Never guess price, location, condition, brand, "
        "or model. Use confidence low if uncertain. Do not publish anything."
    )
    if note.strip():
        prompt += "\nUser-provided context (may be used as stated): " + note.strip()[:1000]
    content = [{"type": "image"} for _ in pil_images]
    content.append({"type": "text", "text": prompt})
    messages = [{"role": "user", "content": content}]
    formatted = processor.apply_chat_template(messages, add_generation_prompt=True)
    inputs = processor(text=formatted, images=pil_images, return_tensors="pt")
    inputs = {key: value.to(device) if hasattr(value, "to") else value for key, value in inputs.items()}
    with torch.inference_mode():
        output = model.generate(**inputs, max_new_tokens=450, do_sample=False)
    generated = output[0][inputs["input_ids"].shape[1]:]
    text = processor.decode(generated, skip_special_tokens=True).strip()
    # Models sometimes wrap JSON in a markdown fence; strip only the fence.
    if text.startswith("```"):
        text = text.split("\n", 1)[-1]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
    try:
        result = json.loads(text)
    except json.JSONDecodeError:
        return {
            "ok": False, "kind": "recognition_failed", "code": "INVALID_MODEL_OUTPUT",
            "message": "Модель не смогла подготовить корректную карточку. Попробуйте другие фотографии.",
            "recognitionSource": "self_hosted_model",
        }
    category = result.get("category")
    if category not in CATEGORIES:
        category = "Товары и ресурсы"
    confidence = result.get("confidence", "low")
    if confidence not in {"high", "medium", "low"}:
        confidence = "low"
    return {
        "ok": True,
        "kind": "draft",
        "recognizedObject": str(result.get("recognizedObject", ""))[:300],
        "confidence": confidence,
        "category": category,
        "title": str(result.get("title", ""))[:120],
        "description": str(result.get("description", ""))[:3000],
        "location": None,
        "price": None,
        "intent": "Предложение",
        "suggestions": result.get("unknowns", []) if isinstance(result.get("unknowns", []), list) else [],
        "recognitionSource": "self_hosted_model",
    }
