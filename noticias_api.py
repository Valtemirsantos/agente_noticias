"""Cliente simples para a API NewsAPI."""

from __future__ import annotations

import os
import logging
from dataclasses import asdict, dataclass
from typing import Any

import httpx


logger = logging.getLogger(__name__)
NEWS_API_URL = "https://newsapi.org/v2/top-headlines"
NEWS_API_EVERYTHING_URL = "https://newsapi.org/v2/everything"
PLACEHOLDER_API_KEYS = {
    "sua_chave_da_newsapi",
    "cole_sua_chave_da_newsapi_aqui",
    "coloque_sua_chave_da_newsapi_aqui",
    "YOUR_NEWSAPI_KEY",
}


def normalizar_api_key(chave: str | None) -> str | None:
    """Valida e normaliza a chave da API da NewsAPI."""
    if chave is None:
        return None

    valor = chave.strip()
    if not valor:
        return None

    valor = valor.strip("\"' ")
    if not valor:
        return None

    if valor in PLACEHOLDER_API_KEYS:
        return None

    lowered = valor.lower()
    if "sua_chave" in lowered or "cole_sua" in lowered or "coloque_sua" in lowered:
        return None

    return valor


@dataclass(frozen=True)
class NewsArticle:
	"""Representa os campos úteis de uma notícia."""

	title: str
	description: str
	url: str
	source: str
	published_at: str

	def as_dict(self) -> dict[str, str]:
		return asdict(self)


def _extrair_artigos(payload: dict[str, Any]) -> list[NewsArticle]:
	"""Normaliza a resposta da NewsAPI para objetos NewsArticle."""
	articles: list[NewsArticle] = []
	for item in payload.get("articles", []):
		if not item.get("title") or item.get("title") == "[Removed]":
			continue
		articles.append(
			NewsArticle(
				title=item.get("title", ""),
				description=item.get("description") or "Sem descrição.",
				url=item.get("url", ""),
				source=(item.get("source") or {}).get("name", "Fonte desconhecida"),
				published_at=item.get("publishedAt", "Data desconhecida"),
			)
		)
	return articles


def _obter_payload(response: httpx.Response, endpoint: str) -> dict[str, Any]:
	"""Valida uma resposta da NewsAPI sem registrar dados sensíveis."""
	try:
		response.raise_for_status()
	except httpx.HTTPError as error:
		logger.error("Falha HTTP na NewsAPI (%s): %s", endpoint, type(error).__name__)
		raise RuntimeError("Não foi possível consultar a NewsAPI.") from error

	try:
		payload = response.json()
	except ValueError as error:
		logger.error("Resposta JSON inválida da NewsAPI (%s).", endpoint)
		raise RuntimeError("A NewsAPI retornou uma resposta inválida.") from error

	if not isinstance(payload, dict):
		logger.error("Payload inesperado da NewsAPI (%s).", endpoint)
		raise RuntimeError("A NewsAPI retornou uma resposta inválida.")

	if payload.get("status") != "ok":
		logger.warning("A NewsAPI retornou status de erro (%s).", endpoint)
		message = payload.get("message", "status inválido")
		raise RuntimeError(f"A NewsAPI retornou um erro: {message}")

	return payload


def buscar_noticias(
	query: str | None = None,
	*,
	country: str = "br",
	category: str | None = None,
	page_size: int = 10,
	timeout: float = 15.0,
) -> list[NewsArticle]:
	"""Busca notícias atuais e retorna uma lista normalizada."""
	api_key = normalizar_api_key(os.getenv("NEWSAPI_KEY"))
	if not api_key:
		raise RuntimeError(
			"Configure uma chave real da NewsAPI na variável NEWSAPI_KEY do arquivo .env. "
			"Valores de exemplo e placeholders não são aceitos."
		)

	if not 1 <= page_size <= 100:
		raise ValueError("page_size deve estar entre 1 e 100.")

	params: dict[str, Any] = {
		"country": country,
		"pageSize": page_size,
	}
	headers = {"X-Api-Key": api_key}
	if query:
		params["q"] = query
	if category:
		params["category"] = category

	try:
		logger.info("Consultando notícias na NewsAPI (country=%s, page_size=%s).", country, page_size)
		response = httpx.get(NEWS_API_URL, params=params, headers=headers, timeout=timeout)
		payload = _obter_payload(response, NEWS_API_URL)
		articles = _extrair_artigos(payload)
		if articles:
			return articles
		if not query and country == "br":
			logger.info("Busca principal sem resultados; executando fallback da NewsAPI.")
			fallback_params = {"q": "Brasil", "sortBy": "publishedAt", "pageSize": page_size}
			fallback_response = httpx.get(
				NEWS_API_EVERYTHING_URL,
				params=fallback_params,
				headers=headers,
				timeout=timeout,
			)
			fallback_payload = _obter_payload(fallback_response, NEWS_API_EVERYTHING_URL)
			return _extrair_artigos(fallback_payload)
		return articles
	except httpx.HTTPError as error:
		logger.error("Falha de transporte na NewsAPI: %s", type(error).__name__)
		raise RuntimeError("Não foi possível consultar a NewsAPI.") from error


def buscar_noticias_para_agente(
	query: str = "",
	country: str = "br",
	category: str = "",
	page_size: int = 5,
) -> list[dict[str, str]]:
	"""Ferramenta serializável que o agente Agno pode chamar."""
	return [
		article.as_dict()
		for article in buscar_noticias(
			query=query or None,
			country=country,
			category=category or None,
			page_size=page_size,
		)
	]
