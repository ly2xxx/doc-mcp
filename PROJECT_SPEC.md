# docs-mcp & md-mcp: Project Specification

**Last Updated:** 2026-02-18  
**Status:** Design Phase  
**Architecture:** Two-tier (library + application)

---

## 🎯 Vision

Create a robust, production-ready MCP knowledge base system split into:
1. **md-mcp** - Reusable PyPI library for markdown-based knowledge retrieval
2. **docs-mcp** - User-friendly application for document ingestion and management

---

## 📦 Project 1: md-mcp (PyPI Library)

**Purpose:** Generic markdown knowledge base engine with MCP protocol support

### Core Responsibilities

#### 1. Knowledge Base Management
- Create, load, and manage multiple knowledge bases
- Support namespaced/isolated KBs (multi-tenant ready)
- Schema: `KnowledgeBase(name, path, metadata, config)`
- Operations: `create()`, `load()`, `delete()`, `list()`

#### 2. Chunking Strategies
- **Keyword chunking:** Header-based, paragraph-based, custom delimiters
- **Semantic chunking:** Embedding-based boundary detection
- Configurable chunk size (tokens/chars)
- Overlap support for context continuity
- Metadata preservation (file, line numbers, headers)

#### 3. Indexing & Storage
- **Keyword index:** Full-text search (sqlite FTS5 or similar)
- **Semantic index:** Vector embeddings (FAISS, ChromaDB, or Qdrant)
- Incremental updates: hash-based change detection
- Efficient rebuild: only reprocess modified files

#### 4. Search & Retrieval
- **Hybrid search:** Combine keyword + semantic results
- Configurable weighting: `keyword_weight`, `semantic_weight`
- Ranking/scoring with source attribution
- Return format:
  ```python
  SearchResult(
      text: str,
      score: float,
      source_file: str,
      line_range: tuple[int, int],
      chunk_id: str,
      metadata: dict
  )
  ```

#### 5. MCP Protocol Server
- Implement MCP server specification
- **Tools exposed:**
  - `search_knowledge(query, kb_name, top_k, hybrid_weights)`
  - `list_sources(kb_name)` - enumerate all indexed files
  - `rebuild_index(kb_name, incremental)` - force reindex
  - `get_kb_stats(kb_name)` - chunks, files, last updated
- **Resources:**
  - Expose indexed markdown files as MCP resources
- Integrate with Claude Desktop, Cline, Cursor, etc.

#### 6. Configuration Management
- Per-KB config files (YAML/JSON)
- Settings:
  - Embedding model (local/API)
  - Chunking strategy and params
  - Search weights
  - File patterns (include/exclude)
  - Update frequency

#### 7. Source Attribution
- Every search result includes:
  - Source file path
  - Line number range
  - Section headers (breadcrumb)
  - Last modified timestamp
- Enables citation and follow-up reading

### API Design (Python)

```python
from md_mcp import KnowledgeBase, ChunkingStrategy, SearchConfig

# Create/load KB
kb = KnowledgeBase.create(
    name="my-project",
    source_path="./docs",
    chunking=ChunkingStrategy.SEMANTIC,
    embedding_model="sentence-transformers/all-MiniLM-L6-v2"
)

# Index documents
kb.index(incremental=True)

# Search with hybrid mode
results = kb.search(
    query="how to authenticate users",
    top_k=5,
    config=SearchConfig(keyword_weight=0.3, semantic_weight=0.7)
)

for result in results:
    print(f"{result.source_file}:{result.line_range[0]}-{result.line_range[1]}")
    print(f"Score: {result.score}")
    print(result.text)
```

### Dependencies
- **Embedding:** `sentence-transformers`, `openai` (optional)
- **Vector DB:** `faiss-cpu`, `chromadb`, or `qdrant-client`
- **Search:** `sqlite3` (built-in FTS5) or `whoosh`
- **MCP:** `mcp` (official MCP Python SDK)
- **Utils:** `pydantic`, `pyyaml`, `watchdog` (file monitoring)

### Distribution
- PyPI package: `pip install md-mcp`
- Versioning: Semantic (0.1.0 → 1.0.0)
- License: MIT or Apache 2.0

---

## 🖥️ Project 2: docs-mcp (GUI Application)

**Purpose:** User-friendly document ingestion and knowledge base builder

### Core Responsibilities

#### 1. Document Picker Interface
- **GUI Framework:** Streamlit or Gradio (rapid dev) OR PyQt/Tkinter (native)
- File browser with multi-select
- Drag-and-drop support
- Folder recursive scanning
- Preview selected documents

