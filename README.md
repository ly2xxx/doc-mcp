# docs-mcp + md-mcp: Project Specification

**Status:** 🎨 Design Phase  
**Created:** 2026-02-18  
**Owner:** Master Yang

---

## 📁 What's Here

This directory contains the complete specification for the two-tier markdown knowledge base system:

| Document | Purpose |
|----------|---------|
| **PROJECT_SPEC.md** | Complete feature breakdown, responsibilities, and roadmap |
| **ARCHITECTURE.md** | System design, data flows, and technology stack |
| **DECISIONS.md** | Architectural decisions matrix with recommendations |
| **README.md** | This file - quick navigation guide |

---

## 🎯 Quick Summary

### The Vision
Build a production-ready MCP knowledge base system that:
1. Converts any document (PDF, Office, Web, Code) → Markdown
2. Indexes with hybrid search (keyword + semantic)
3. Exposes via MCP protocol for Claude Desktop integration

### The Architecture
Two clean layers:

**md-mcp (PyPI Library):**
- Pure Python markdown knowledge base engine
- Chunking, indexing, hybrid search
- MCP server protocol implementation
- Reusable by other projects

**docs-mcp (GUI Application):**
- User-friendly document ingestion
- Multi-format conversion (PDF, DOCX, Repomix, etc.)
- Configuration UI
- Uses md-mcp as core dependency

---

## 🚀 Getting Started

### 1. Review the Spec
```bash
# Read in order:
1. PROJECT_SPEC.md    # Overall scope and features
2. ARCHITECTURE.md    # How it works technically
3. DECISIONS.md       # Key choices to make
```

### 2. Make Decisions
Review `DECISIONS.md` and decide on:
- Vector database (FAISS vs ChromaDB)
- Embedding strategy (local vs OpenAI)
- GUI framework (Streamlit vs PyQt)
- Converter scope (core vs full Pandoc)
- Project naming confirmation

### 3. Kick Off Development
Once decisions are made:
```bash
# Create repos
mkdir md-mcp
mkdir docs-mcp

# Initialize with Poetry
cd md-mcp && poetry init
cd ../docs-mcp && poetry init

# Set up tests
pytest --cov

# Start coding!
```

---

## 📊 Feature Distribution

### md-mcp (Library) - Core Engine
- ✅ Knowledge base CRUD
- ✅ Markdown chunking (keyword + semantic)
- ✅ Dual indexing (FTS + vectors)
- ✅ Hybrid search with ranking
- ✅ Source attribution
- ✅ Incremental updates
- ✅ Multi-KB support
- ✅ MCP protocol server

### docs-mcp (App) - User Interface
- ✅ GUI file picker (drag-drop)
- ✅ PDF → Markdown conversion
- ✅ Office docs → Markdown
- ✅ Repomix integration (code repos)
- ✅ Web scraping → Markdown
- ✅ Batch processing queue
- ✅ KB configuration UI
- ✅ Search testing interface
- ✅ MCP server controls

---

## 🗓️ Timeline Estimate

| Phase | Duration | Deliverable |
|-------|----------|-------------|
| **Phase 1:** md-mcp core | 2-3 weeks | Working library with tests |
| **Phase 2:** MCP protocol | 1 week | Claude Desktop integration |
| **Phase 3:** docs-mcp GUI | 2 weeks | Complete app with converters |
| **Phase 4:** Polish & release | 1 week | PyPI packages + docs |
| **Total** | **6-7 weeks** | Production-ready v1.0 |

---

## 🔧 Tech Stack Summary

### md-mcp
- Python 3.10+
- sentence-transformers (embeddings)
- FAISS (vector search)
- SQLite FTS5 (keyword search)
- MCP SDK (protocol)
- Pydantic (config validation)

### docs-mcp
- Streamlit (GUI)
- pypdf (PDF extraction)
- python-docx (Word docs)
- openpyxl (Excel)
- trafilatura (web scraping)
- repomix (code repos)
- md-mcp (core dependency)

---

## 📝 Open Questions

From `DECISIONS.md`, awaiting Master Yang's input:

1. **Vector DB:** FAISS (simple) or ChromaDB (feature-rich)?
2. **Embedding:** Local-only or support OpenAI API?
3. **GUI:** Streamlit (web) or PyQt (native)?
4. **Converters:** Core set or full Pandoc integration?
5. **Distribution:** PyPI only or also standalone binaries?
6. **Naming:** Confirm md-mcp + docs-mcp or alternative?

---

## 🎬 Next Steps

**Immediate:**
1. ✅ Spec reviewed by Master Yang
2. ⏳ Architectural decisions finalized
3. ⏳ GitHub repos created
4. ⏳ Development environment set up

**Week 1:**
- Start md-mcp core (knowledge base + chunking)
- Write initial unit tests
- Set up CI pipeline

**Week 2-3:**
- Complete md-mcp indexing + search
- Implement MCP protocol
- Test with Claude Desktop

**Week 4-5:**
- Build docs-mcp GUI
- Integrate converters
- End-to-end testing

**Week 6:**
- Documentation
- Polish UX
- Release v1.0

---

## 📞 Contact

**Project Owner:** Master Yang  
**AI Assistant:** Helpful Bob 🤖  
**Location:** `C:\code\docs-mcp\`

---

**Ready to build!** 🚀

Review the specs, make decisions, and let's ship this. The architecture is solid, the plan is clear, and the timeline is realistic.
