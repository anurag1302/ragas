### Chunking is NOT a fixed algorithm.

It is a design choice about how you want meaning to be packaged. There is no universal chunking strategy because chunking depends on

1. document structure
2. retrieval goal
3. question type
4. domain semantics
5. how the LLM will use context

### Why different domains need different chunking

#### Research papers (scientific RAG)

- Structure
  - abstract
  - intro
  - methodology
  - results
  - conclusion
- Best chunking
  - structure-aware + section-based chunking
    - each section = one idea
    - citations matter
    - tables/figures are localized
