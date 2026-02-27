"""
Knowledge Base Generator Component

Handles KB name input and generation workflow.
"""

import streamlit as st
from pathlib import Path
import sys

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.repomix_runner import (
    run_repomix,
    check_repomix_installed,
    RepomixError,
    RepomixNotFoundError,
    RepomixTimeoutError,
    get_folder_stats
)
from utils.kb_manager import (
    create_kb,
    delete_kb,
    kb_exists,
    KBError,
    KBAlreadyExistsError
)


def render_kb_generator():
    """Render the KB generation UI."""
    
    # KB name input
    st.markdown("**Name your knowledge base:**")
    
    kb_name = st.text_input(
        "Knowledge Base Name",
        value=st.session_state.kb_name,
        placeholder="my-project",
        help="Choose a descriptive name (lowercase, hyphens only)",
        label_visibility="collapsed",
        key="kb_name_input"
    )
    
    # Validate KB name
    kb_name_valid = bool(kb_name and kb_name.replace("-", "").replace("_", "").isalnum())
    
    if kb_name and not kb_name_valid:
        st.warning("⚠️ KB name should only contain letters, numbers, hyphens, and underscores")
    
    # Update session state
    if kb_name != st.session_state.kb_name:
        st.session_state.kb_name = kb_name
    
    st.divider()
    
    # Generate button
    can_generate = (
        len(st.session_state.selected_folders) > 0 
        and kb_name_valid
        and st.session_state.kb_status != "processing"
    )
    
    if st.button(
        "🚀 Generate Knowledge Base",
        type="primary",
        disabled=not can_generate,
        use_container_width=True
    ):
        # Check repomix is installed
        if not check_repomix_installed():
            st.error("❌ Repomix not found!")
            st.error("Install with: `npm install -g repomix`")
            st.info("💡 After installation, refresh this page")
            return
        
        # Start generation
        st.session_state.kb_status = "processing"
        st.session_state.generation_results = []
        
        # Create workspace directory
        workspace = Path.home() / ".code-folders-mcp" / st.session_state.kb_name / "sources"
        workspace.mkdir(parents=True, exist_ok=True)
        
        # Process each folder
        progress_text = st.empty()
        progress_bar = st.progress(0)
        
        total_folders = len(st.session_state.selected_folders)
        generated_files = []
        
        for i, folder in enumerate(st.session_state.selected_folders):
            progress_text.text(f"Processing {i+1}/{total_folders}: {folder.name}")
            
            try:
                # Get folder stats
                stats = get_folder_stats(folder)
                st.session_state.generation_results.append(
                    f"📁 {folder.name}: {stats['num_files']} files, {stats['total_size_mb']} MB"
                )
                
                # Run repomix
                output_file = run_repomix(
                    folder_path=folder,
                    output_name=folder.name,
                    workspace_dir=workspace
                )
                
                # Get output file size
                output_size_mb = output_file.stat().st_size / (1024 * 1024)
                
                st.session_state.generation_results.append(
                    f"✅ Generated: {output_file.name} ({output_size_mb:.2f} MB)"
                )
                
                generated_files.append(output_file)
                
            except RepomixNotFoundError as e:
                st.error(f"❌ {str(e)}")
                st.session_state.kb_status = "idle"
                return
                
            except RepomixTimeoutError as e:
                st.error(f"⏱️ Timeout: {folder.name}")
                st.error(str(e))
                st.session_state.generation_results.append(
                    f"❌ {folder.name}: Timeout"
                )
                
            except RepomixError as e:
                st.error(f"❌ Failed: {folder.name}")
                st.error(str(e))
                st.session_state.generation_results.append(
                    f"❌ {folder.name}: {str(e)}"
                )
            
            # Update progress
            progress = (i + 1) / total_folders
            progress_bar.progress(progress)
        
        # Clear progress indicators
        progress_text.empty()
        progress_bar.empty()
        
        if generated_files:
            # Create KB from generated files
            progress_text.text("Creating knowledge base...")
            
            try:
                # Check if KB already exists
                kb_workspace = Path.home() / ".code-folders-mcp"
                
                if kb_exists(st.session_state.kb_name, kb_workspace):
                    # Ask user to overwrite
                    overwrite = st.warning(
                        f"⚠️ Knowledge base '{st.session_state.kb_name}' already exists. "
                        "Delete and recreate?"
                    )
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("🗑️ Delete & Recreate", type="primary"):
                            delete_kb(st.session_state.kb_name, kb_workspace)
                            st.rerun()
                    with col2:
                        if st.button("❌ Cancel"):
                            st.session_state.kb_status = "idle"
                            st.rerun()
                    return
                
                # Create KB
                kb_stats = create_kb(
                    kb_name=st.session_state.kb_name,
                    md_files=generated_files,
                    workspace_dir=kb_workspace
                )
                
                st.session_state.kb_path = Path(kb_stats["kb_path"])
                st.session_state.kb_status = "ready"
                st.session_state.generation_results.append(
                    f"\n📊 KB Stats:"
                )
                st.session_state.generation_results.append(
                    f"  - Files: {kb_stats['num_files']}"
                )
                st.session_state.generation_results.append(
                    f"  - Total size: {kb_stats['total_size_mb']} MB"
                )
                st.session_state.generation_results.append(
                    f"  - Location: {kb_stats['kb_path']}"
                )
                
                progress_text.empty()
                st.success(f"✅ Knowledge base '{st.session_state.kb_name}' created successfully!")
                st.info("📁 Sources copied to: " + kb_stats['kb_path'])
                st.rerun()
                
            except KBAlreadyExistsError as e:
                st.error(f"❌ {str(e)}")
                st.session_state.kb_status = "idle"
                
            except KBError as e:
                st.error(f"❌ Failed to create KB: {str(e)}")
                st.session_state.kb_status = "idle"
        else:
            st.error("❌ No files were generated successfully")
            st.session_state.kb_status = "idle"
    
    # Show requirements if can't generate
    if not can_generate and st.session_state.kb_status != "processing":
        missing = []
        if len(st.session_state.selected_folders) == 0:
            missing.append("❌ Add at least one folder")
        if not kb_name_valid:
            missing.append("❌ Enter a valid KB name")
        
        if missing:
            st.warning("\n".join(["**Requirements:**"] + missing))
    
    # Status display area
    st.divider()
    st.markdown("**Generation Status:**")
    
    if st.session_state.kb_status == "idle":
        st.info("⚪ Ready to generate - Click the button above when ready")
    
    elif st.session_state.kb_status == "processing":
        st.warning("🟡 Processing folders... (This will show progress bars in next task)")
        # Progress bars will be added in Repomix Integration task
    
    elif st.session_state.kb_status == "ready":
        st.success("✅ Knowledge Base ready!")
        
        if st.session_state.generation_results:
            with st.expander("📊 Generation Results"):
                for result in st.session_state.generation_results:
                    st.text(result)
