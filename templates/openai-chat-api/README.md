# OpenAI Chat API

A small FastAPI service that wraps the OpenAI chat API. Your apps talk to this server instead of calling OpenAI directly, so you keep your API key on the server.

## What you get

- POST `/v1/chat` for normal JSON responses
- Same endpoint with `"stream": true` for streaming (SSE)
- GET `/health` for Railway
- Optional API key protection

## Deploy on Railway

1. Deploy this repo from GitHub.
2. Set these variables on the service:
   - `OPENAI_API_KEY` = your OpenAI key
   - `OPENAI_MODEL` = `gpt-4o-mini` (or another model)
   - `API_KEY` = `${{secret(32)}}` to lock down the endpoint
3. Turn on public networking.
4. Deploy and hit `/health`.

No database needed for this one.

## Run locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --port 8000
```

Fill in `OPENAI_API_KEY` in your `.env` file.

## Environment variables

| Variable | Required | What it does |
| --- | --- | --- |
| `OPENAI_API_KEY` | Yes | Your OpenAI API key |
| `OPENAI_MODEL` | No | Default model (gpt-4o-mini) |
| `API_KEY` | No | Require `X-API-Key` header on `/v1/chat` |

## Try the API

```bash
curl -X POST http://localhost:8000/v1/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d "{\"messages\":[{\"role\":\"user\",\"content\":\"Say hello in one sentence.\"}]}"
```

For streaming, add `"stream": true` to the JSON body.

## Author

romeoxt — herbylegall9@gmail.com

## License

MIT
