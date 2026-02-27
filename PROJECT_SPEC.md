# Code Folders MCP: Project Specification

**Last Updated:** 2026-02-27 (Pivoted to code-folders-first)  
**Status:** MVP Development  
**Architecture:** Single Streamlit app using md-mcp

---

## 🎯 Vision (Revised)

Build a **code-folders-first MCP knowledge base** that:
1. Takes code folders as input
2. Uses Repomix to generate markdown per folder
3. Indexes with md-mcp (already live on PyPI)
4. Exposes via MCP for Claude Desktop

**Out of scope for MVP:** PDF, DOCX, web scraping. We'll add those later.

---

## 📦 Single Application: Code Folders MCP

### Core Responsibilities

#### 1. Folder Selection UI (Streamlit)
- Multi-select folder browser
- Display selected folders with remove/reorder
- Validate folder paths exist
- Support drag-drop (if Streamlit supports)

#### 2. Repomix Integration
- Run repomix as subprocess on each folder
- Generate `{folder-name}.md` per folder
- Show progress per folder (progress bar)
- Handle repomix errors gracefully
- Store generated .md files in workspace

#### 3. Knowledge Base Creation
- User provides KB name (e.g., "my-project")
- Create md-mcp knowledge base from generated .md files
- Index with hybrid search (keyword + semantic)
- Store KB in user's home directory (`~/.code-folders-mcp/`)

#### 4. MCP Server Management
- Start/stop MCP server via UI
- Display server status (running/stopped)
- Show MCP endpoint details
- Generate Claude Desktop config snippet

#### 5. Configuration Export
- Generate `claude_desktop_config.json` snippet
- Copy-to-clipboard button
- Show installation instructions
- Support multiple KBs in one config

#### 6. Search Testing (Nice-to-Have)
- In-app search UI to test KB
- Display results with source attribution
- Validate search quality before connecting to Claude

---

## 🎨 UI Mockup (Streamlit)

### Main Screen

```
╔══════════════════════════════════════════════════════════════════╗
║  Code Folders MCP - Turn Your Codebase into Claude Knowledge    ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  📁 Selected Folders (3)                                         ║
║  ┌────────────────────────────────────────────────────────────┐ ║
║  │ ✓ C:\code\my-project\backend          [Remove]             │ ║
║  │ ✓ C:\code\my-project\frontend         [Remove]             │ ║
║  │ ✓ C:\code\shared-utils                [Remove]             │ ║
║  └────────────────────────────────────────────────────────────┘ ║
║                                                                  ║
║  [➕ Add Folder]                                                 ║
║                                                                  ║
║  ────────────────────────────────────────────────────────────  ║
║                                                                  ║
║  📝 Knowledge Base Name                                          ║
║  ┌────────────────────────────────────────────────────────────┐ ║
║  │ my-project                                                  │ ║
║  └────────────────────────────────────────────────────────────┘ ║
║                                                                  ║
║  [🚀 Generate Knowledge Base]                                   ║
║                                                                  ║
║  ────────────────────────────────────────────────────────────  ║
║                                                                  ║
║  📊 Status                                                       ║
║  ┌────────────────────────────────────────────────────────────┐ ║
║  │ ✅ Repomix: backend.md generated (4.2 MB)                   │ ║
║  │ ✅ Repomix: frontend.md generated (3.1 MB)                  │ ║
║  │ ✅ Repomix: shared-utils.md generated (512 KB)              │ ║
║  │ ✅ KB indexed: 3 files, 12,450 chunks                       │ ║
║  └────────────────────────────────────────────────────────────┘ ║
║                                                                  ║
║  🔧 MCP Server                                                   ║
║  ┌────────────────────────────────────────────────────────────┐ ║
║  │ Status: Running on stdio                                    │ ║
║  │ [⏸ Stop Server]                                             │ ║
║  │                                                              │ ║
║  │ Claude Desktop Config:                                       │ ║
║  │ ┌──────────────────────────────────────────────────────┐   │ ║
║  │ │ {                                                      │   │ ║
║  │ │   "mcpServers": {                                      │   │ ║
║  │ │     "my-project": {                                    │   │ ║
║  │ │       "command": "python",                             │   │ ║
║  │ │       "args": ["-m", "md_mcp.server",                  │   │ ║
║  │ │                "--kb=my-project"]                      │   │ ║
║  │ │     }                                                   │   │ ║
║  │ │   }                                                     │   │ ║
║  │ │ }                                                       │   │ ║
║  │ └──────────────────────────────────────────────────────┘   │ ║
║  │ [📋 Copy to Clipboard]                                      │ ║
║  └────────────────────────────────────────────────────────────┘ ║
║                                                                  ║
║  🔍 Test Search (Optional)                                       ║
║  ┌────────────────────────────────────────────────────────────┐ ║
║  │ Query: how does authentication work?                       │ ║
║  │ [Search]                                                    │ ║
║  │                                                              │ ║
║  │ Results (3):                                                │ ║
║  │ 1. backend.md:234-256 (score: 0.89)                        │ ║
║  │    "The authentication flow uses JWT tokens..."            │ ║
║  │                                                              │ ║
║  │ 2. frontend.md:89-102 (score: 0.76)                        │ ║
║  │    "Login component sends credentials to /api/auth..."     │ ║
║  └────────────────────────────────────────────────────────────┘ ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## 🔄 Data Flow

### Step 1: User Adds Folders
```
User clicks "Add Folder"
    │
    ▼
