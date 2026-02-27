"""
Code Folders MCP - Main Streamlit Application

Converts code folders into MCP knowledge base for Claude Desktop.
"""

import streamlit as st
from pathlib import Path
import sys

# Add app directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from components.folder_selector import render_folder_selector
from components.kb_generator import render_kb_generator
from components.mcp_controls import render_mcp_controls
from components.search_tester import render_search_tester


def init_session_state():
    """Initialize Streamlit session state variables."""
    if "selected_folders" not in st.session_state:
        st.session_state.selected_folders = []
    
    if "kb_name" not in st.session_state:
        st.session_state.kb_name = ""
    
    if "kb_status" not in st.session_state:
        st.session_state.kb_status = "idle"  # idle | processing | ready
    
    if "kb_path" not in st.session_state:
        st.session_state.kb_path = None
    
    if "mcp_server_running" not in st.session_state:
        st.session_state.mcp_server_running = False
    
    if "generation_results" not in st.session_state:
        st.session_state.generation_results = []


def main():
    """Main application entry point."""
    # Page config
    st.set_page_config(
        page_title="Code Folders MCP",
        page_icon="📁",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    init_session_state()
    
    # Header
    st.title("📁 Code Folders MCP")
    st.markdown(
        "Turn your codebase into Claude Desktop knowledge in 3 steps: "
        "**Select folders** → **Generate KB** → **Connect to Claude**"
    )
    st.divider()
    
    # Main content in columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Step 1: Folder Selection
        st.header("📂 Step 1: Select Code Folders")
        render_folder_selector()
        
        st.divider()
        
        # Step 2: KB Generation
        st.header("🚀 Step 2: Generate Knowledge Base")
        render_kb_generator()
        
        st.divider()
        
        # Step 3: MCP Server
        st.header("🔧 Step 3: Connect to Claude Desktop")
        render_mcp_controls()
    
    with col2:
        # Sidebar: Status & Testing
        st.header("📊 Status")
        
        # Display current state
        status_text = {
            "idle": "⚪ Idle - No KB created yet",
            "processing": "🟡 Processing - Generating KB...",
            "ready": "🟢 Ready - KB available for search"
        }
        st.info(status_text[st.session_state.kb_status])
        
        # Stats
        if st.session_state.kb_status == "ready" and st.session_state.kb_path:
            st.metric("Selected Folders", len(st.session_state.selected_folders))
            st.metric("KB Name", st.session_state.kb_name or "N/A")
        
        st.divider()
        
        # Optional: Search Testing
        if st.session_state.kb_status == "ready":
            st.header("🔍 Test Search")
            render_search_tester()
    
    # Footer
    st.divider()
    st.caption(
        "💡 **Tip:** After generating your KB and starting the MCP server, "
        "copy the config snippet and paste it into your Claude Desktop config file. "
        "Then restart Claude."
    )
    st.caption("Built with ❤️ using [md-mcp](https://pypi.org/project/md-mcp/) | "
               "[Documentation](https://github.com/ly2xxx/doc-mcp)")


if __name__ == "__main__":
    main()
