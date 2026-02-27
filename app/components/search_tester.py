"""
Search Testing Component

Test KB search quality before connecting to Claude.
"""

import streamlit as st


def render_search_tester():
    """Render the search testing UI."""
    
    st.markdown("**Test your knowledge base:**")
    
    # Search input
    query = st.text_input(
        "Search query",
        placeholder="How does authentication work?",
        label_visibility="collapsed",
        key="search_query"
    )
    
    # Search button
    if st.button("🔍 Search", disabled=not query, use_container_width=True):
        # Placeholder - will be implemented in Testing task
        st.info("🔧 Search functionality will be implemented in the Testing task")
        st.info("For now, this is just a UI placeholder")
    
    # Results placeholder
    if query:
        st.markdown("**Results:**")
        st.caption("Search results will appear here once search is implemented")
