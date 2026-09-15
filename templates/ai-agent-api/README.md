# AI Agent API

A FastAPI service that runs a simple OpenAI agent with tools. You send a prompt, the model can call tools if it needs to, and you get back the answer plus a log of what tools ran.

## What you get

- POST `/v1/agent` with a `prompt` field
- Built-in tools: get current time, basic calculator
- Tool trace in the response so you can see what happened
- Easy to add your own tools in `app/tools.py`

## Deploy on Railway

1. Deploy this repo from GitHub.
2. Set variables:
   - `OPENAI_API_KEY` = your OpenAI key
   - `OPENAI_MODEL` = `gpt-4o-mini`
   - `API_KEY` = `${{secret(32)}}`
   - `MAX_TOOL_ROUNDS` = `5` (optional safety limit)
3. Enable public networking and deploy.

## Run locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --port 8000
```

## Environment variables

| Variable | Required | What it does |
| --- | --- | --- |
| `OPENAI_API_KEY` | Yes | OpenAI API key |
| `OPENAI_MODEL` | No | Chat model with tool support |
| `API_KEY` | No | Protects `/v1/agent` |
| `MAX_TOOL_ROUNDS` | No | Max tool loops (default 5) |

## Try the API

```bash
curl -X POST http://localhost:8000/v1/agent \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d "{\"prompt\":\"What is 25 times 4? Use the calculator.\"}"
```

## Adding your own tools

Edit `app/tools.py`:
1. Add a tool definition to the `TOOLS` list
2. Handle it in the `run_tool` function

## Author

romeoxt — herbylegall9@gmail.com

## License

MIT
