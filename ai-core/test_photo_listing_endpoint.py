import base64
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient
import main


def png_data_url() -> str:
    raw = b"\x89PNG\r\n\x1a\n" + b"x"
    return "data:image/png;base64," + base64.b64encode(raw).decode("ascii")


class PhotoListingEndpointTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(main.app)
        self.rate_limit_patch = patch("main.rate_limit", return_value=None)
        self.rate_limit_patch.start()

    def tearDown(self):
        self.rate_limit_patch.stop()

    def test_missing_images_returns_400(self):
        response = self.client.post("/ai/photo-listing", json={"images": []})
        self.assertEqual(response.status_code, 400)
        self.assertIn("фотограф", response.json()["detail"].lower())

    def test_invalid_image_returns_400(self):
        response = self.client.post(
            "/ai/photo-listing",
            json={"images": ["data:image/png;base64,bm90IGEgcG5n"]},
        )
        self.assertEqual(response.status_code, 400)

    def test_calls_adapter_and_returns_draft(self):
        expected = {
            "ok": True,
            "kind": "draft",
            "recognizedObject": "дрель",
            "confidence": "high",
            "category": "Техника и оборудование",
            "title": "Электрическая дрель",
            "description": "Электрическая дрель с видимым корпусом и рукояткой.",
            "location": None,
            "price": None,
            "intent": "Предложение",
            "suggestions": [],
            "recognitionSource": "self_hosted_model",
        }
        with patch("main.recognize_photos", return_value=expected) as adapter:
            response = self.client.post(
                "/ai/photo-listing",
                json={"images": [png_data_url()], "note": "инструмент"},
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["category"], "Техника и оборудование")
        self.assertIsNone(response.json()["price"])
        adapter.assert_called_once()

    def test_no_model_returns_explicit_unavailable_state(self):
        unavailable = {
            "ok": False,
            "kind": "recognition_unavailable",
            "code": "VISION_MODEL_NOT_CONFIGURED",
            "message": "Модель не настроена",
            "recognitionSource": None,
        }
        with patch("main.recognize_photos", return_value=unavailable):
            response = self.client.post(
                "/ai/photo-listing", json={"images": [png_data_url()]}
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["kind"], "recognition_unavailable")


if __name__ == "__main__":
    unittest.main()
