# Decision Checklist

**Last Updated:** 2026-02-27  
**Purpose:** Quick reference for remaining decisions after code-folders-first pivot

---

## ✅ MVP-Blocking Decisions (All Settled!)

| # | Decision | Status | Choice |
|---|----------|--------|--------|
| 1 | Project scope | ✅ **DONE** | Code folders only |
| 2 | GUI framework | ✅ **DONE** | Streamlit |
| 3 | Code→Markdown tool | ✅ **DONE** | Repomix (subprocess) |
| 4 | KB engine | ✅ **DONE** | md-mcp (PyPI) |
| 5 | Vector database | ✅ **DONE** | FAISS (md-mcp default) |
| 6 | Embeddings | ✅ **DONE** | Local (sentence-transformers) |
| 7 | Keyword search | ✅ **DONE** | SQLite FTS5 |
| 8 | MCP transport | ✅ **DONE** | stdio |
| 9 | KB storage location | ✅ **DONE** | ~/.code-folders-mcp/ |
| 10 | Distribution | ✅ **DONE** | pip install (PyPI) |

**🎉 No MVP-blocking decisions remain!** Ready to code.

---

## ⏳ Nice-to-Have Decisions (Can Defer)

### 1. Watch Mode (Auto-Regenerate)

**Question:** Auto-detect code changes and regenerate .md files?

- **Option A:** No watch mode (simpler MVP) ← **RECOMMENDED**
- **Option B:** Optional watch mode (better UX)
- **Option C:** Always-on watch mode (resource-heavy)

**Recommendation:** Skip for MVP (Option A), add in v0.2 if users request it.

**Priority:** ⭐⭐⬜⬜⬜ (Low - nice to have)

---

### 2. Multi-KB Management

**Question:** Support multiple KBs in one UI session?

- **Option A:** Single KB per session (simpler) ← **RECOMMENDED**
- **Option B:** KB switcher dropdown (better for multi-project devs)
- **Option C:** Multiple tabs (complex UI)

**Recommendation:** Single KB for MVP (Option A), add switcher if needed.

**Priority:** ⭐⭐⬜⬜⬜ (Low - can restart app)

---

### 3. Repomix Configuration Exposure

**Question:** Let users customize repomix options (exclude patterns, etc.)?

- **Option A:** Use repomix defaults (zero config) ← **RECOMMENDED**
- **Option B:** Expose basic options (exclude patterns)
- **Option C:** Full repomix config (overwhelming)

**Note:** Repomix already respects `.gitignore`, covering 90% of use cases.

**Recommendation:** Defaults only for MVP (Option A).

**Priority:** ⭐⬜⬜⬜⬜ (Very Low - .gitignore handles most cases)

---

### 4. Search Testing UI

**Question:** Include in-app search widget to test KB quality?

- **Option A:** No search UI (simpler MVP)
- **Option B:** Basic search box + results display ← **RECOMMENDED**
- **Option C:** Full search dashboard (scope creep)

**Recommendation:** Add basic search box (Option B) - it's easy and useful for debugging.

**Priority:** ⭐⭐⭐⬜⬜ (Medium - valuable for QA)

**Decision:** **Add to MVP** - Streamlit makes this trivial:
```python
query = st.text_input("Test search:")
if query:
    results = kb.search(query, top_k=5)
    for r in results:
        st.write(f"**{r.source}** (score: {r.score:.2f})")
        st.write(r.text)
```

---

### 5. Package Naming

**Question:** Confirm package name: `code-folders-mcp`?

**Alternatives:**
- `code-folders-mcp` ← **CURRENT**
- `codebase-mcp`
- `repo-mcp`
- `source-mcp`

**Recommendation:** `code-folders-mcp` is clear and descriptive.

**Priority:** ⭐⭐⭐⭐⭐ (High - need to decide before publishing)

**Action Required:** Master Yang's final approval ✅

---

### 6. Configuration Persistence

**Question:** Save folder selections for reuse?

- **Option A:** No persistence (stateless MVP) ← **RECOMMENDED**
- **Option B:** Save to config file (reusable "profiles")
- **Option C:** Browser session state only

**Recommendation:** No persistence for MVP (Option A). Users can re-select if needed.

**Priority:** ⭐⬜⬜⬜⬜ (Very Low - marginal UX improvement)

