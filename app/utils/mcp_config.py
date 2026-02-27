"""
MCP Configuration Generator

Generates Claude Desktop config and server start commands.
"""

from pathlib import Path
from typing import Dict
import json
import sys


def get_mcp_server_command(kb_name: str, kb_path: Path) -> str:
    """
    Generate the command to start the MCP server.
    
    Args:
        kb_name: Name of the knowledge base
        kb_path: Path to the KB directory
        
    Returns:
        Command string to start the server
    """
    # Get sources directory where markdown files are stored
    sources_dir = kb_path / "sources"
    
    # Python executable
    python_exe = sys.executable
    
    # Command to start md-mcp server
    # Uses md-mcp's CLI: md-mcp <folder-path> --name <server-name>
    command = f'md-mcp "{sources_dir}" --name "{kb_name}"'
    
    return command


def get_claude_desktop_config(kb_name: str, kb_path: Path) -> Dict:
    """
    Generate Claude Desktop configuration for the MCP server.
    
    Args:
        kb_name: Name of the knowledge base
        kb_path: Path to the KB directory
        
    Returns:
        Dict with Claude Desktop config
    """
    sources_dir = kb_path / "sources"
    
    # Get the md-mcp executable path
    # This will be something like: C:\\Users\\...\\Python\\Scripts\\md-mcp.exe
    # or the python -m md_mcp equivalent
    
    config = {
        "mcpServers": {
            kb_name: {
                "command": "md-mcp",
                "args": [str(sources_dir), "--name", kb_name]
            }
        }
    }
    
    return config


def get_claude_desktop_config_json(kb_name: str, kb_path: Path) -> str:
    """
    Get Claude Desktop config as formatted JSON string.
    
    Args:
        kb_name: Name of the knowledge base
        kb_path: Path to the KB directory
        
    Returns:
        Formatted JSON string
    """
    config = get_claude_desktop_config(kb_name, kb_path)
    return json.dumps(config, indent=2)


def get_claude_desktop_config_path() -> Path:
    """
    Get the path to Claude Desktop config file based on OS.
    
    Returns:
        Path to claude_desktop_config.json
    """
    import platform
    
    system = platform.system()
    
    if system == "Darwin":  # macOS
        return Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    elif system == "Windows":
        return Path.home() / "AppData" / "Roaming" / "Claude" / "claude_desktop_config.json"
    else:  # Linux
        return Path.home() / ".config" / "Claude" / "claude_desktop_config.json"


def get_setup_instructions(kb_name: str, kb_path: Path) -> str:
    """
    Get complete setup instructions for the user.
    
    Args:
        kb_name: Name of the knowledge base
        kb_path: Path to the KB directory
        
    Returns:
        Markdown-formatted instructions
    """
    config_path = get_claude_desktop_config_path()
    server_command = get_mcp_server_command(kb_name, kb_path)
    config_json = get_claude_desktop_config_json(kb_name, kb_path)
    
    instructions = f"""
### 🚀 How to Connect to Claude Desktop

**Step 1: Start the MCP Server**

Open a terminal and run:

```bash
{server_command}
```

Keep this terminal open (the server must stay running).

---

**Step 2: Configure Claude Desktop**

1. Open your Claude Desktop config file:
   - **Path:** `{config_path}`
   - If the file doesn't exist, create it

2. Add this configuration (or merge with existing):

```json
{config_json}
```

3. Save the file

---

**Step 3: Restart Claude Desktop**

1. Quit Claude Desktop completely
2. Start Claude Desktop again
3. The MCP server should now be connected

---

**Step 4: Test It!**

Ask Claude:
- "Search my code for authentication"
- "How does the login flow work?"
- "Show me error handling patterns"

Claude will use the `{kb_name}` MCP tool to search your codebase!

---

### 🐛 Troubleshooting

**Problem: "md-mcp: command not found"**
- Install md-mcp globally: `pip install md-mcp`
- Or use full path: `python -m md_mcp.cli "{kb_path / 'sources'}" --name "{kb_name}"`

**Problem: Claude doesn't show the tool**
- Verify the config file path is correct
- Restart Claude Desktop completely
- Check the terminal where MCP server is running for errors

**Problem: Server crashes**
- Check that the KB path exists: `{kb_path / 'sources'}`
- Verify markdown files are in the sources folder
- Check terminal output for error messages
"""
    
    return instructions
