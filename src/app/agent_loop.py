import json

import anthropic

from app.config import settings

client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

TOOLS = [
    {
        "name": "get_order_status",
        "description": "Look up shipping status of an order by order ID.",
        "input_schema": {
            "type": "object",
            "properties": {"order_id": {"type": "string"}},
            "required": ["order_id"],
        },
    },
    {
        "name": "lookup_customer",
        "description": "Look up a customer's account details by email.",
        "input_schema": {
            "type": "object",
            "properties": {"email": {"type": "string"}},
            "required": ["email"],
        },
    },
]


# Dummy implementations — Week 3 replaces these with real Postgres queries
def execute_tool(name: str, tool_input: dict) -> str:
    if name == "get_order_status":
        return json.dumps(
            {"order_id": tool_input["order_id"], "status": "shipped", "eta": "2026-09-18"}
        )
    if name == "lookup_customer":
        return json.dumps({"email": tool_input["email"], "customer_id": "CUST-001", "tier": "gold"})
    return json.dumps({"error": f"unknown tool: {name}"})


def run_agent(user_message: str, max_turns: int = 5) -> str:
    messages = [{"role": "user", "content": user_message}]

    for _ in range(max_turns):
        resp = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            tools=TOOLS,
            messages=messages,
        )

        if resp.stop_reason != "tool_use":
            # final answer — concatenate any text blocks
            return "".join(b.text for b in resp.content if b.type == "text")

        # Claude wants tool(s) executed — may be more than one in this turn
        messages.append({"role": "assistant", "content": resp.content})

        tool_results = []
        for block in resp.content:
            if block.type != "tool_use":
                continue
            try:
                result = execute_tool(block.name, block.input)
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                    }
                )
            except Exception as e:
                # tool failures go back to the model as errors, not exceptions —
                # let Claude decide how to recover/communicate the failure
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps({"error": str(e)}),
                        "is_error": True,
                    }
                )

        messages.append({"role": "user", "content": tool_results})

    raise RuntimeError("agent exceeded max_turns without a final answer")


if __name__ == "__main__":
    print(
        run_agent(
            "Is order ORD-9911 shipped, and can you also tell me the tier for customer a@b.com?"
        )
    )
