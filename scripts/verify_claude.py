import anthropic

from app.config import settings

client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
resp = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=100,
    messages=[{"role": "user", "content": "Reply with just: OK"}],
)
print(resp.content[0].text)
