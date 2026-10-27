import base64
import unittest

from photo_listing import ImageInputError, decode_image_data_url, validate_photo_request, unavailable_response


def data_url(mime: str, raw: bytes) -> str:
    return f"data:{mime};base64," + base64.b64encode(raw).decode("ascii")


class PhotoListingValidationTests(unittest.TestCase):
    def test_valid_png_signature(self):
        mime, raw = decode_image_data_url(data_url("image/png", b"\x89PNG\r\n\x1a\n" + b"x"))
        self.assertEqual(mime, "image/png")
        self.assertTrue(raw.startswith(b"\x89PNG"))

    def test_rejects_mime_signature_mismatch(self):
        with self.assertRaises(ImageInputError):
            decode_image_data_url(data_url("image/png", b"not a png"))

    def test_requires_at_least_one_image(self):
        with self.assertRaises(ImageInputError):
            validate_photo_request({"images": []})

    def test_max_five_images(self):
        item = data_url("image/png", b"\x89PNG\r\n\x1a\n" + b"x")
        with self.assertRaises(ImageInputError):
            validate_photo_request({"images": [item] * 6})

    def test_unconfigured_model_is_not_faked(self):
        result = unavailable_response()
        self.assertFalse(result["ok"])
        self.assertEqual(result["kind"], "recognition_unavailable")
        self.assertIsNone(result["recognitionSource"])


if __name__ == "__main__":
    unittest.main()
