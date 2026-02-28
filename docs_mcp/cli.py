#!/usr/bin/env python3
"""
docs-mcp CLI - Command-line interface

Supports both CLI and web UI modes.
"""

import sys
import click
from pathlib import Path


@click.group()
@click.version_option()
def main():
    """docs-mcp - Convert code folders into Claude Desktop knowledge bases"""
    pass


@main.command()
@click.option('--folder', '-f', multiple=True, type=click.Path(exists=True),
              help='Folder to process (can be specified multiple times)')
@click.option('--output', '-o', type=click.Path(),
              help='Output directory for knowledge base')
@click.option('--name', '-n', default='kb',
              help='Knowledge base name (default: kb)')
def generate(folder, output, name):
    """Generate knowledge base from code folders"""
    if not folder:
        click.echo("Error: No folders specified. Use --folder to add folders.")
        sys.exit(1)
    
    click.echo(f"Generating knowledge base '{name}' from {len(folder)} folder(s)...")
    
    import subprocess
    import os
    
    # Calculate output path
    out_dir = Path(output) if output else Path.home() / ".docs-mcp" / "kbs" / name
    
    # Clear existing files in the KB directory
    import shutil
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # Use UTF-8 environment for Windows
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    
    try:
        for f in folder:
            f_path = str(f)
            f_name = os.path.basename(f_path)
            out_file = out_dir / f"{f_name}.md"
            
            cmd = ["uvx", "repomix", "--output", str(out_file), f_path]
            click.echo(f"Running command: {' '.join(cmd)}")
            subprocess.run(cmd, check=True, env=env)
            
    except subprocess.CalledProcessError as e:
        click.echo(f"Error generating KB: {e}")
        sys.exit(1)
    
    click.echo("✅ Knowledge base generated successfully!")
    click.echo(f"Output: {output or 'default location'}")


@main.command()
@click.option('--port', '-p', default=5000, type=int,
              help='Port to run web server on (default: 5000)')
@click.option('--host', '-h', default='127.0.0.1',
              help='Host to bind to (default: 127.0.0.1)')
@click.option('--no-browser', is_flag=True,
              help='Do not open browser automatically')
def web(port, host, no_browser):
    """Start web UI for managing knowledge bases"""
    try:
        try:
            from docs_mcp.web.app import start_web_server
        except ImportError:
            from web.app import start_web_server
    except ImportError:
        click.echo("Error: Web UI dependencies not installed.")
        click.echo("Install with: pip install docs-mcp[web]")
        sys.exit(1)
    
    try:
        start_web_server(port=port, host=host, open_browser=not no_browser)
    except KeyboardInterrupt:
        click.echo("\nServer stopped.")
    except Exception as e:
        click.echo(f"Error: {e}")
        sys.exit(1)


@main.command()
@click.argument('kb_path', type=click.Path(exists=True))
@click.option('--port', '-p', type=int, default=3000,
              help='MCP server port (default: 3000)')
def serve(kb_path, port):
    """Start MCP server for a knowledge base"""
    click.echo(f"Starting MCP server for: {kb_path}")
    click.echo(f"Port: {port}")
    
    import subprocess
    cmd = ["uvx", "md-mcp", "--folder", kb_path]
    
    # Use UTF-8 environment for Windows
    import os
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    
    try:
        subprocess.run(cmd, check=True, env=env)
    except subprocess.CalledProcessError as e:
        click.echo(f"Error starting server: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        click.echo("\nServer stopped.")
    
    click.echo("✅ MCP server started")
    click.echo("\nAdd this to your Claude Desktop config:")
    click.echo(f"""
{{
  "mcpServers": {{
    "{Path(kb_path).name}": {{
      "command": "uvx",
      "args": ["md-mcp", "{kb_path}"]
    }}
  }}
}}
    """)


if __name__ == '__main__':
    main()
