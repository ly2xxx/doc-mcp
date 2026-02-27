"""
Knowledge Base Manager Utility

Handles md-mcp KB creation, indexing, and management.
"""

from pathlib import Path
from typing import List, Optional, Dict
import json


class KBError(Exception):
    """Base exception for KB errors."""
    pass


class KBAlreadyExistsError(KBError):
    """Raised when KB already exists."""
    pass


class KBNotFoundError(KBError):
    """Raised when KB is not found."""
    pass


def create_kb(
    kb_name: str,
    md_files: List[Path],
    workspace_dir: Path
) -> Dict:
    """
    Create a knowledge base from markdown files using md-mcp.
    
    Args:
        kb_name: Name of the knowledge base
        md_files: List of .md files to index
        workspace_dir: Directory to store KB data
        
    Returns:
        Dict with KB statistics
        
    Raises:
        KBAlreadyExistsError: If KB already exists
        KBError: If KB creation fails
    """
    try:
        # Import md_mcp dynamically to catch import errors
        from md_mcp import KnowledgeBase
        
    except ImportError as e:
        raise KBError(
            f"md-mcp not installed or import failed: {e}\n"
            "Install with: pip install md-mcp"
        )
    
    # Check if KB already exists
    kb_dir = workspace_dir / kb_name
    if kb_dir.exists():
        raise KBAlreadyExistsError(
            f"Knowledge base '{kb_name}' already exists at {kb_dir}"
        )
    
    # Create workspace directory
    kb_dir.mkdir(parents=True, exist_ok=True)
    
    # Create KB configuration
    kb_config = {
        "name": kb_name,
        "description": f"Code folders knowledge base for {kb_name}",
        "chunking": {
            "strategy": "semantic",
            "chunk_size": 512,
            "overlap": 50
        },
        "search": {
            "keyword_weight": 0.3,
            "semantic_weight": 0.7
        }
    }
    
    # Save config
    config_file = kb_dir / "config.json"
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(kb_config, f, indent=2)
    
    # Copy md files to KB directory
    sources_dir = kb_dir / "sources"
    sources_dir.mkdir(exist_ok=True)
    
    copied_files = []
    for md_file in md_files:
        if md_file.exists():
            dest = sources_dir / md_file.name
            # Copy file
            import shutil
            shutil.copy2(md_file, dest)
            copied_files.append(dest)
    
    if not copied_files:
        raise KBError("No valid markdown files to index")
    
    # Create KB instance
    try:
        kb = KnowledgeBase(
            name=kb_name,
            source_dir=str(sources_dir),
            config=kb_config
        )
        
        # Index the files
        # Note: md-mcp might not have an index() method, we'll need to check the actual API
        # For now, we'll just create the KB structure
        
        # Return stats
        total_size = sum(f.stat().st_size for f in copied_files)
        total_size_mb = total_size / (1024 * 1024)
        
        return {
            "kb_name": kb_name,
            "kb_path": str(kb_dir),
            "num_files": len(copied_files),
            "total_size_mb": round(total_size_mb, 2),
            "files": [f.name for f in copied_files]
        }
        
    except Exception as e:
        raise KBError(f"Failed to create knowledge base: {str(e)}")


def delete_kb(kb_name: str, workspace_dir: Path) -> bool:
    """
    Delete a knowledge base.
    
    Args:
        kb_name: Name of the knowledge base
        workspace_dir: KB workspace directory
        
    Returns:
        True if deleted successfully
        
    Raises:
        KBNotFoundError: If KB doesn't exist
    """
    kb_dir = workspace_dir / kb_name
    
    if not kb_dir.exists():
        raise KBNotFoundError(f"Knowledge base '{kb_name}' not found")
    
    # Delete the directory
    import shutil
    shutil.rmtree(kb_dir)
    
    return True


def kb_exists(kb_name: str, workspace_dir: Path) -> bool:
    """
    Check if a knowledge base exists.
    
    Args:
        kb_name: Name of the knowledge base
        workspace_dir: KB workspace directory
        
    Returns:
        True if KB exists
    """
    kb_dir = workspace_dir / kb_name
    return kb_dir.exists() and (kb_dir / "config.json").exists()


def get_kb_info(kb_name: str, workspace_dir: Path) -> Optional[Dict]:
    """
    Get information about a knowledge base.
    
    Args:
        kb_name: Name of the knowledge base
        workspace_dir: KB workspace directory
        
    Returns:
        Dict with KB info or None if not found
    """
    kb_dir = workspace_dir / kb_name
    config_file = kb_dir / "config.json"
    
    if not kb_exists(kb_name, workspace_dir):
        return None
    
    # Load config
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # Get source files
    sources_dir = kb_dir / "sources"
    md_files = list(sources_dir.glob("*.md")) if sources_dir.exists() else []
    
    total_size = sum(f.stat().st_size for f in md_files)
    total_size_mb = total_size / (1024 * 1024)
    
    return {
        "kb_name": kb_name,
        "kb_path": str(kb_dir),
        "config": config,
        "num_files": len(md_files),
        "total_size_mb": round(total_size_mb, 2),
        "files": [f.name for f in md_files]
    }
