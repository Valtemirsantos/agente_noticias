# Agente de Notícias
# Autor: Valtemir Santos.

Agente em Python para responder perguntas sobre notícias usando a biblioteca Agno e a API da NewsAPI.

## Funcionalidades

- busca notícias atuais
- valida chaves de API
- responde em português
- destaca título, fonte, data e link
- usa fallback quando a busca por país não retorna resultados

## Requisitos

- Python 3.11+
- chave válida da OpenAI
- chave válida da NewsAPI

## Instalação

1. Clone o projeto e entre na pasta:

```bash
cd agente_noticias
```

2. Crie um ambiente virtual:

```bash
python -m venv .venv
```

3. Ative o ambiente virtual:

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

4. Instale as dependências:

```bash
pip install -r requirements.txt
```

## Configuração

Crie um arquivo `.env` na raiz do projeto com as variáveis abaixo:

```env
OPENAI_API_KEY=sua_chave_real_da_openai
OPENAI_MODEL=gpt-5.4-mini
NEWSAPI_KEY=sua_chave_real_da_newsapi
```

Importante:
- nunca compartilhe o arquivo `.env`
- não publique a chave em repositórios públicos
- mantenha o `.env` fora do Git
- use o arquivo `.env.example` apenas como modelo, sem inserir chaves reais nele

## Execução

Execute o agente com uma pergunta:

```bash
python agente_noticias.py "Quais são as principais notícias do Brasil hoje?"
```

Ou apenas:

```bash
python agente_noticias.py
```

## Testes

Execute os testes unitários com:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

## Estrutura do projeto

- `agente_noticias.py` — ponto de entrada do agente
- `noticias_api.py` — cliente e wrapper da NewsAPI
- `.env` — variáveis locais sensíveis, ocultas e ignoradas pelo Git
- `.env.example` — modelo de configuração sem chaves reais
- `requirements.txt` — dependências

## Observações

- A NewsAPI exige uma chave real e válida.
- O projeto rejeita valores de exemplo como `sua_chave_da_newsapi`.
- A OpenAI precisa de uma API key ativa para responder as perguntas.

## Solução de problemas

### Erro: `Configure OPENAI_API_KEY`
Verifique se a variável `OPENAI_API_KEY` existe no `.env` ou no ambiente do sistema.

### Erro: `Configure uma chave real da NewsAPI`
Verifique se a variável `NEWSAPI_KEY` foi preenchida corretamente.

### Erro ao executar o arquivo
Use o nome correto:

```bash
python agente_noticias.py
```

Não use `python agente_noticias` sem a extensão.
