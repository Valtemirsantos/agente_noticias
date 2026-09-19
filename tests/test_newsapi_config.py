import os
import unittest
from unittest.mock import Mock, patch

import httpx

from noticias_api import buscar_noticias, normalizar_api_key


class NewsApiKeyValidationTests(unittest.TestCase):
    def test_placeholder_is_rejected(self):
        self.assertIsNone(normalizar_api_key("sua_chave_da_newsapi"))
        self.assertIsNone(normalizar_api_key("cole_sua_chave_da_newsapi_aqui"))

    def test_real_key_is_kept(self):
        self.assertEqual(normalizar_api_key("  abc123def456  "), "abc123def456")

    def test_missing_key_is_rejected(self):
        self.assertIsNone(normalizar_api_key(""))
        self.assertIsNone(normalizar_api_key(None))


class NewsApiRequestTests(unittest.TestCase):
    def setUp(self):
        self.environment = patch.dict(os.environ, {"NEWSAPI_KEY": "test-secret"})
        self.environment.start()
        self.addCleanup(self.environment.stop)

    @staticmethod
    def _response(payload):
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = payload
        return response

    def test_fallback_returns_articles_and_keeps_key_out_of_url(self):
        primary = self._response({"status": "ok", "articles": []})
        fallback = self._response(
            {
                "status": "ok",
                "articles": [
                    {
                        "title": "Notícia",
                        "description": "Resumo",
                        "url": "https://example.com/noticia",
                        "source": {"name": "Fonte"},
                        "publishedAt": "2026-09-19T12:00:00Z",
                    }
                ],
            }
        )
        with patch("noticias_api.httpx.get", side_effect=[primary, fallback]) as request:
            articles = buscar_noticias()

        self.assertEqual(len(articles), 1)
        self.assertEqual(request.call_args_list[0].kwargs["headers"], {"X-Api-Key": "test-secret"})
        self.assertNotIn("apiKey", request.call_args_list[0].kwargs["params"])

    def test_http_error_does_not_expose_error_details(self):
        response = self._response({})
        response.raise_for_status.side_effect = httpx.RequestError("secret in request")
        with patch("noticias_api.httpx.get", return_value=response):
            with self.assertRaisesRegex(RuntimeError, "Não foi possível consultar") as context:
                buscar_noticias(country="us")

        self.assertNotIn("secret in request", str(context.exception))

    def test_invalid_json_is_reported(self):
        response = self._response({})
        response.json.side_effect = ValueError("JSON inválido")
        with patch("noticias_api.httpx.get", return_value=response):
            with self.assertRaisesRegex(RuntimeError, "resposta inválida"):
                buscar_noticias(country="us")

    def test_invalid_payload_status_is_reported(self):
        response = self._response({"status": "error", "message": "chave inválida"})
        with patch("noticias_api.httpx.get", return_value=response):
            with self.assertRaisesRegex(RuntimeError, "chave inválida"):
                buscar_noticias(country="us")


if __name__ == "__main__":
    unittest.main()
