"""
Knowledge Base Generator Component

Handles KB name input and generation workflow.
"""

import streamlit as st
from pathlib import Path


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
        # Placeholder for actual generation logic
        st.session_state.kb_status = "processing"
        
        # This will be implemented in the next task (Repomix Integration)
        st.info("⏳ Generation logic will be implemented in the next task...")
        st.info("🔧 Next: Implement Repomix integration to process folders")
        
        # For now, reset status after showing message
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