File browser dialog
    │
    ▼
Selected folder added to list
    │
    ▼
Display in UI
```

### Step 2: Generate Knowledge Base
```
User clicks "Generate Knowledge Base"
    │
    ├──► Validate: KB name not empty
    ├──► Validate: At least one folder selected
    │
    ▼
For each folder:
    │
    ├──► Create temp dir: ~/.code-folders-mcp/temp/
    │
    ├──► Run: repomix --output {folder-name}.md --style markdown
    │     (Show progress bar)
    │
    ├──► Move {folder-name}.md to KB workspace
    │
    ▼
All folders processed
    │
    ▼
Create md-mcp KB:
    KnowledgeBase.create(
        name=user_kb_name,
        source_files=[...generated .md files]
    )
    │
    ▼
Index with md-mcp:
    kb.index()
    │
    ▼
Display stats:
    - Number of files indexed
    - Total chunks
    - KB size
```

### Step 3: Start MCP Server
```
User clicks "Start MCP Server"
    │
    ▼
md-mcp starts server:
    kb.start_mcp_server(transport="stdio")
    │
    ▼
Server status: Running
    │
    ▼
Generate Claude config snippet
    │
    ▼
Display in UI with copy button
```

### Step 4: Connect to Claude
```
User copies config snippet
    │
    ▼
Paste into:
    macOS: ~/Library/Application Support/Claude/claude_desktop_config.json
    Windows: %APPDATA%\Claude\claude_desktop_config.json
    Linux: ~/.config/Claude/claude_desktop_config.json
    │
    ▼
Restart Claude Desktop
    │
    ▼
Claude connects to MCP server
    │
    ▼
User can ask: "How does the authentication flow work?"
    │
    ▼
Claude uses search_knowledge() tool
    │
    ▼
