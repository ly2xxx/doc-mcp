# docs-mcp

This directory contains the core logic for `docs-mcp`, including a command-line interface (CLI) and a web user interface.

## Prerequisites

- **Python 3.10+**
- **uv**: Required for running `repomix` and `md-mcp` via `uvx`. [Installation Guide](https://docs.astral.sh/uv/getting-started/installation/)

## Requirements

Ensure you have the necessary library dependencies installed before running the scripts:

```bash
pip install -r requirements.txt
```

## Running the CLI (`cli.py`)

The CLI provides commands to generate knowledge bases, start the web interface, and run the MCP server.

You can run the CLI script directly using Python:

```bash
python cli.py [COMMAND]
```

### Available Commands

1. **`generate`**: Generate a knowledge base from specified code folders.
   ```bash
   python cli.py generate --folder /path/to/code_folder --name my-kb --output /path/to/output_dir
   ```

2. **`web`**: Start the web UI to manage knowledge bases.
   ```bash
   python cli.py web --port 5000
   ```

3. **`serve`**: Start the MCP server for an existing knowledge base.
   ```bash
   python cli.py serve /path/to/kb_dir --port 3000
   ```

Use `python cli.py --help` or `python cli.py [COMMAND] --help` to view detailed information on all available arguments and options.

## Running the Web UI (`web/app.py`)

The web UI provides a visual interface for managing your `doc-mcp` knowledge bases and MCP server. It is built using Flask.

While you can start the web UI via the CLI (`python cli.py web`), you can also run the web application script directly:

```bash
python web/app.py
```

### Options

* `--port`, `-p`: Port to run the web server on (default: `5000`)
* `--host`: Host to bind to (default: `127.0.0.1`)
* `--no-browser`: Start the server without automatically opening the web browser.

Example:
```bash
python web/app.py --port 8080 --host 0.0.0.0 --no-browser
```
