"""Agente de IA para pesquisa e resumo de notícias."""
# Este módulo define um agente de IA para pesquisa e resumo de notícias.
# Autor: Valtemir Santos.
from __future__ import annotations

import argparse
import os

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv

from noticias_api import buscar_noticias_para_agente


def criar_agente() -> Agent:
	"""Cria o agente com a ferramenta de consulta de notícias."""
	load_dotenv()
	if not os.getenv("OPENAI_API_KEY"):
		raise RuntimeError(
			"Configure OPENAI_API_KEY no ambiente ou no arquivo .env."
		)
	model_id = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")
	return Agent(
		name="Agente de Notícias",
		model=OpenAIChat(id=model_id),
		tools=[buscar_noticias_para_agente],
		instructions=[
			"Você é um analista de notícias em português do Brasil.",
			"Use a ferramenta de notícias antes de responder sobre fatos atuais.",
			"Não invente informações; informe quando a busca não retornar resultados.",
			"Responda sempre em formato simples e legível para usuário final.",
			"Organize a resposta em uma lista numerada, com um item por notícia.",
			"Para cada notícia, mostre: Título, Fonte, Data, URL e um resumo em 1 ou 2 frases.",
			"Use quebras de linha claras entre cada notícia e evite blocos longos de texto sem separação.",
			"Separe fatos encontrados de qualquer análise ou contexto adicional.",
		],
		markdown=True,
	)


def executar(pergunta: str) -> str:
	"""Executa uma pergunta e retorna o texto produzido pelo agente."""
	resultado = criar_agente().run(pergunta)
	return str(resultado.content or "O agente não retornou conteúdo.")


def main() -> None:
	load_dotenv()
	parser = argparse.ArgumentParser(description="Consulta notícias usando Agno.")
	parser.add_argument(
		"pergunta",
		nargs="?",
		default="Quais são as principais notícias do Brasil hoje?",
	)
	args = parser.parse_args()
	print(executar(args.pergunta))


if __name__ == "__main__":
	main()
