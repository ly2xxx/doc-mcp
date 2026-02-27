# Architecture Decisions

**Last Updated:** 2026-02-27  
**Status:** Most decisions settled after pivot to code-folders-first

---

## ✅ Decisions Made (Settled)

### 1. Scope: Code Folders First (MVP)

**Decision:** Build code-folders-MCP first, defer PDF/DOCX/web scraping.

**Rationale:**
- ✅ md-mcp is already live on PyPI - we have the core
- ✅ Repomix is proven for code → markdown
- ✅ Code search is the #1 developer use case
- ✅ Smaller scope = ship faster
- ✅ Can add document support later (proven architecture)

**Status:** ✅ **SETTLED** - Code folders only for v0.1

---

### 2. GUI Framework: Streamlit

**Decision:** Use Streamlit for MVP UI.

**Rationale:**
| Pro | Con |
|-----|-----|
| ✅ Fast prototyping (< 100 lines for full UI) | ⚠️ Web-based (not native) |
| ✅ Python-native (no JS/HTML/CSS) | ⚠️ Limited offline support |
| ✅ Built-in widgets (file picker, buttons, etc.) | ⚠️ Not as polished as native apps |
| ✅ Easy deployment (Streamlit Cloud option) | |
| ✅ Good for data/ML tools | |

**Alternatives considered:**
- PyQt: More polished, but steeper learning curve
- Gradio: Good for ML demos, but less flexible for general apps
- CLI-only: Too basic for user-friendly experience

**Status:** ✅ **SETTLED** - Streamlit for MVP, consider PyQt for v2.0

---

### 3. Code → Markdown: Repomix

**Decision:** Use Repomix (subprocess) for code consolidation.

**Rationale:**
- ✅ Already proven tool (Master Yang uses it)
- ✅ Handles all file types (Python, JS, Rust, etc.)
- ✅ Respects `.gitignore`
- ✅ Generates clean markdown with file structure
- ✅ No reinventing the wheel

**Alternatives considered:**
- Tree + cat: Too manual, no formatting
- Custom parser: Unnecessary complexity
- Pandoc: Overkill for code files

**Status:** ✅ **SETTLED** - Repomix is the right tool

---

### 4. Knowledge Base: md-mcp (PyPI)

**Decision:** Use md-mcp library as the core KB engine.

**Rationale:**
- ✅ Already published on PyPI
- ✅ Proven chunking + indexing
- ✅ Built-in MCP server
- ✅ Hybrid search (keyword + semantic)
- ✅ Maintained by same team

**Status:** ✅ **SETTLED** - md-mcp is the foundation

---

### 5. Vector Database: FAISS (md-mcp default)

**Decision:** Use md-mcp's default (FAISS).

**Rationale:**
- ✅ md-mcp already uses FAISS
- ✅ Fast, local, no external dependencies
- ✅ Proven for <100K chunks (our use case)
- ✅ Simple API
- ✅ No need to change md-mcp internals

**Alternatives:**
- ChromaDB: Feature-rich, but heavier
- Qdrant: Production-grade, but overkill for local use
- Pinecone/Weaviate: Cloud-only, violates local-first principle

**Status:** ✅ **SETTLED** - Stick with FAISS

---

### 6. Embeddings: Local (sentence-transformers)

**Decision:** Use local embeddings via sentence-transformers.

**Rationale:**
- ✅ md-mcp already uses `all-MiniLM-L6-v2`
- ✅ No API costs
- ✅ No network dependency
- ✅ Privacy-preserving (code stays local)
- ✅ Fast inference on CPU

**Alternatives:**
- OpenAI embeddings: Costs money, requires API key, not private
- Cohere: Same issues as OpenAI

**Status:** ✅ **SETTLED** - Local embeddings only for MVP

---

### 7. Keyword Search: SQLite FTS5 (md-mcp default)

**Decision:** Use md-mcp's built-in FTS5 index.

