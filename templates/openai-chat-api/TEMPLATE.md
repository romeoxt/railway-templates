# Railway Template Composer Setup

## Services

| Service | Source |
| --- | --- |
| OpenAI Chat API | GitHub repo (this folder) |

## Variables

| Variable | Value | Description |
| --- | --- | --- |
| `OPENAI_API_KEY` | *(user provided)* | OpenAI API key. Mark as required in composer. |
| `OPENAI_MODEL` | `gpt-4o-mini` | Default chat model |
| `API_KEY` | `${{secret(32)}}` | Protects `/v1/chat`; clients send `X-API-Key` |

## Settings

- **Healthcheck path:** `/health`
- Enable **public HTTP** networking

## Publish metadata

- **Category:** AI
- **Description:** Private OpenAI chat API with streaming SSE and API-key auth.
