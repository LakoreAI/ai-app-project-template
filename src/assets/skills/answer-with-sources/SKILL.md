---
name: answer-with-sources
description: Answer a question using only retrieved context (Postgres rows, Milvus hits) and cite it. Use for RAG-style questions.
---

# Answer with sources

1. Use only the provided context; never answer from memory when context is supplied.
2. Cite each claim with its source id, e.g. `[doc-12]`.
3. If the context does not contain the answer, reply "I don't know based on the available data."
4. Keep the answer short; quote only when exact wording matters.
