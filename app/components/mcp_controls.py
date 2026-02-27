"""
MCP Server Controls Component

Generate MCP server commands and Claude Desktop config.
"""

import streamlit as st
from pathlib import Path
import sys

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.mcp_config import (
    get_mcp_server_command,
    get_claude_desktop_config_json,
    get_claude_desktop_config_path,
    get_setup_instructions
)


def render_mcp_controls():
    """Render the MCP server controls UI."""
    
    # Only show if KB is ready
    if st.session_state.kb_status != "ready":
        st.info("🔒 Generate a knowledge base first to enable MCP server controls")
        return
    
    if not st.session_state.kb_path or not st.session_state.kb_name:
        st.error("❌ KB path or name not set")
        return
    
    kb_path = Path(st.session_state.kb_path)
    kb_name = st.session_state.kb_name
    
    # Get MCP server command
    server_command = get_mcp_server_command(kb_name, kb_path)
    config_json = get_claude_desktop_config_json(kb_name, kb_path)
    config_path = get_claude_desktop_config_path()
    
    st.markdown("**🚀 MCP Server Command**")
    st.info("The MCP server must run in a separate terminal (keep it open)")
    
    st.code(server_command, language="bash")
    
    # Copy command button
    if st.button("📋 Copy Command", key="copy_command", use_container_width=True):
        try:
            import pyperclip
            pyperclip.copy(server_command)
            st.success("✅ Command copied to clipboard!")
        except ImportError:
            st.warning("⚠️ Install pyperclip for clipboard support: pip install pyperclip")
            st.info(f"Manual copy: {server_command}")
    
    st.divider()
    
    # Configuration snippet
    st.markdown("**⚙️ Claude Desktop Config**")
    st.caption(f"Add this to: `{config_path}`")
    
    st.code(config_json, language="json")
    
    # Copy config button
    if st.button("📋 Copy Config", key="copy_config", use_container_width=True):
        try:
            import pyperclip
            pyperclip.copy(config_json)
            st.success("✅ Config copied to clipboard!")
        except ImportError:
            st.warning("⚠️ Install pyperclip for clipboard support: pip install pyperclip")
    
    st.divider()
    
    # Detailed instructions
    with st.expander("📖 Complete Setup Instructions", expanded=False):
        instructions = get_setup_instructions(kb_name, kb_path)
        st.markdown(instructions)