#### 2. Multi-Format Conversion
- **Supported inputs:**
  - Code repositories (via Repomix)
  - PDFs (via `pypdf` or `pdfplumber`)
  - Office docs: `.docx`, `.xlsx`, `.pptx` (via `python-docx`, `openpyxl`)
  - Web pages (via `trafilatura` or `beautifulsoup4`)
  - Plain text: `.txt`, `.md`, `.rst`
  - Notion exports (ZIP → MD)
  - HTML files
- **Conversion pipeline:**
  1. Detect format
  2. Extract text
  3. Convert to Markdown
  4. Preserve structure (headers, lists, tables)

#### 3. Repomix Integration
- One-click "Add Repository" button
- Configure Repomix options:
  - Include/exclude patterns
  - Comment handling
  - Output style (markdown/xml/plain)
- Output: Single consolidated `.md` file → fed to md-mcp

#### 4. Knowledge Base Configuration UI
- Create/select KB
- Set chunking strategy (dropdown)
- Configure embedding model
- Set search weights (sliders)
- Include/exclude file patterns

#### 5. Batch Processing
- Queue multiple documents/repos
- Progress tracking with status indicators
- Error handling and logs
- Summary report after completion

#### 6. Preview & Testing
- Search test interface
- Query KB and see results
- View source attribution links
- Export search results

#### 7. MCP Server Management
- Start/stop MCP server from GUI
- View server logs
- Test connection (ping)
- Copy MCP config for Claude Desktop

### Tech Stack

**Option A: Streamlit (Recommended for MVP)**
- Fast prototyping
- Built-in file uploaders
- Easy deployment (cloud-ready)
- Good for demos

**Option B: PyQt/Tkinter**
- Native desktop app
- Better performance
- Offline-first
- More complex

### Workflow Example

```
User Flow:
1. Launch docs-mcp GUI
2. Click "New Knowledge Base" → Name it "ProjectX"
3. Add sources:
   - Upload PDF (converted to MD)
   - Add GitHub repo URL (Repomix → MD)
   - Drag-drop Word docs (converted to MD)
4. Configure:
   - Chunking: Semantic
   - Embedding: OpenAI ada-002
   - Weights: 30% keyword, 70% semantic
5. Click "Build Index" → Progress bar
6. Test search: "authentication flow" → See results
7. Click "Start MCP Server" → Copy config to Claude Desktop
```

### Dependencies
- `md-mcp` (core library dependency)
- `streamlit` or `gradio` (GUI)
- `repomix` (via subprocess or Python wrapper)
- `pypdf` (PDF extraction)
- `python-docx` (Word docs)
- `openpyxl` (Excel)
- `trafilatura` (web scraping)
- `pandoc` (universal converter - optional)

### Distribution
- **Standalone app:** PyInstaller bundle (Windows/Mac/Linux)
- **Web app:** Deploy to Streamlit Cloud, Hugging Face Spaces
- **PyPI:** `pip install docs-mcp` (with GUI extras)

---

## 🔄 Integration Architecture

```
┌─────────────────────────────────────┐
│         docs-mcp (GUI App)          │
│  ┌───────────────────────────────┐  │
│  │  Document Ingestion           │  │
│  │  - PDF, DOCX, Repomix, etc.   │  │
│  │  - Convert to Markdown        │  │
│  └───────────┬───────────────────┘  │
│              │                       │
│              ▼                       │
│  ┌───────────────────────────────┐  │
│  │  md-mcp Library (imported)    │  │
│  │  - Create KB                  │  │
│  │  - Index markdown files       │  │
│  │  - Search & retrieve          │  │
│  └───────────┬───────────────────┘  │
└──────────────┼───────────────────────┘
               │
               ▼
    ┌──────────────────────┐
    │   MCP Server         │
    │   (exposed tools)    │
    └──────────┬───────────┘
               │
               ▼
    ┌──────────────────────┐
    │  Claude Desktop      │
    │  Cline, Cursor, etc. │
    └──────────────────────┘
```

---

## 📋 Feature Matrix

