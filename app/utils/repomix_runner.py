"""
Repomix Runner Utility

Handles subprocess calls to Repomix for code → markdown conversion.
"""

import subprocess
import shutil
from pathlib import Path
from typing import Optional


class RepomixError(Exception):
    """Base exception for Repomix errors."""
    pass


class RepomixNotFoundError(RepomixError):
    """Raised when repomix is not installed."""
    pass


class RepomixTimeoutError(RepomixError):
    """Raised when repomix execution times out."""
    pass


def check_repomix_installed() -> bool:
    """
    Check if repomix is installed globally.
    
    Returns:
        True if repomix is found in PATH, False otherwise
    """
    return shutil.which("repomix") is not None


def run_repomix(
    folder_path: Path,
    output_name: str,
    workspace_dir: Path,
    timeout: int = 300
) -> Path:
    """
    Run repomix on a folder and return path to generated .md file.
    
    Args:
        folder_path: Absolute path to code folder
        output_name: Name for output file (without .md extension)
        workspace_dir: Directory to store generated .md file
        timeout: Timeout in seconds (default: 300 = 5 minutes)
        
    Returns:
        Path to generated .md file
        
    Raises:
        RepomixNotFoundError: If repomix is not installed
        RepomixTimeoutError: If execution times out
        RepomixError: If repomix fails for other reasons
    """
    # Check repomix is installed
    if not check_repomix_installed():
        raise RepomixNotFoundError(
            "repomix not found. Install with: npm install -g repomix"
        )
    
    # Ensure workspace directory exists
    workspace_dir.mkdir(parents=True, exist_ok=True)
    
    # Output file path
    output_file = workspace_dir / f"{output_name}.md"
    
    # Build repomix command
    cmd = [
        "repomix",
        "--output", str(output_file),
        "--style", "markdown"
    ]
    
    try:
        # Run repomix
        result = subprocess.run(
            cmd,
            cwd=str(folder_path),
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding='utf-8',
            errors='replace'  # Handle encoding issues gracefully
        )
        
        # Check if successful
        if result.returncode != 0:
            error_msg = result.stderr or result.stdout or "Unknown error"
            raise RepomixError(f"repomix failed: {error_msg}")
        
        # Verify output file was created
        if not output_file.exists():
            raise RepomixError(f"Output file not created: {output_file}")
        
        return output_file
        
    except subprocess.TimeoutExpired:
        raise RepomixTimeoutError(
            f"repomix timed out after {timeout} seconds. "
            f"Try processing a smaller folder or increase timeout."
        )
    except FileNotFoundError:
        raise RepomixNotFoundError(
            "repomix command not found. Install with: npm install -g repomix"
        )
    except Exception as e:
        raise RepomixError(f"Unexpected error running repomix: {str(e)}")


def get_folder_stats(folder_path: Path) -> dict:
    """
    Get basic statistics about a folder.
    
    Args:
        folder_path: Path to folder
        
    Returns:
        Dict with 'num_files' and 'total_size_mb'
    """
    try:
        files = list(folder_path.rglob("*"))
        num_files = len([f for f in files if f.is_file()])
        
        total_size = sum(
            f.stat().st_size for f in files if f.is_file()
        )
        total_size_mb = total_size / (1024 * 1024)
        
        return {
            "num_files": num_files,
            "total_size_mb": round(total_size_mb, 2)
        }
    except Exception:
        return {
            "num_files": 0,
            "total_size_mb": 0.0
        }
