---
name: gpt-researcher
description: Autonomous deep research from Codex via GPT Researcher/MCP.
---

# GPT Researcher For Codex

Use GPT Researcher from Codex when a task needs autonomous deep research, multi-source synthesis, or MCP-backed research workflows.

Source: https://github.com/assafelovic/gpt-researcher
Installed: 2026-07-02

## When To Use

- Deep research tasks that need source-backed synthesis across many web or local sources.
- Research workflows where GPT Researcher's planner/execution/publisher model is useful.
- MCP research flows after the GPT Researcher runtime and credentials are configured.

## Local Setup Note

This workspace-local personal skill is only the skill wrapper. The full GPT Researcher runtime is not vendored here. Running GPT Researcher still requires a Python environment plus the required provider/search credentials, typically `OPENAI_API_KEY` and `TAVILY_API_KEY`, or an approved local/OpenAI-compatible setup.

Do not upload client-confidential PDFs, RFQ packages, or P&IDs to third-party tools through this skill without explicit approval.
