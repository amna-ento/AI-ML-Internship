A CLI or API-backed assistant with real capabilities.

At least three working tools: a calculator, one that calls a real external API (weather, currency, anything), and one that queries a local database or file
The model decides which tool to call — no hardcoded routing
All output validated against a Pydantic schema before use
Streaming responses
Retry with backoff on transient errors
Token usage and estimated cost logged per request
Graceful handling of: rate limits, timeouts, malformed model output, tool failure
One MCP server connected, as a demo