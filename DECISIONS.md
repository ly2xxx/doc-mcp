# Architectural Decisions

**Purpose:** Track key technical decisions with rationale

---

## 🎯 Critical Decisions Needed

### 1. Vector Database Choice

| Option | Pros | Cons | Recommendation |
|--------|------|------|----------------|
| **FAISS** | • Fastest search<br>• Minimal dependencies<br>• Battle-tested by Facebook<br>• Works offline | • No built-in persistence (need manual save/load)<br>• Less feature-rich | ✅ **Phase 1 MVP** |
| **ChromaDB** | • Easy API<br>• Built-in persistence<br>• Metadata filtering<br>• Cloud-ready | • Heavier dependency<br>• Slower than FAISS | ⭐ **Phase 2 upgrade** |
| **Qdrant** | • Production-grade<br>• Horizontal scaling<br>• Advanced filtering | • Overkill for local use<br>• Requires server | 🔮 **Future (if cloud needed)** |

**Decision:** Start with FAISS, design abstraction layer for easy swap to ChromaDB later

---

### 2. Embedding Model Strategy

| Option | Pros | Cons | Recommendation |
|--------|------|------|----------------|
| **Local (sentence-transformers)** | • Free<br>• Fast<br>• Private<br>• Works offline | • Slightly lower quality<br>• 300MB model download | ✅ **Default** |
| **OpenAI (text-embedding-ada-002)** | • Best quality<br>• No local storage | • Costs $0.0001/1K tokens<br>• Requires API key<br>• Privacy concern | 🔧 **Optional upgrade** |
| **Cohere** | • Good quality<br>• Free tier available | • Still requires API<br>• Less popular | ⚠️ **Consider for v2** |

**Decision:** Default to `all-MiniLM-L6-v2` (local), allow user to configure OpenAI as override

**Config example:**
```yaml
embedding:
  provider: local  # or openai, cohere
  model: sentence-transformers/all-MiniLM-L6-v2
  # If provider=openai:
  # model: text-embedding-ada-002
  # api_key: ${OPENAI_API_KEY}
```

---

### 3. GUI Framework

| Option | Pros | Cons | Use Case |
|--------|------|------|----------|
| **Streamlit** | • Fast dev (days not weeks)<br>• Web-ready (deploy anywhere)<br>• Good for demos<br>• Built-in widgets | • Web-only (not native app)<br>• Slower than native<br>• Requires Python runtime | ✅ **MVP & web deployment** |
| **Gradio** | • Similar to Streamlit<br>• Hugging Face integration | • Less flexible<br>• Smaller community | ⚠️ Alternative to Streamlit |
| **PyQt** | • Native desktop<br>• Best performance<br>• Professional look | • Steep learning curve<br>• 2-3x dev time<br>• Platform-specific quirks | 🔮 **v2 if native app needed** |

**Decision:** Streamlit for MVP, evaluate PyQt for v2 if users request native app

**Hybrid approach:**
```python
# docs-mcp supports both
$ docs-mcp --gui          # Launch Streamlit
$ docs-mcp build --source ./docs  # CLI mode
```

---

### 4. Document Conversion Strategy

| Format | Library | Backup Option | Notes |
|--------|---------|---------------|-------|
| **PDF** | `pypdf` | `pdfplumber` | pypdf is pure Python (easier install) |
| **DOCX** | `python-docx` | `mammoth` | python-docx is official MS library |
| **XLSX** | `openpyxl` | `pandas` | openpyxl for structure, pandas for data |
| **Web** | `trafilatura` | `beautifulsoup4` | trafilatura is best for article extraction |
| **Code** | `repomix` (subprocess) | Custom parser | Repomix already proven |
| **Universal** | `pandoc` (optional) | - | 50MB dependency, but handles 40+ formats |

**Decision:** 
- Core converters (PDF, DOCX, Web, Repomix) built-in
- Pandoc as optional dependency for power users: `pip install docs-mcp[pandoc]`

---

### 5. MCP Server Deployment

| Mode | When to Use | How It Works |
|------|-------------|--------------|
| **Stdio** | Claude Desktop, Cline | MCP server reads stdin, writes stdout |
| **HTTP** | Remote access, web clients | MCP over HTTP (port 8080) |
| **Both** | Maximum compatibility | Detect mode from environment |

**Decision:** Support both, detect automatically:
```python
# In md-mcp
if sys.stdin.isatty():
    # Running interactively, use HTTP
    server.run_http(port=8080)
else:
    # Piped input, use stdio
    server.run_stdio()
```

**Claude Desktop config:**
```json
{
  "mcpServers": {
    "my-docs": {
      "command": "python",
      "args": ["-m", "md_mcp.server", "--kb", "my-project"]
    }
  }
}
```

---

### 6. Chunking Strategy Default

| Strategy | Best For | Performance | Accuracy |
|----------|----------|-------------|----------|
| **Header-based** | Technical docs with clear structure | Fast | Good |
| **Paragraph-based** | Prose, articles | Fast | Medium |
| **Semantic** | Mixed content | Slower | Best |
| **Hybrid** | Maximum coverage | Slowest | Best |

