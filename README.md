# NetOps GenAI Assistant

Agentic RAG assistant for network-operations incident triage: retrieves relevant runbook
docs, queries operational KPI data via a tool, and returns a structured triage decision
(severity, likely cause, recommended steps, cited sources). Includes an evaluation harness
and a KPI-anomaly analytics module.

Status: under active development — see commit history for progress.

## Stack
Python 3.11, sentence-transformers, Chroma, Ollama (llama3.1:8b), FastAPI, pandas,
matplotlib, ragas.

## Setup
```
python3.11 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
ollama pull llama3.1:8b
```
