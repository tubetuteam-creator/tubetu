import unittest
from main import classify, knowledge, normalize

class CoreTests(unittest.TestCase):
 def test_extracts_sale_fields(self):
  d=classify("Продам перфоратор Bosch за 25000 тенге в Алматы, телефон 87010000000")
  self.assertEqual(d["location"],"Алматы")
  self.assertIn("25000",d["price"])
  self.assertEqual(d["contacts"],"87010000000")
  self.assertEqual(d["category"],"Техника и оборудование")
 def test_navigation(self):
  self.assertTrue(knowledge("Где настройки профиля"))
 def test_normalize_controls(self):
  self.assertEqual(normalize(" hello\x00   world "),"hello world")

if __name__ == "__main__": unittest.main()