| Feature | md-mcp (Library) | docs-mcp (App) |
|---------|------------------|----------------|
| Knowledge base CRUD | ✅ | via md-mcp |
| Markdown chunking | ✅ | - |
| Semantic chunking | ✅ | - |
| Keyword search | ✅ | - |
| Semantic search | ✅ | - |
| Hybrid search | ✅ | - |
| Source attribution | ✅ | - |
| Incremental indexing | ✅ | - |
| Multi-KB support | ✅ | - |
| MCP server protocol | ✅ | - |
| GUI file picker | - | ✅ |
| PDF conversion | - | ✅ |
| Office doc conversion | - | ✅ |
| Repomix integration | - | ✅ |
| Web scraping | - | ✅ |
| Batch processing | - | ✅ |
| Config UI | - | ✅ |
| Search testing UI | - | ✅ |
| MCP server controls | - | ✅ |

---

## 🚀 Development Phases

### Phase 1: md-mcp Core (2-3 weeks)
- [ ] Project setup (Poetry, tests, CI)
- [ ] Knowledge base CRUD
- [ ] Keyword chunking + FTS index
- [ ] Semantic chunking + vector index
- [ ] Hybrid search implementation
- [ ] Source attribution
- [ ] Incremental indexing
- [ ] Unit tests (>80% coverage)

### Phase 2: MCP Protocol (1 week)
- [ ] Implement MCP server
- [ ] Define tools (search, list, rebuild, stats)
- [ ] Test with Claude Desktop
- [ ] Documentation for integration

### Phase 3: docs-mcp GUI (2 weeks)
- [ ] Streamlit app scaffold
- [ ] File picker + drag-drop
- [ ] PDF conversion
- [ ] Office doc conversion
- [ ] Repomix integration
- [ ] KB config UI
- [ ] Build/index workflow

### Phase 4: Polish & Release (1 week)
- [ ] Error handling
- [ ] Logging
- [ ] User docs + tutorials
- [ ] PyPI release (md-mcp)
- [ ] Package docs-mcp (PyInstaller or web)
- [ ] Demo video
- [ ] GitHub repo (separate repos for md-mcp and docs-mcp)

**Total: ~7-8 weeks to production**

---

## 📁 Project Structure

### md-mcp (Library)
```
md-mcp/
├── src/
│   └── md_mcp/
│       ├── __init__.py
│       ├── knowledge_base.py      # KB management
│       ├── chunking.py            # Chunking strategies
│       ├── indexing.py            # FTS + vector indexing
│       ├── search.py              # Hybrid search
│       ├── mcp_server.py          # MCP protocol
│       ├── config.py              # Configuration
│       └── utils.py
├── tests/
├── docs/
├── pyproject.toml
├── README.md
└── LICENSE
```

### docs-mcp (Application)
```
docs-mcp/
├── src/
│   └── docs_mcp/
│       ├── __init__.py
│       ├── app.py                 # Streamlit entry point
│       ├── converters/
│       │   ├── pdf.py
│       │   ├── office.py
│       │   ├── repomix.py
│       │   └── web.py
│       ├── ui/
│       │   ├── file_picker.py
│       │   ├── config_panel.py
│       │   └── search_test.py
│       └── utils.py
├── tests/
├── docs/
├── pyproject.toml
├── README.md
└── requirements.txt
```

---

## 🎓 Success Criteria

### md-mcp
- ✅ PyPI package installable in <1 minute
- ✅ Search latency <500ms for 10K chunks
- ✅ Incremental index update <5s for 100 changed files
- ✅ Works with Claude Desktop out-of-the-box
- ✅ 80%+ test coverage

### docs-mcp
- ✅ Convert 100+ page PDF in <30s
- ✅ Index 1000-file repo in <2 minutes
- ✅ GUI responsive (no freezing during processing)
- ✅ One-click MCP server setup
- ✅ Supports Windows/Mac/Linux

---

## 🤔 Open Questions

1. **Embedding model:** Default to local (sentence-transformers) or cloud (OpenAI)?
2. **Vector DB:** FAISS (simple, local) vs ChromaDB (feature-rich) vs Qdrant (scalable)?
3. **GUI framework:** Streamlit (web) vs PyQt (native)?
4. **Pandoc dependency:** Include for universal conversion or keep lean?
5. **Cloud sync:** Should md-mcp support remote storage (S3, GCS)?
6. **Multi-language:** Should we support non-English from day 1?

---

## 📝 Next Steps

1. **Review this spec** with Master Yang
2. **Make architectural decisions** (embedding model, vector DB, GUI framework)
3. **Create GitHub repos** (md-mcp, docs-mcp)
4. **Set up development environments**
5. **Start Phase 1: md-mcp core**

---

**Maintainer:** Master Yang  
**Repository:** (TBD)  
**Contact:** (TBD)
