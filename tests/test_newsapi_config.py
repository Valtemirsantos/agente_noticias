import os
import unittest
from unittest.mock import patch

from noticias_api import normalizar_api_key


class NewsApiKeyValidationTests(unittest.TestCase):
    def test_placeholder_is_rejected(self):
        self.assertIsNone(normalizar_api_key("sua_chave_da_newsapi"))
        self.assertIsNone(normalizar_api_key("cole_sua_chave_da_newsapi_aqui"))

    def test_real_key_is_kept(self):
        self.assertEqual(normalizar_api_key("  abc123def456  "), "abc123def456")

    def test_missing_key_is_rejected(self):
        self.assertIsNone(normalizar_api_key(""))
        self.assertIsNone(normalizar_api_key(None))


if __name__ == "__main__":
    unittest.main()
