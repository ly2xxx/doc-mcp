# Architecture: Code Folders MCP

**Last Updated:** 2026-02-27  
**Design Philosophy:** Simple, focused, ship fast

---

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        User's Machine                           │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │              Streamlit Web UI (localhost:8501)            │ │
│  │                                                           │ │
│  │  📁 Folder Selector                                       │ │
│  │  📝 KB Name Input                                         │ │
│  │  🚀 Generate Button                                       │ │
│  │  📊 Status Display                                        │ │
│  │  🔧 MCP Controls                                          │ │
│  └───────────────────┬───────────────────────────────────────┘ │
│                      │                                           │
│                      ▼                                           │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │              Repomix Runner (subprocess)                  │ │
│  │                                                           │ │
│  │  For each folder:                                         │ │
│  │    cd /path/to/folder                                     │ │
│  │    repomix --output {name}.md --style markdown            │ │
│  │                                                           │ │
│  │  Output: .md files in workspace                           │ │
│  └───────────────────┬───────────────────────────────────────┘ │
│                      │                                           │
│                      ▼                                           │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │              md-mcp Knowledge Base                        │ │
│  │              (PyPI: md-mcp)                               │ │
│  │                                                           │ │
│  │  ┌─────────────────────────────────────────────────────┐ │ │
│  │  │ Chunking Engine                                     │ │ │
│  │  │  - Split .md files into chunks                      │ │ │
│  │  │  - Preserve metadata (file, line, headers)          │ │ │
│  │  └─────────────────────────────────────────────────────┘ │ │
│  │                                                           │ │
│  │  ┌─────────────────────────────────────────────────────┐ │ │
│  │  │ Hybrid Indexing                                     │ │ │
│  │  │  ├─ Keyword Index (SQLite FTS5)                     │ │ │
│  │  │  └─ Vector Index (FAISS)                            │ │ │
│  │  └─────────────────────────────────────────────────────┘ │ │
│  │                                                           │ │
│  │  ┌─────────────────────────────────────────────────────┐ │ │
│  │  │ MCP Server                                          │ │ │
│  │  │  - Exposes search_knowledge() tool                  │ │ │
│  │  │  - Runs on stdio                                    │ │ │
│  │  └─────────────────────────────────────────────────────┘ │ │
│  └───────────────────┬───────────────────────────────────────┘ │
│                      │                                           │
│                      ▼                                           │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │              Claude Desktop                               │ │
│  │                                                           │ │
│  │  Connects to MCP server via stdio                         │ │
│  │  Uses search_knowledge() to query code                    │ │
│  └───────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component Details

### 1. Streamlit UI

**Responsibilities:**
- Folder selection (multi-select with browse dialog)
- KB name input with validation
- Trigger repomix processing
- Display progress and status
- MCP server start/stop controls
- Config snippet generation

**Key Files:**
```python
app/
├── main.py              # Main Streamlit app
├── components/
│   ├── folder_selector.py    # Folder selection widget
│   ├── kb_generator.py       # KB creation workflow
│   ├── mcp_controls.py       # Server controls
│   └── search_tester.py      # Optional search UI
└── utils/
    ├── repomix_runner.py     # Subprocess wrapper
    └── config_generator.py   # Claude config generator
```

**State Management:**
```python
# Streamlit session state
st.session_state.selected_folders = []
st.session_state.kb_name = ""
st.session_state.kb_status = "idle"  # idle | processing | ready
st.session_state.mcp_server_running = False
```

---

### 2. Repomix Integration

**Execution Flow:**
```python
def run_repomix(folder_path: str, output_name: str) -> Path:
    """
    Run repomix on a folder and return path to generated .md file.
    
    Args:
        folder_path: Absolute path to code folder
        output_name: Name for output file (e.g., "backend")
        
    Returns:
        Path to generated .md file
        
    Raises:
        RepomixError: If repomix fails
    """
    output_file = workspace_dir / f"{output_name}.md"
    
    # Check repomix is installed
    if not shutil.which("repomix"):
        raise RepomixError("repomix not found. Install with: npm install -g repomix")
    
    # Run repomix
    result = subprocess.run(
        ["repomix", "--output", str(output_file), "--style", "markdown"],
        cwd=folder_path,
        capture_output=True,
        text=True,
        timeout=300  # 5 min timeout
    )
    
    if result.returncode != 0:
        raise RepomixError(f"repomix failed: {result.stderr}")
    
    return output_file
```

**Progress Tracking:**
```python
# Streamlit progress bar
progress_bar = st.progress(0)
status_text = st.empty()

for i, folder in enumerate(selected_folders):
    status_text.text(f"Processing {folder.name}...")
    
    md_file = run_repomix(folder, folder.name)
    
    progress = (i + 1) / len(selected_folders)
    progress_bar.progress(progress)

status_text.text("✅ All folders processed!")
```

