# Architecture Overview

## Two-Tier Design

### Layer 1: md-mcp (Core Library)
**What it does:** Pure Python library for markdown knowledge base management

**Key Components:**
```
┌─────────────────────────────────────────────────────────┐
│                     md-mcp Library                      │
├─────────────────────────────────────────────────────────┤
│  Knowledge Base Manager                                 │
│  ├─ Create/Load/Delete KBs                             │
│  ├─ Multi-namespace support                            │
│  └─ Configuration management                           │
├─────────────────────────────────────────────────────────┤
│  Chunking Engine                                        │
│  ├─ Keyword-based (header, paragraph, custom)          │
│  ├─ Semantic-based (embedding boundaries)              │
│  └─ Metadata preservation (file, line, headers)        │
├─────────────────────────────────────────────────────────┤
│  Indexing Layer                                         │
│  ├─ Keyword Index (SQLite FTS5)                        │
│  ├─ Vector Index (FAISS/ChromaDB/Qdrant)               │
│  └─ Incremental update (hash-based)                    │
├─────────────────────────────────────────────────────────┤
│  Search & Retrieval                                     │
│  ├─ Keyword search                                      │
│  ├─ Semantic search                                     │
│  ├─ Hybrid ranking (weighted combination)              │
│  └─ Source attribution                                 │
├─────────────────────────────────────────────────────────┤
│  MCP Protocol Server                                    │
│  ├─ Tools: search, list_sources, rebuild, stats        │
│  ├─ Resources: expose markdown files                   │
│  └─ Integration: Claude Desktop, Cline, Cursor         │
└─────────────────────────────────────────────────────────┘
```

### Layer 2: docs-mcp (GUI Application)
**What it does:** User-facing app for document ingestion and KB management

**Key Components:**
```
┌─────────────────────────────────────────────────────────┐
│                   docs-mcp Application                  │
├─────────────────────────────────────────────────────────┤
│  Document Ingestion Pipeline                            │
│  ├─ File Picker (drag-drop, browse)                    │
│  ├─ Format Detection                                    │
│  └─ Batch Queue Management                             │
├─────────────────────────────────────────────────────────┤
│  Format Converters                                      │
│  ├─ PDF → Markdown (pypdf)                             │
│  ├─ Office → Markdown (python-docx, openpyxl)          │
│  ├─ Web → Markdown (trafilatura)                       │
│  ├─ Code → Markdown (Repomix)                          │
│  └─ Generic (Pandoc fallback)                          │
├─────────────────────────────────────────────────────────┤
│  GUI Interface (Streamlit/PyQt)                         │
│  ├─ KB Configuration Panel                             │
│  ├─ Document Upload/Selection                          │
│  ├─ Progress Tracking                                   │
│  └─ Search Testing UI                                  │
├─────────────────────────────────────────────────────────┤
│  MCP Server Controls                                    │
│  ├─ Start/Stop Server                                   │
│  ├─ View Logs                                           │
│  └─ Export Config (for Claude Desktop)                 │
├─────────────────────────────────────────────────────────┤
│  md-mcp Integration (dependency)                        │
│  └─ Uses md-mcp for all KB operations                  │
└─────────────────────────────────────────────────────────┘
```

---

## Data Flow

### Document → Knowledge Base
```
┌──────────────┐
│ Source Docs  │ (PDF, DOCX, GitHub, Web, etc.)
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│ docs-mcp:        │
│ Format Converter │ (PDF→MD, Repomix→MD, etc.)
└──────┬───────────┘
       │
       ▼ (Markdown files)
┌──────────────────┐
│ md-mcp:          │
│ Chunking Engine  │ (Split into chunks with metadata)
└──────┬───────────┘
       │
       ▼
┌──────────────────────────────┐
│ md-mcp:                      │
│ Dual Indexing                │
│ ┌────────────┬─────────────┐ │
│ │ Keyword    │ Vector      │ │
│ │ Index      │ Index       │ │
│ │ (FTS5)     │ (Embeddings)│ │
│ └────────────┴─────────────┘ │
└──────────────┬───────────────┘
               │
               ▼
       ┌───────────────┐
       │ Knowledge Base│ (Ready for search)
       └───────────────┘
```

### Query → Results
```
┌─────────────┐
│ User Query  │ ("how to authenticate users")
└──────┬──────┘
       │
       ▼
┌────────────────────────┐
│ md-mcp:                │
│ Hybrid Search          │
│ ┌──────────────────┐   │
│ │ Keyword Search   │   │ → Results + Scores
│ │ Semantic Search  │   │ → Results + Scores
│ └──────────────────┘   │
│ Weighted Combination   │ (0.3 × keyword + 0.7 × semantic)
└──────┬─────────────────┘
       │
       ▼
┌──────────────────────┐
│ Ranked Results       │
│ ┌──────────────────┐ │
│ │ - Text chunk     │ │
│ │ - Score          │ │
│ │ - Source file    │ │
│ │ - Line range     │ │
│ │ - Metadata       │ │
│ └──────────────────┘ │
└──────────────────────┘
```

---

## MCP Integration Flow

