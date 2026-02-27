"""
MCP Server Controls Component

Start/stop MCP server and generate Claude Desktop config.
"""

import streamlit as st


def render_mcp_controls():
    """Render the MCP server controls UI."""
    
    # Only show if KB is ready
    if st.session_state.kb_status != "ready":
        st.info("🔒 Generate a knowledge base first to enable MCP server controls")
        return
    
    st.markdown("**MCP Server Status:**")
    
    # Server status
    if st.session_state.mcp_server_running:
        st.success("🟢 Server running")
    else:
        st.warning("⚪ Server stopped")
    
    # Start/Stop buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(
            "▶️ Start Server",
            disabled=st.session_state.mcp_server_running,
            use_container_width=True
        ):
            # Placeholder - will implement in MCP Server Controls task
            st.info("🔧 Server start logic will be implemented in MCP Server Controls task")
            # st.session_state.mcp_server_running = True
            # st.rerun()
    
    with col2:
        if st.button(
            "⏸️ Stop Server",
            disabled=not st.session_state.mcp_server_running,
            use_container_width=True
        ):
            # Placeholder - will implement in MCP Server Controls task
            st.info("🔧 Server stop logic will be implemented in MCP Server Controls task")
            # st.session_state.mcp_server_running = False
            # st.rerun()
    
    st.divider()
    
    # Configuration snippet (placeholder)
    if st.session_state.kb_name:
        st.markdown("**Claude Desktop Config:**")
        
        # This will be implemented in Configuration Export task
        config_snippet = f"""{{
  "mcpServers": {{
    "{st.session_state.kb_name}": {{
      "command": "python",
      "args": [
        "-m", "md_mcp.server",
        "--kb={st.session_state.kb_name}"
      ]
    }}
  }}
}}"""
        
        st.code(config_snippet, language="json")
        
        # Copy button placeholder
        if st.button("📋 Copy to Clipboard", disabled=True):
            st.info("🔧 Clipboard functionality will be implemented in Configuration Export task")
        
        # Instructions placeholder
        with st.expander("📖 Setup Instructions"):
            st.markdown("""
            **How to connect to Claude Desktop:**
            
            1. Copy the config snippet above
            2. Open your Claude Desktop config file:
               - **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
               - **Windows:** `%APPDATA%\\Claude\\claude_desktop_config.json`
               - **Linux:** `~/.config/Claude/claude_desktop_config.json`
            3. Paste the config into the `mcpServers` section
            4. Restart Claude Desktop
            5. Ask Claude to search your code!
            
            *(Detailed instructions will be added in Configuration Export task)*
            """)
