# CodeOrbit - Code review agent

An AI-powered code review system that automatically detects bugs, edge cases, and architecture violations in pull requests. Built on Google ADK with a multi-agent architecture, tiered LLM routing, and semantic memory via Milvus.

## What is does
- **Bug detection** — nulls, off-by-ones, race conditions, uncaught exceptions
- **Semantic review** — dead code, type mismatches, naming violations, unreachable branches
- **Architecture analysis** — SOLID violations, layer coupling, import graph regressions
- **Contextual suggestions** — actor-critic loop produces actionable fix suggestions with code examples
- **Institutional memory** — findings are stored in Milvus and retrieved in future reviews, so the system improves over time

Each review is classified by change scope (trivial / moderate / architectural) and routes only the agents that are warranted, keeping costs proportional to actual risk.

## Architectural overview

Trigger (PR webhook / manual)
    │
    ▼
Git Agent          ← AST-aware chunking, dual Milvus ingest
    │
    ▼
Orchestrator       ← classifies scope, fans out to specialists
    │
    ├── Semantic Agent   ┐
    ├── Bug Agent        ├── parallel execution
    ├── Arch Agent       │   each with scoped Milvus retrieval
    └── RAG Agent        ┘
    │
    ▼
Suggestion Agent   ← dedup → actor draft → critic gate → output
    │
    ▼
PR comments + findings stored to Milvus

## Tech stack
- Agent Framework: [Google ADK](https://google.github.io/adk-docs/get-started/python/)
- LLM Routing: [LiteLLM](https://docs.litellm.ai/docs/)
- Vector Store: [Milvus](https://milvus.io/docs)

## Prerequisites
- Python 3.14
- LiteLLM proxy server
- Milvus vector store