---

### 3. md-mcp Knowledge Base

**KB Creation:**
```python
from md_mcp import KnowledgeBase

# Create KB from generated .md files
kb = KnowledgeBase.create(
    name=user_kb_name,
    source_files=[
        workspace_dir / "backend.md",
        workspace_dir / "frontend.md",
        workspace_dir / "utils.md"
    ],
    config={
        "chunking": {
            "strategy": "semantic",  # or "keyword"
            "chunk_size": 512,
            "overlap": 50
        },
        "search": {
            "keyword_weight": 0.3,
            "semantic_weight": 0.7
        }
    }
)

# Index the KB
kb.index(show_progress=True)

# Save to disk
kb.save(path=Path.home() / ".code-folders-mcp" / user_kb_name)
```

**KB Storage Structure:**
```
~/.code-folders-mcp/
├── my-project/                # KB directory
│   ├── config.json            # KB configuration
│   ├── sources/               # Original .md files
│   │   ├── backend.md
│   │   ├── frontend.md
│   │   └── utils.md
│   ├── index/                 # Indexed data
│   │   ├── keyword.db         # SQLite FTS5
│   │   ├── vectors.faiss      # FAISS index
│   │   └── metadata.json      # Chunk metadata
│   └── stats.json             # KB statistics
```

---

### 4. MCP Server

**Server Startup:**
```python
# md-mcp provides built-in MCP server
kb.start_mcp_server(
    transport="stdio",  # Claude Desktop uses stdio
    port=None           # Not used for stdio
)

# Server exposes tools:
# - search_knowledge(query, top_k, weights)
# - list_sources()
# - get_kb_stats()
```

**Claude Desktop Config:**
```json
{
  "mcpServers": {
    "my-project": {
      "command": "python",
      "args": [
        "-m", "md_mcp.server",
        "--kb=my-project",
        "--kb-path=/Users/yang/.code-folders-mcp/my-project"
      ]
    }
  }
}
```

**MCP Tool Example:**
```python
# When Claude calls search_knowledge()
{
  "tool": "search_knowledge",
  "arguments": {
    "query": "how does authentication work",
    "top_k": 5,
    "weights": {"keyword": 0.3, "semantic": 0.7}
  }
}

# md-mcp returns:
{
  "results": [
    {
      "text": "The authentication flow uses JWT tokens...",
      "score": 0.89,
      "source": "backend.md",
      "line_range": [234, 256],
      "metadata": {
        "file": "backend.md",
        "headers": ["Backend", "Authentication", "JWT Flow"]
      }
    },
    ...
  ]
}
```

---

## Data Flow Diagrams

### Flow 1: Generate Knowledge Base

```
User selects folders (A, B, C)
         │
         ▼
User enters KB name "my-project"
         │
         ▼
User clicks "Generate KB"
         │
         ├──► Validate inputs
         │
         ▼
For folder A:
  ├─► cd A
  ├─► repomix --output A.md
  ├─► Progress: 33%
  │
For folder B:
  ├─► cd B
  ├─► repomix --output B.md
  ├─► Progress: 66%
  │
For folder C:
  ├─► cd C
  ├─► repomix --output C.md
  ├─► Progress: 100%
  │
  ▼
All .md files generated
  │
  ▼
md-mcp.KnowledgeBase.create(
  name="my-project",
  sources=[A.md, B.md, C.md]
)
  │
  ▼
Chunk files
  │
  ▼
Build keyword index (FTS5)
Build vector index (FAISS)
  │
  ▼
Save to ~/.code-folders-mcp/my-project/
  │
  ▼
Display: "✅ KB ready! 12,450 chunks indexed"
```

### Flow 2: Start MCP Server

```
User clicks "Start MCP Server"
         │
         ▼
Load KB from ~/.code-folders-mcp/my-project/
         │
         ▼
md-mcp.start_mcp_server(transport="stdio")
         │
         ├─► Server listens on stdio
         │
         ▼
Display:
  - Status: Running
  - Config snippet
  - Copy button
         │
         ▼
User copies config
         │
         ▼
User pastes into Claude Desktop config
         │
         ▼
User restarts Claude
         │
         ▼
Claude connects to MCP server
         │
         ▼
search_knowledge() tool available in Claude
```

### Flow 3: Claude Searches Code

