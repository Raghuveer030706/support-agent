import anthropic

from app.config import settings

client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

tools = [
    {
        "name": "get_order_status",
        "description": "Look up the shipping status of a customer order by order ID.",
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {"type": "string", "description": "The order ID, e.g. ORD-1234"}
            },
            "required": ["order_id"],
        },
    }
]

resp = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "Where is my order ORD-1234?"}],
)

print(resp.stop_reason)  # should be "tool_use"
for block in resp.content:
    print(block.type, getattr(block, "input", None))