```
┌──────────────────┐
│ User runs:       │
│ docs-mcp GUI     │
└────────┬─────────┘
         │
         ├─ Builds KB using md-mcp
         │
         ▼
┌─────────────────────┐
│ User clicks:        │
│ "Start MCP Server"  │
└────────┬────────────┘
         │
         ▼
┌───────────────────────────┐
│ md-mcp MCP Server starts  │
│ (listening on stdio/port) │
└────────┬──────────────────┘
         │
         ▼
┌────────────────────────────┐
│ User adds to:              │
│ Claude Desktop config.json │
│ {                          │
│   "mcpServers": {          │
│     "docs-kb": {           │
│       "command": "...",    │
│       "args": ["--kb=..."]│
│     }                      │
│   }                        │
│ }                          │
└────────┬───────────────────┘
         │
         ▼
┌──────────────────────┐
│ Claude Desktop       │
│ connects to MCP      │
│ server               │
└────────┬─────────────┘
         │
         ▼
┌────────────────────────────┐
│ Tools available in Claude: │
│ - search_knowledge()       │
│ - list_sources()           │
│ - rebuild_index()          │
│ - get_kb_stats()           │
└────────────────────────────┘
```

---

## Deployment Options

### Option A: Streamlit Web App
```
┌─────────────────────┐
│ docs-mcp            │
│ (Streamlit Cloud)   │
└──────────┬──────────┘
           │ HTTPS
           ▼
┌─────────────────────┐
│ User Browser        │
│ - Upload docs       │
│ - Build KB          │
│ - Download KB files │
└─────────────────────┘
           │
           ▼
┌──────────────────────┐
│ Local Machine        │
│ - Run md-mcp server  │
│ - Connect to Claude  │
└──────────────────────┘
```

### Option B: Desktop App (PyInstaller)
```
┌────────────────────────┐
│ docs-mcp.exe           │
│ (standalone bundle)    │
│ - GUI (PyQt)           │
│ - md-mcp (bundled)     │
│ - Converters (bundled) │
└──────────┬─────────────┘
           │
           ├─ Builds KB locally
           ├─ Starts MCP server
           │
           ▼
┌──────────────────────┐
│ Claude Desktop       │
│ (local MCP connect)  │
└──────────────────────┘
```

### Option C: Hybrid (Recommended)
```
┌─────────────────────────────────────┐
│ PyPI: pip install docs-mcp          │
│ - Includes md-mcp dependency        │
│ - CLI + GUI both available          │
└──────────────┬──────────────────────┘
               │
       ┌───────┴────────┐
       │                │
       ▼                ▼
┌──────────────┐ ┌──────────────┐
│ CLI Mode     │ │ GUI Mode     │
│ $ docs-mcp   │ │ $ docs-mcp   │
│   build      │ │   --gui      │
│   --source   │ │              │
│   ./docs     │ │ (Streamlit)  │
└──────────────┘ └──────────────┘
```

---

## Technology Stack

### md-mcp (Library)
| Component | Technology | Rationale |
|-----------|------------|-----------|
| Embedding | sentence-transformers | Local, fast, no API costs |
| Vector DB | FAISS | Simple, proven, minimal deps |
| Keyword Index | SQLite FTS5 | Built-in, zero config |
| MCP | official MCP SDK | Standard compliance |
| Config | YAML + Pydantic | Type-safe, readable |
| Testing | pytest | Industry standard |

### docs-mcp (Application)
| Component | Technology | Rationale |
|-----------|------------|-----------|
| GUI | Streamlit | Fast prototyping, web-ready |
| PDF | pypdf | Pure Python, no external deps |
| Office | python-docx, openpyxl | Official MS format support |
| Web | trafilatura | Best web extraction library |
| Code | Repomix (subprocess) | Already proven tool |
| Packaging | PyInstaller (optional) | Cross-platform binaries |

---

## Scalability Considerations

### Performance Targets
- **Index 10K markdown files:** <5 minutes
- **Search latency:** <500ms (cold), <100ms (warm)
- **Incremental update:** <5s for 100 changed files
- **Memory footprint:** <500MB for 1GB corpus

### Optimization Strategies
1. **Lazy loading:** Don't load entire KB into memory
2. **Batch processing:** Chunk and index in batches
3. **Caching:** LRU cache for frequent queries
4. **Parallel indexing:** Multi-threaded chunk processing
5. **Quantization:** Use smaller embedding models if needed

### Future Enhancements
- Distributed vector DB (Qdrant, Milvus)
- Cloud storage backends (S3, GCS)
- Horizontal scaling (multiple MCP servers)
- Real-time updates (file watcher)

---

## Security & Privacy

### Data Handling
- **Local-first:** All processing on user's machine by default
- **No telemetry:** Zero data sent to external services
- **API keys:** User-provided, stored locally (keyring)
- **Sandboxing:** No arbitrary code execution from documents

### Threat Model
- ✅ **Protect:** Private documents stay local
- ✅ **Protect:** No external API calls without consent
- ⚠️ **Risk:** Malicious PDFs (mitigated by pypdf sandboxing)
- ⚠️ **Risk:** Repomix executing untrusted code (user responsibility)

---

## Open Questions for Master Yang

1. **Vector DB:** FAISS (simple) vs ChromaDB (feature-rich)?
2. **Embedding:** Local-only or also support OpenAI/Cohere?
3. **GUI:** Streamlit (web) vs PyQt (native)?
4. **Scope:** MVP with basic converters, or full Pandoc integration?
5. **Distribution:** PyPI only or also standalone binaries?
6. **Naming:** Happy with md-mcp + docs-mcp or prefer alternatives?

---

**Ready for review!** 🚀