```
User asks Claude: "How does auth work?"
         │
         ▼
Claude decides to use search_knowledge() tool
         │
         ▼
Claude calls MCP server:
  search_knowledge(
    query="authentication flow implementation",
    top_k=5
  )
         │
         ▼
md-mcp processes query:
  ├─► Keyword search (FTS5)
  ├─► Semantic search (FAISS)
  ├─► Hybrid ranking
  │
  ▼
Return top 5 results with source attribution
         │
         ▼
Claude receives results:
  [
    {text: "...", source: "backend.md:234-256", score: 0.89},
    ...
  ]
         │
         ▼
Claude synthesizes answer using retrieved context
         │
         ▼
Claude replies: "The authentication flow works as follows:
  1. User submits credentials (backend.md:234)
  2. JWT token is generated (backend.md:240)
  3. Token stored in localStorage (frontend.md:89)
  ..."
```

---

## Technology Stack

| Layer | Technology | Reason |
|-------|------------|--------|
| **UI** | Streamlit | Fast prototyping, web-based, Python-native |
| **Subprocess** | repomix (Node.js) | Best code→markdown tool, proven |
| **KB Engine** | md-mcp (PyPI) | Already published, battle-tested |
| **Keyword Search** | SQLite FTS5 | Built-in, zero config, fast |
| **Vector Search** | FAISS | Fast, local, no dependencies |
| **Embeddings** | sentence-transformers | Local model, no API costs |
| **MCP** | md-mcp built-in | Standard MCP SDK |
| **Storage** | Filesystem (JSON + DB) | Simple, portable |

**No external services required.** Everything runs locally.

---

## Performance Considerations

### Expected Performance
- **Repomix:** ~30s for 1000-file folder
- **Indexing:** ~5s for 1MB markdown file
- **Search latency:** <100ms (warm cache)

### Optimization Strategies
1. **Parallel repomix:** Run multiple folders concurrently
2. **Incremental indexing:** Only reindex changed files
3. **Lazy loading:** Don't load entire KB into memory
4. **Cache embeddings:** Reuse embeddings for unchanged chunks

### Scalability Limits
- **Max folders:** ~10 (limited by UI space, not performance)
- **Max KB size:** ~1GB markdown (FAISS handles this fine)
- **Max chunks:** ~100K (FTS5 + FAISS both scale to this)

If users exceed these limits, suggest splitting into multiple KBs.

---

## Error Handling

### Repomix Failures
```python
try:
    run_repomix(folder, name)
except RepomixNotFoundError:
    st.error("Repomix not installed. Run: npm install -g repomix")
except RepomixTimeoutError:
    st.error(f"Repomix timed out processing {folder}. Try smaller folder.")
except RepomixError as e:
    st.error(f"Repomix failed: {e}")
```

### KB Creation Failures
```python
try:
    kb = KnowledgeBase.create(...)
except KBAlreadyExistsError:
    if st.confirm("KB exists. Overwrite?"):
        kb = KnowledgeBase.create(..., overwrite=True)
except KBEmptySourcesError:
    st.error("No .md files generated. Check repomix output.")
```

### MCP Server Failures
```python
try:
    kb.start_mcp_server()
except ServerAlreadyRunningError:
    st.warning("Server already running on this KB.")
except ServerPortInUseError:
    st.error("Port in use. Stop other MCP servers first.")
```

---

## Security & Privacy

### Data Security
- ✅ All processing local
- ✅ No network calls
- ✅ No telemetry
- ✅ User owns all files

### Potential Risks
- ⚠️ Repomix might include `.env` files (mitigate: respect `.gitignore`)
- ⚠️ KB stored in plaintext (document: keep `~/.code-folders-mcp/` secure)

### Best Practices (User Documentation)
1. Review generated .md files before indexing sensitive codebases
2. Use `.gitignore` to exclude secrets from repomix
3. Don't commit KB files to version control
4. Secure `~/.code-folders-mcp/` directory

---

## Deployment Options

### Option A: pip install (MVP)
```bash
pip install code-folders-mcp
code-folders-mcp  # Launches Streamlit app
```

### Option B: Docker (Future)
```bash
docker run -p 8501:8501 \
  -v ~/.code-folders-mcp:/data \
  code-folders-mcp
```

### Option C: Streamlit Cloud (Future)
```
https://code-folders-mcp.streamlit.app
```

**Start with Option A.** It's simplest and keeps data local.

---

## Open Questions

1. **Repomix config:** Should we expose repomix options (exclude patterns, etc.) in UI?
2. **Watch mode:** Auto-regenerate on file changes? (Use `watchdog`?)
3. **Multi-KB:** Support multiple KBs in one UI session?
4. **Config profiles:** Save folder selections as templates?

---

**Architecture is solid.** Simple, focused, achievable. Let's build! 🚀
