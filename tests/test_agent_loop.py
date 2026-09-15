from unittest.mock import MagicMock, patch  # noqa: F401

from app.agent_loop import execute_tool


def test_execute_tool_order_status():
    result = execute_tool("get_order_status", {"order_id": "ORD-1"})
    assert "shipped" in result


def test_execute_tool_unknown():
    result = execute_tool("nonexistent", {})
    assert "error" in result