Returns results from indexed code
```

---

## 🛠️ Technical Stack

### Core Dependencies
| Package | Version | Purpose |
|---------|---------|---------|
| streamlit | ^1.30 | Web UI framework |
| md-mcp | ^0.1.0 | Knowledge base + MCP server |
| repomix | latest (npm) | Code → Markdown conversion |

### Optional Dependencies
| Package | Purpose |
|---------|---------|
| watchdog | File watcher for auto-regen |
| pyperclip | Clipboard support for config |

---

## 📋 Feature Checklist

### MVP (Week 1: Feb 27 - Mar 5)
- [ ] **Streamlit UI Setup**
  - [ ] Folder selection widget
  - [ ] KB name input field
  - [ ] Generate button
  - [ ] Status display area
  
- [ ] **Repomix Integration**
  - [ ] Subprocess wrapper for repomix
  - [ ] Progress bar per folder
  - [ ] Error handling for repomix failures
  - [ ] Validate repomix is installed (npm global)
  
- [ ] **md-mcp Integration**
  - [ ] Create KB from .md files
  - [ ] Index with hybrid search
  - [ ] Store in ~/.code-folders-mcp/
  - [ ] Handle KB already exists (overwrite prompt)
  
- [ ] **MCP Server Controls**
  - [ ] Start server button
  - [ ] Stop server button
  - [ ] Display server status
  - [ ] Generate config snippet
  
- [ ] **Configuration Export**
  - [ ] Generate Claude Desktop config JSON
  - [ ] Copy to clipboard button
  - [ ] Display file path instructions
  
- [ ] **Testing**
  - [ ] Test with sample code folder
  - [ ] Verify Claude Desktop connection
  - [ ] Test search quality

### Nice-to-Have (Week 2: Mar 6-12)
- [ ] **Search Testing UI**
  - [ ] In-app search widget
  - [ ] Display results with scores
  - [ ] Source file links
  
- [ ] **Watch Mode**
  - [ ] Auto-detect file changes in folders
  - [ ] Auto-regenerate .md files
  - [ ] Auto-reindex KB
  
- [ ] **Multiple KBs**
  - [ ] List existing KBs
  - [ ] Switch between KBs
  - [ ] Delete KB
  
- [ ] **Statistics Dashboard**
  - [ ] KB size, chunk count
  - [ ] Files indexed
  - [ ] Last updated timestamp
  
- [ ] **Repomix Config**
  - [ ] Customize repomix options
  - [ ] Exclude patterns
  - [ ] Output format options

### Future (Post-MVP)
- [ ] **Document Support**
  - [ ] PDF → Markdown
  - [ ] DOCX → Markdown
  - [ ] Web scraping
  
- [ ] **Advanced Features**
  - [ ] Real-time collaboration
  - [ ] Cloud deployment (Streamlit Cloud)
  - [ ] Multi-user support
  - [ ] API endpoints

---

## 🧪 Testing Strategy

### Manual Testing
1. **Folder Selection**
   - Select single folder ✓
   - Select multiple folders ✓
   - Remove folder ✓
   - Invalid path handling ✓

2. **Repomix Execution**
   - Small folder (< 100 files) ✓
   - Large folder (> 1000 files) ✓
   - Repomix not installed ✓
   - Repomix fails (invalid path) ✓

3. **KB Creation**
   - First KB creation ✓
   - KB already exists ✓
   - Empty folder list ✓
   - Empty KB name ✓

4. **MCP Integration**
   - Start server ✓
   - Stop server ✓
   - Server already running ✓
   - Claude Desktop connection ✓

5. **Search Quality**
   - Code-specific queries ✓
   - Function/class name search ✓
   - Conceptual queries ✓
   - Edge cases (no results) ✓

### Automated Testing
- Unit tests for repomix wrapper
- Integration tests for md-mcp KB creation
- End-to-end test with sample folder

---

## 📦 Distribution Options

### Option A: pip install (Recommended)
```bash
pip install code-folders-mcp
code-folders-mcp  # Launches Streamlit app
```

**Pros:**
- Easy installation
- Standard Python workflow
- Works on all platforms

**Cons:**
- Requires Python environment
- Users need to install repomix separately

### Option B: Standalone Executable
```bash
# PyInstaller bundle
code-folders-mcp.exe  # Windows
./code-folders-mcp    # macOS/Linux
```

**Pros:**
- No Python required
- One-click launch

**Cons:**
- Large file size
- Complex bundling (Streamlit + md-mcp)

### Option C: Streamlit Cloud Deploy
```
https://code-folders-mcp.streamlit.app
```

**Pros:**
- Zero installation
- Web-based

**Cons:**
- Requires upload of code (privacy concern)
- Network dependency
- Not suitable for private codebases

**Decision:** Start with **Option A** (pip install), explore others later.

---

## 🔒 Security & Privacy

### Data Handling
- ✅ **Local-first:** All processing on user's machine
- ✅ **No upload:** Code never leaves local filesystem
- ✅ **No telemetry:** Zero data collection
- ✅ **User control:** User owns KB files

### Potential Risks
- ⚠️ Repomix might include sensitive files (mitigate: .gitignore respect)
- ⚠️ KB stored in plaintext (mitigate: document best practices)

---

## 📚 Documentation Plan

### User Documentation
1. **README.md** - Quick start guide
2. **Installation.md** - Detailed setup
3. **Usage.md** - Step-by-step walkthrough
4. **Troubleshooting.md** - Common issues

### Developer Documentation
1. **ARCHITECTURE.md** - System design
2. **DECISIONS.md** - Design choices
3. **CONTRIBUTING.md** - How to contribute
4. **API.md** - md-mcp integration details

---

## 🎯 Success Criteria

**MVP is successful if:**
- ✅ User can select 1+ code folders
- ✅ Repomix generates .md files
- ✅ md-mcp creates searchable KB
- ✅ MCP server starts successfully
- ✅ Claude Desktop can search the codebase
- ✅ Search results are relevant (>70% accuracy on test queries)

**Post-MVP goals:**
- 📈 50+ users testing the tool
- 📈 5+ GitHub stars on doc-mcp repo
- 📈 Positive feedback on search quality
- 📈 Feature requests for PDF/DOCX support

---

## 📞 Contact

**Project Owner:** Master Yang  
**AI Assistant:** Helpful Bob 🤖  
**Repository:** https://github.com/ly2xxx/doc-mcp  
**PyPI (md-mcp):** https://pypi.org/project/md-mcp/

---

**Let's build this MVP!** 🚀

Clear scope, proven tech, achievable timeline. Time to code.
