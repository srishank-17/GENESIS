# GENESIS — Personal Learning Operating System

> **AI that learns how you learn.**
> Dynamic Knowledge Graph + Learner Digital Twin + Adaptive Learning Engine + Diagnostic Intelligence

GENESIS models each learner's knowledge, mastery, mistakes, goals, confidence, and study patterns.

---

## Key Intelligence Pillars

1. **Document Intelligence & Grounded RAG**
   Ingests course material, extracts semantic chunks, creates 1536-dimensional embeddings with pgvector, and provides cited answers with verifiable page references.

2. **Dynamic Knowledge Graph**
   Maintains concept hierarchies, prerequisite relationships (REQUIRES, BUILDS_ON), and taxonomic links in Neo4j.

3. **Learner Digital Twin**
   Append-only event-sourced log (learning_events) driving Bayesian Knowledge Tracing (BKT) to model dynamic cognitive mastery.

4. **Diagnostic Engine: 'Why am I getting this wrong?'**
   Four-tier diagnostic reasoning engine:
   - Deterministic: Neo4j prerequisite graph traversal
   - Statistical: BKT mastery verification across ancestor nodes
   - Graph-Reasoning: Deepest root-cause bottleneck isolation
   - LLM Synthesis: Empathetic, personalized remediation plan with citations

---

## Technology Stack

- **Frontend**: Next.js 14, TypeScript, Tailwind CSS, shadcn/ui, Recharts
- **Backend**: FastAPI, Python 3.12, Pydantic v2, SQLAlchemy 2.0 (asyncpg)
- **Database**: PostgreSQL 16 with pgvector
- **Graph Store**: Neo4j 5 Community Edition
- **Cache / Bus**: Redis 7 (with Redis Streams & Celery)
- **Object Storage**: MinIO / S3-compatible storage
- **AI Models**: OpenAI (GPT-4o, text-embedding-3-small), Cohere Rerank

---

## Quickstart

### Starting Full Stack
1. Clone and enter repository:
   `ash
   cd GENESIS
   `
2. Configure environment:
   `ash
   cp .env.example .env
   `
3. Start entire Docker Compose infrastructure:
   `ash
   docker compose up -d
   `

### Local Services
- **Web App**: http://localhost:3000
- **FastAPI API**: http://localhost:8000
- **Interactive Swagger Docs**: http://localhost:8000/docs
- **MinIO Console**: http://localhost:9001
- **Neo4j Browser**: http://localhost:7474
