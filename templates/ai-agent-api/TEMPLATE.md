# Railway Template Composer Setup

## Services

| Service | Source |
| --- | --- |
| AI Agent API | GitHub repo (this folder) |

## Variables

| Variable | Value | Description |
| --- | --- | --- |
| `OPENAI_API_KEY` | *(user provided)* | OpenAI API key |
| `OPENAI_MODEL` | `gpt-4o-mini` | Model with tool-calling support |
| `API_KEY` | `${{secret(32)}}` | Protects `/v1/agent` |
| `MAX_TOOL_ROUNDS` | `5` | Safety cap on tool loops |

## Settings

- **Healthcheck path:** `/health`
- Enable **public HTTP** networking

## Publish metadata

- **Category:** AI
- **Description:** OpenAI tool-calling agent API with extensible tools and request tracing.