**Rationale:**
- ✅ SQLite is built into Python
- ✅ FTS5 is fast and proven
- ✅ Zero config
- ✅ md-mcp already implements it

**Status:** ✅ **SETTLED** - FTS5 is perfect

---

### 8. MCP Transport: stdio

**Decision:** Use stdio transport for MCP (not HTTP).

**Rationale:**
- ✅ Claude Desktop expects stdio
- ✅ Simpler than HTTP (no port management)
- ✅ md-mcp supports stdio natively

**Status:** ✅ **SETTLED** - stdio for Claude Desktop integration

---

### 9. Storage Location: ~/.code-folders-mcp/

**Decision:** Store KBs in `~/.code-folders-mcp/{kb-name}/`.

**Rationale:**
- ✅ Standard user-local directory
- ✅ Portable across sessions
- ✅ Easy to backup
- ✅ Hidden by default (starts with `.`)

**Alternatives:**
- Project-local (.code-mcp/ in each project): Duplicates data
- /tmp/: Not persistent
- Custom user-specified: More complex UX

**Status:** ✅ **SETTLED** - `~/.code-folders-mcp/`

---

### 10. Distribution: pip install

**Decision:** Distribute via PyPI as `code-folders-mcp`.

**Rationale:**
- ✅ Standard Python packaging
- ✅ Easy installation (`pip install code-folders-mcp`)
- ✅ Dependency management via Poetry
- ✅ Can add standalone binaries later

**Status:** ✅ **SETTLED** - PyPI first, binaries later

---

## ⏳ Open Questions (To Decide)

### 1. Watch Mode (Auto-Regenerate)

**Question:** Should we auto-detect code changes and regenerate .md files?

**Options:**
| Option | Pros | Cons |
|--------|------|------|
| **A: No watch mode (MVP)** | ✅ Simpler, fewer deps | ⚠️ Manual regeneration |
| **B: Optional watch mode** | ✅ Better UX, fresher index | ⚠️ Complexity, resource usage |
| **C: Watch mode only** | ✅ Always fresh | ⚠️ Can't disable for large repos |

**Recommendation:** **Option A** for MVP, add **Option B** in v0.2.

**Decision:** ⏳ **PENDING** (lean towards Option A for MVP)

---

### 2. Multi-KB Management

**Question:** Should users manage multiple KBs in one UI session?

**Options:**
| Option | Pros | Cons |
|--------|------|------|
| **A: Single KB per session** | ✅ Simpler UI | ⚠️ Need to restart for other KBs |
| **B: KB switcher in UI** | ✅ Better UX | ⚠️ More state management |
| **C: Multiple tabs** | ✅ Parallel work | ⚠️ UI complexity |

**Recommendation:** **Option A** for MVP, add **Option B** if users request it.

**Decision:** ⏳ **PENDING** (lean towards Option A for MVP)

---

### 3. Repomix Configuration Exposure

**Question:** Should we let users configure repomix options (exclude patterns, etc.)?

**Options:**
| Option | Pros | Cons |
|--------|------|------|
| **A: Use repomix defaults** | ✅ Zero config | ⚠️ Less control |
| **B: Basic options (exclude)** | ✅ Useful for sensitive files | ⚠️ More UI complexity |
| **C: Full repomix config** | ✅ Maximum flexibility | ⚠️ Overwhelming for users |

**Recommendation:** **Option A** for MVP, add **Option B** if needed.

**Note:** Repomix already respects `.gitignore`, which covers 90% of use cases.

**Decision:** ⏳ **PENDING** (lean towards Option A for MVP)

---

### 4. Search Testing UI

**Question:** Should we include in-app search testing?

**Options:**
| Option | Pros | Cons |
|--------|------|------|
| **A: No search UI** | ✅ Simpler scope | ⚠️ Can't test before Claude |
| **B: Basic search widget** | ✅ Validate search quality | ⚠️ Extra development |
| **C: Full search dashboard** | ✅ Rich testing | ⚠️ Scope creep |

