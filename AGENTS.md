# Instrucoes do projeto

## Escopo

Estas instrucoes valem para todo o projeto `agente_noticias`.

## Python

- Use Python 3.11 ou superior.
- Preserve a estrutura atual e prefira alteracoes pequenas e objetivas.
- Mantenha as chamadas HTTP usando `httpx`.
- Escreva documentacao e mensagens voltadas ao usuario em portugues do Brasil.

## Testes e validacao

- Execute os testes com:
  `python -m unittest discover -s tests -p "test_*.py" -v`
- Compile os arquivos Python com:
  `python -m compileall -q agente_noticias.py noticias_api.py tests`
- Valide os testes depois de qualquer alteracao em codigo.
- Adicione ou atualize testes ao alterar comportamento.

## Seguranca

- Nunca leia, exiba, registre ou versiona valores de `.env`, tokens ou chaves de API.
- Mantenha `.env` ignorado pelo Git; publique somente `.env.example` com placeholders.
- Nao coloque chaves em URLs, logs, mensagens de erro, README ou codigo-fonte.
- Use o cabecalho `X-Api-Key` para enviar a chave da NewsAPI.
- Registre somente metadados que nao contenham credenciais ou dados pessoais.

## Git

- Nao faca commit de `.env` ou outros arquivos com segredos.
- Verifique `git status` antes de commit e push.
- Nao faca push sem executar os testes e a compilacao.
- Use mensagens de commit curtas e descritivas.