---

### 7. Error Handling Strategy

**Question:** How to handle repomix failures?

**Options:**
- **A:** Show error, let user retry ← **RECOMMENDED**
- **B:** Auto-retry with backoff
- **C:** Skip failed folders, continue with others

**Recommendation:** Option A for MVP - clear error messages, user decides.

**Priority:** ⭐⭐⭐⭐⬜ (High - must handle gracefully)

**Decision:** **Add to MVP** - Streamlit error handling:
```python
try:
    run_repomix(folder)
except RepomixError as e:
    st.error(f"❌ {folder}: {e}")
    st.info("💡 Check that repomix is installed: npm install -g repomix")
```

---

## 📋 MVP Checklist (Technical)

### Week 1: Core Functionality

- [ ] **Streamlit UI**
  - [ ] Folder selection widget (multi-select)
  - [ ] KB name input with validation
  - [ ] "Generate KB" button
  - [ ] Progress bar for repomix
  - [ ] Status display area
  
- [ ] **Repomix Integration**
  - [ ] Subprocess wrapper
  - [ ] Error handling (repomix not found, timeout, failures)
  - [ ] Progress tracking per folder
  - [ ] Output file management
  
- [ ] **md-mcp Integration**
  - [ ] KB creation from .md files
  - [ ] Index with hybrid search
  - [ ] Save to ~/.code-folders-mcp/
  - [ ] Handle KB already exists
  
- [ ] **MCP Server**
  - [ ] Start/stop buttons
  - [ ] Server status display
  - [ ] Config snippet generation
  - [ ] Copy to clipboard

- [ ] **Search Testing UI** (NEW - added to MVP)
  - [ ] Simple search input
  - [ ] Results display with scores
  - [ ] Source file links

### Week 2: Polish & Ship

- [ ] **Error Handling**
  - [ ] Repomix failures
  - [ ] KB creation errors
  - [ ] Server start failures
  
- [ ] **Documentation**
  - [ ] Installation guide
  - [ ] Usage tutorial
  - [ ] Claude Desktop setup
  - [ ] Troubleshooting
  
- [ ] **Testing**
  - [ ] Test with sample code folder
  - [ ] Test Claude Desktop integration
  - [ ] Test search quality
  
- [ ] **Packaging**
  - [ ] pyproject.toml setup
  - [ ] README for PyPI
  - [ ] Publish to PyPI
  
- [ ] **Release**
  - [ ] GitHub release
  - [ ] Announcement (Discord, Twitter)

---

## 🎯 Post-MVP Backlog

### v0.2 Features (If Requested)
- [ ] Watch mode (auto-regenerate on changes)
- [ ] Multi-KB management (switcher dropdown)
- [ ] Configuration persistence (save folder selections)
- [ ] Repomix config exposure (exclude patterns)
- [ ] KB statistics dashboard
- [ ] Multiple KBs in Claude config

### v1.0 Features (Original Vision)
- [ ] PDF → Markdown conversion
- [ ] DOCX → Markdown conversion
- [ ] Web scraping → Markdown
- [ ] Generic Pandoc fallback
- [ ] Document upload UI
- [ ] Batch processing queue

---

## 📊 Decision Status Summary

| Status | Count | Decisions |
|--------|-------|-----------|
| ✅ Settled | 10 | All MVP-blocking decisions |
| ⏳ Pending (Low Priority) | 5 | Watch mode, Multi-KB, Repomix config, Persistence, Config profiles |
| 🚀 Add to MVP | 2 | Search testing UI, Error handling |
| 🎯 Post-MVP | 1 | Package naming (needs approval) |

**Total:** 18 decisions tracked

**MVP Readiness:** ✅ **100%** (all blocking decisions settled)

---

## ✅ Action Items for Master Yang

1. **Approve package name:** `code-folders-mcp` (or suggest alternative)
2. **Confirm MVP scope:** Code folders only, no watch mode, no multi-KB
3. **Greenlight development:** Start building Streamlit UI

---

## 🚀 Ready to Code!

All MVP-blocking decisions are settled. The remaining open questions are either:
- Low priority (can defer to v0.2)
- Easy additions (search UI, error handling)
- Awaiting Master Yang's approval (package name)

**No technical blockers.** Let's ship the MVP! 🎯
