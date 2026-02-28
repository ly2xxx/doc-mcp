"""
Folder Selection Component

Allows users to select multiple code folders to process.
"""

import streamlit as st
from pathlib import Path


def render_folder_selector():
    """Render the folder selection UI."""
    
    # Folder input field
    st.markdown("**Add folders containing your code:**")
    
    with st.form("add_folder_form", clear_on_submit=True):
        col1, col2 = st.columns([4, 1])
        
        with col1:
            folder_input = st.text_input(
                "Folder path",
                placeholder="C:\\code\\my-project or /home/user/projects/app",
                label_visibility="collapsed"
            )
        
        with col2:
            add_button = st.form_submit_button("➕ Add", type="primary", use_container_width=True)
        
        # Add folder logic
        if add_button and folder_input:
            folder_path = Path(folder_input.strip())
            
            # Validate folder exists
            if not folder_path.exists():
                st.error(f"❌ Folder not found: {folder_path}")
            elif not folder_path.is_dir():
                st.error(f"❌ Not a directory: {folder_path}")
            elif str(folder_path) in [str(f) for f in st.session_state.selected_folders]:
                st.warning(f"⚠️ Folder already added: {folder_path.name}")
            else:
                st.session_state.selected_folders.append(folder_path)
                st.success(f"✅ Added: {folder_path.name}")
                st.rerun()
    
    # Display selected folders
    st.markdown("**Selected folders:**")
    
    if st.session_state.selected_folders:
        for i, folder in enumerate(st.session_state.selected_folders):
            col1, col2, col3 = st.columns([6, 2, 1])
            
            with col1:
                st.text(f"📁 {folder}")
            
            with col2:
                # Show folder size hint
                try:
                    num_files = len(list(folder.rglob("*")))
                    st.caption(f"{num_files} files")
                except:
                    st.caption("Unknown size")
            
            with col3:
                if st.button("🗑️", key=f"remove_{i}", help="Remove folder"):
                    st.session_state.selected_folders.pop(i)
                    st.rerun()
    else:
        st.info("👆 Add at least one code folder to get started")
    
    # Quick tips
    with st.expander("💡 Tips for selecting folders"):
        st.markdown("""
        **Best practices:**
        - Select project root folders (e.g., `backend/`, `frontend/`)
        - Each folder will become one consolidated .md file via Repomix
        - Smaller, focused folders = better search results
        - Repomix respects `.gitignore` automatically
        
        **What to avoid:**
        - Don't select parent folders with multiple unrelated projects
        - Don't include `node_modules/`, `__pycache__/`, etc. (use .gitignore)
        - Avoid selecting the same folder twice
        """)