**Decision:** Default to semantic chunking, allow override:
```yaml
chunking:
  strategy: semantic  # or header, paragraph, hybrid
  max_chunk_size: 512  # tokens
  overlap: 50  # tokens
```

---

### 7. Project Naming

| Aspect | Current | Alternative | Decision |
|--------|---------|-------------|----------|
| **Library** | md-mcp | markdown-knowledge, mdkb | **md-mcp** ✅ (clear, concise) |
| **App** | docs-mcp | kb-builder, doc-indexer | **docs-mcp** ✅ (consistent naming) |
| **PyPI** | md-mcp, docs-mcp | Same | ✅ Match repo names |

**Rationale:** 
- "mcp" signals MCP protocol support
- "md" = markdown (core format)
- "docs" = multi-format documents (broader scope)

---

### 8. Testing Strategy

| Layer | Framework | Coverage Target | Priority |
|-------|-----------|-----------------|----------|
| **Unit tests** | pytest | 80%+ | High |
| **Integration tests** | pytest + fixtures | Key workflows | High |
| **MCP protocol tests** | MCP test harness | All tools | High |
| **GUI tests** | Streamlit test framework | Basic flows | Medium |
| **Performance tests** | pytest-benchmark | Latency, throughput | Medium |

**Decision:** Unit + integration mandatory before v1.0, GUI tests nice-to-have

---

### 9. Versioning & Release

| Aspect | Strategy |
|--------|----------|
| **Version scheme** | Semantic: 0.1.0 → 1.0.0 |
| **md-mcp releases** | Independent of docs-mcp |
| **Breaking changes** | Major version bump (1.x → 2.x) |
| **Deprecation** | 1 minor version warning before removal |

**Release checklist:**
- [ ] All tests pass
- [ ] Docs updated
- [ ] CHANGELOG.md entry
- [ ] PyPI upload
- [ ] GitHub release + tag
- [ ] Demo video updated

---

### 10. License

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| **MIT** | Most permissive, widely adopted | No patent grant | ✅ **Recommended** |
| **Apache 2.0** | Patent grant, enterprise-friendly | Slightly more complex | Alternative |
| **GPL** | Strong copyleft | Can't use in proprietary projects | ❌ Too restrictive |

**Decision:** MIT for both projects (maximize adoption)

---

## 📋 Configuration Recommendations

### md-mcp default config (YAML)
```yaml
knowledge_base:
  name: my-kb
  source_path: ./docs
  output_path: ./kb-data

embedding:
  provider: local
  model: sentence-transformers/all-MiniLM-L6-v2
  device: cpu  # or cuda

chunking:
  strategy: semantic
  max_chunk_size: 512
  overlap: 50
  preserve_metadata: true

indexing:
  vector_db: faiss
  keyword_index: sqlite_fts5
  incremental: true

search:
  keyword_weight: 0.3
  semantic_weight: 0.7
  top_k: 5

mcp_server:
  mode: auto  # auto, stdio, http
  port: 8080  # for HTTP mode
```

### docs-mcp default config (YAML)
```yaml
converters:
  pdf:
    enabled: true
    extract_images: false
  docx:
    enabled: true
    preserve_formatting: true
  xlsx:
    enabled: true
    convert_tables: true
  web:
    enabled: true
    timeout: 30
  repomix:
    enabled: true
    include_patterns: ["*.py", "*.js", "*.md"]
    exclude_patterns: ["node_modules", ".git"]

ui:
  framework: streamlit
  theme: dark
  max_upload_size_mb: 100

batch:
  max_concurrent: 4
  progress_updates: true
```

---

## 🚦 Decision Status

| Decision | Status | Owner | Date |
|----------|--------|-------|------|
| Vector DB (FAISS) | ⏳ Pending review | Master Yang | 2026-02-18 |
| Embedding (local default) | ⏳ Pending review | Master Yang | 2026-02-18 |
| GUI (Streamlit) | ⏳ Pending review | Master Yang | 2026-02-18 |
| Converters (core + optional) | ⏳ Pending review | Master Yang | 2026-02-18 |
| MCP server (stdio + HTTP) | ⏳ Pending review | Master Yang | 2026-02-18 |
| Chunking (semantic default) | ⏳ Pending review | Master Yang | 2026-02-18 |
| Naming (md-mcp, docs-mcp) | ⏳ Pending review | Master Yang | 2026-02-18 |
| License (MIT) | ⏳ Pending review | Master Yang | 2026-02-18 |

---

## 🎬 Next Actions

**For Master Yang to review:**
1. Approve/modify vector DB choice
2. Approve/modify embedding strategy
3. Approve/modify GUI framework
4. Approve/modify converter scope
5. Green-light project naming
6. Confirm license

**Once decided:**
1. Create GitHub repos (md-mcp, docs-mcp)
2. Set up development environment
3. Initialize projects with Poetry
4. Write first unit tests (TDD approach)
5. Start Phase 1 implementation

---

**Status:** Awaiting Master Yang's architectural decisions ⏳
