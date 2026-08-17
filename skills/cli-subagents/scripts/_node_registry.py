from __future__ import annotations

from typing import Any


NODE_IDS = ("claude-code", "codex", "gemini", "grok-build", "cursor", "opencode")


def add_node_state(payload: dict[str, Any], node_id: str) -> None:
    """Compatibility metadata: availability is discovered at runtime."""
    payload["node"] = {"id": node_id, "availability": "runtime"}


def node_gate_payload(node_id: str, _allow_inactive: bool = False) -> None:
    """No static node gate. Doctor and probe establish live availability."""
    if node_id not in NODE_IDS:
        raise ValueError(f"unknown node: {node_id}")
    return None
