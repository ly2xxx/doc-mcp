# 📋 Decision Checklist for Master Yang

**Purpose:** Quick approval/modification of key architectural decisions  
**Action Required:** Review and mark ✅/❌/🔧 for each decision

---

## Instructions

- ✅ = Approved as-is
- ❌ = Reject, need alternative
- 🔧 = Modify (add notes)

---

## 1. Vector Database

**Recommendation:** FAISS (Phase 1) → ChromaDB (Phase 2)

**Rationale:**
- FAISS fastest, simplest for MVP
- Easy to swap later via abstraction layer
- ChromaDB better for production features

**Decision:** [ ] ✅  [ ] ❌  [ ] 🔧

**Notes:**
```


```

---

## 2. Embedding Model

**Recommendation:** Local `all-MiniLM-L6-v2` (default) + optional OpenAI

**Rationale:**
- Free, private, works offline
- OpenAI as premium option for power users
- User can configure via YAML

**Decision:** [ ] ✅  [ ] ❌  [ ] 🔧

**Notes:**
```


```

---

## 3. GUI Framework

**Recommendation:** Streamlit (MVP) + CLI mode

**Rationale:**
- 5x faster development than PyQt
- Web-ready (deploy to cloud)
- Good for demos and testing
- Can add PyQt in v2 if needed

**Decision:** [ ] ✅  [ ] ❌  [ ] 🔧

**Notes:**
```


```

---

## 4. Document Converters

**Recommendation:** Core set (PDF, DOCX, XLSX, Web, Repomix) + optional Pandoc

**Rationale:**
- Covers 90% of use cases
- Pure Python dependencies (easier install)
- Pandoc adds 40+ formats but 50MB overhead
- Power users: `pip install docs-mcp[pandoc]`

**Decision:** [ ] ✅  [ ] ❌  [ ] 🔧

**Notes:**
```


```

---

## 5. MCP Server Modes

**Recommendation:** Support both stdio (Claude Desktop) + HTTP (remote)

**Rationale:**
- Stdio for local Claude Desktop integration
- HTTP for remote access and web clients
- Auto-detect from environment

**Decision:** [ ] ✅  [ ] ❌  [ ] 🔧

**Notes:**
```


```

---

## 6. Default Chunking Strategy

**Recommendation:** Semantic chunking (embedding-based boundaries)

**Rationale:**
- Best accuracy for mixed content
- User can override to header/paragraph for speed
- Modern approach, future-proof

**Decision:** [ ] ✅  [ ] ❌  [ ] 🔧

**Notes:**
```


```

---

## 7. Project Naming

**Recommendation:** 
- Library: `md-mcp`
- App: `docs-mcp`

**Rationale:**
- Clear, concise
- "mcp" signals MCP protocol support
- "md" = markdown core
- "docs" = broader multi-format scope

**Decision:** [ ] ✅  [ ] ❌  [ ] 🔧

**Alternative names:**
```


```

---

## 8. License

**Recommendation:** MIT

**Rationale:**
- Most permissive
- Widely adopted in Python ecosystem
- Encourages adoption

**Decision:** [ ] ✅  [ ] ❌  [ ] 🔧

**Notes:**
```


```

---

## 9. Testing Strategy

**Recommendation:** 
- Unit tests (pytest, 80%+ coverage) - mandatory
- Integration tests (key workflows) - mandatory
- MCP protocol tests - mandatory
- GUI tests - nice-to-have

**Rationale:**
- Core library needs high test coverage
- GUI can rely more on manual testing for MVP

**Decision:** [ ] ✅  [ ] ❌  [ ] 🔧

**Notes:**
```


```

---

## 10. Distribution Strategy

**Recommendation:**
- PyPI packages (both projects)
- Streamlit Cloud deployment (optional)
- PyInstaller binaries (Phase 2)

**Rationale:**
- PyPI for developers
- Streamlit Cloud for non-technical users
- Binaries if native app demand is high

**Decision:** [ ] ✅  [ ] ❌  [ ] 🔧

**Notes:**
```


```

---

## Additional Decisions/Modifications

**Any other preferences or requirements?**

```




```

---

## Timeline Confirmation

**Estimated:** 6-7 weeks to v1.0 production release

**Breakdown:**
- Week 1-3: md-mcp core + MCP protocol
- Week 4-5: docs-mcp GUI + converters
- Week 6: Polish + documentation + release

**Acceptable?** [ ] Yes  [ ] No - modify:

```


```

---

## Scope Adjustments

**MVP Feature Set (can cut for faster release):**
- ✅ PDF converter
- ✅ DOCX converter
- ✅ Repomix integration
- ✅ Web scraping
- ⚠️ XLSX converter (use Pandoc instead?)
- ⚠️ GUI search testing (CLI only for MVP?)
- ⚠️ Incremental indexing (full rebuild for MVP?)

**Suggestions:**
```


```

---

## Sign-Off

**Reviewed by:** ________________  
**Date:** ________________  
**Status:** [ ] Approved to proceed  [ ] Needs revisions  

**Next Action:**
- [ ] Create GitHub repos
- [ ] Set up development environment
- [ ] Start Phase 1 implementation

---

## Notes Section

**Free-form feedback, ideas, or concerns:**

```








```

---

**Ready to build!** 🚀

Return this checklist with decisions marked, and we'll create the repos and start coding.
