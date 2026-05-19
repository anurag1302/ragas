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

#### Legal documents

- Structure
  - clauses
  - sub-clauses
  - definitions
  - references to other sections

- Best chunking
  - hierarchical + clause-aware chunking
    - exact wording
    - references ("see section 3.2")
    - dependencies

#### Technical manuals / SOPs

- Structure
  - steps
  - procedures
  - warnings
  - instructions
- Best chunking
  - step-based + paragraph grouping