**Recommendation:** **Option B** - A simple search box is valuable for debugging.

**Decision:** ⏳ **PENDING** (lean towards Option B - it's easy to add)

---

### 5. Deployment Target

**Question:** Where should users run this?

**Options:**
| Option | Target | Pros | Cons |
|--------|--------|------|------|
| **A: Local only (pip)** | Developer machines | ✅ Privacy, speed | ⚠️ Requires Python setup |
| **B: Streamlit Cloud** | Web browser | ✅ Zero install | ⚠️ Upload code (privacy!) |
| **C: Docker** | Anywhere | ✅ Portable | ⚠️ Heavier setup |
| **D: Standalone binary** | Non-developers | ✅ One-click | ⚠️ Large file size |

**Recommendation:** Start with **Option A**, add others later.

**Decision:** ✅ **SETTLED** - Local pip install for MVP

---

### 6. Project Naming

**Question:** Confirm package name: `code-folders-mcp`?

**Alternatives:**
- `codebase-mcp`
- `repo-mcp`
- `source-mcp`
- `dev-mcp`

**Recommendation:** `code-folders-mcp` is descriptive and clear.

**Decision:** ⏳ **PENDING** - Need Master Yang's final approval

---

### 7. Configuration Persistence

**Question:** Should we save folder selections for reuse?

**Options:**
| Option | Pros | Cons |
|--------|------|------|
| **A: No persistence** | ✅ Stateless, simple | ⚠️ Re-enter folders each time |
| **B: Save to config file** | ✅ Reusable "profiles" | ⚠️ More code |
| **C: Browser session only** | ✅ Temporary persistence | ⚠️ Lost on refresh |

**Recommendation:** **Option A** for MVP, add **Option B** if requested.

**Decision:** ⏳ **PENDING** (lean towards Option A for MVP)

---

## 📊 Decision Summary

| Decision | Status | Choice |
|----------|--------|--------|
| 1. Scope | ✅ Settled | Code folders only (MVP) |
| 2. GUI | ✅ Settled | Streamlit |
| 3. Code→MD | ✅ Settled | Repomix |
| 4. KB Engine | ✅ Settled | md-mcp |
| 5. Vector DB | ✅ Settled | FAISS |
| 6. Embeddings | ✅ Settled | Local (sentence-transformers) |
| 7. Keyword Search | ✅ Settled | SQLite FTS5 |
| 8. MCP Transport | ✅ Settled | stdio |
| 9. Storage | ✅ Settled | ~/.code-folders-mcp/ |
| 10. Distribution | ✅ Settled | pip install |
| 11. Watch Mode | ⏳ Pending | Lean: No (MVP) |
| 12. Multi-KB | ⏳ Pending | Lean: No (MVP) |
| 13. Repomix Config | ⏳ Pending | Lean: Defaults only (MVP) |
| 14. Search UI | ⏳ Pending | Lean: Yes (easy to add) |
| 15. Package Name | ⏳ Pending | Proposed: code-folders-mcp |
| 16. Config Persistence | ⏳ Pending | Lean: No (MVP) |

**Progress:** 10/16 settled (62%)

**MVP-blocking decisions:** All settled! ✅

**Nice-to-have decisions:** Can be deferred to post-MVP.

---

## 🎯 Next Steps

1. ✅ Finalize package name with Master Yang
2. ✅ Confirm MVP scope excludes watch mode, multi-KB, config persistence
3. ⏳ Build Streamlit UI (folder selector + repomix runner)
4. ⏳ Integrate md-mcp KB creation
5. ⏳ Add simple search testing UI
6. ⏳ Test end-to-end with Claude Desktop
7. ⏳ Ship v0.1.0 to PyPI

---

**Decisions are mostly settled!** Ready to start coding. 🚀
