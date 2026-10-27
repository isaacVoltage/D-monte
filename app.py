"""
Simple Inverted Index Generator for Information Retrieval
---------------------------------------------------------
A clean, interactive Streamlit application designed for college mini-project
demonstrations and laboratory exploration.

Features:
- Add custom documents or load preset classroom collections.
- Real-time automatic inverted index generation.
- Case-insensitive keyword searching.
- Boolean retrieval (AND, OR) with set operations.
- Vocabulary metrics & inverted index inspection table.
- Interactive educational How to Work guide and algorithmic walkthrough.
"""

import streamlit as st
import pandas as pd
import html
import re
from inverted_index import InvertedIndex

# Configure Streamlit page
st.set_page_config(
    page_title="Inverted Index Generator | IR Mini-Project",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for modern, clean academic presentation
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

    /* Main container styling */
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 24px;
        border-radius: 12px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    }
    .main-header h1 {
        color: #ffffff !important;
        margin: 0;
        font-size: 2.1rem;
        font-weight: 700;
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
    }
    .main-header p {
        color: #e0e7ff !important;
        margin: 8px 0 0 0;
        font-size: 1.05rem;
    }
    .badge-pill {
        display: inline-block;
        background: rgba(255, 255, 255, 0.2);
        color: #ffffff;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        margin-right: 8px;
        margin-top: 10px;
    }
    .doc-card {
        background-color: rgba(148, 163, 184, 0.08);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 14px;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .doc-card:hover {
        border-color: rgba(148, 163, 184, 0.4);
        box-shadow: 0 3px 10px rgba(0,0,0,0.06);
    }
    .doc-card-title {
        font-size: 1.15rem;
        font-weight: 600;
        color: inherit;
        margin-bottom: 6px;
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
    }
    .match-tag {
        background-color: #3b82f6;
        color: #ffffff;
        font-size: 0.8rem;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 4px;
        margin-right: 6px;
    }
    .highlight {
        background-color: #fef08a;
        color: #854d0e;
        font-weight: 600;
        padding: 1px 4px;
        border-radius: 3px;
    }
    
    /* FAQ Section - Clean modern typography that works across Light & Dark themes */
    .faq-answer-card {
        background: rgba(59, 130, 246, 0.06);
        border: 1px solid rgba(59, 130, 246, 0.25);
        border-left: 5px solid #2563eb;
        padding: 16px 22px;
        border-radius: 0 10px 10px 0;
        margin: 8px 0 14px 0;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        font-size: 1.03rem;
        line-height: 1.75;
        letter-spacing: 0.01em;
        color: inherit;
    }
    .faq-badge {
        display: inline-block;
        background: #2563eb;
        color: #ffffff !important;
        font-weight: 700;
        font-size: 0.75rem;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        padding: 3px 9px;
        border-radius: 4px;
        margin-right: 8px;
        vertical-align: middle;
    }
    .faq-answer-card code {
        font-family: 'JetBrains Mono', monospace;
        background: rgba(148, 163, 184, 0.2);
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 0.9em;
        color: inherit;
    }
    .faq-answer-card ul {
        margin-top: 10px;
        margin-bottom: 8px;
        padding-left: 22px;
    }
    .faq-answer-card li {
        margin-bottom: 6px;
    }
    .formula-box {
        background-color: rgba(148, 163, 184, 0.08);
        border: 1px dashed rgba(148, 163, 184, 0.3);
        padding: 12px;
        border-radius: 6px;
        font-family: 'JetBrains Mono', monospace;
        color: inherit;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "Dark"

if "engine" not in st.session_state:
    st.session_state.engine = InvertedIndex()
    # Preload the classroom preset so user sees immediate results on launch
    st.session_state.engine.load_sample_documents(preset="classroom")

engine: InvertedIndex = st.session_state.engine

# ----------------- SIDEBAR -----------------
with st.sidebar:
    # Left Corner Top Theme Toggle Mode
    theme_col1, theme_col2 = st.columns([1, 1.8])
    with theme_col1:
        st.markdown("<div style='font-size: 0.95rem; font-weight: 700; margin-top: 6px;'>🌓 Theme:</div>", unsafe_allow_html=True)
    with theme_col2:
        selected_theme = st.radio(
            "Theme Mode",
            options=["🌙 Dark", "☀️ Light"],
            index=0 if st.session_state.theme_mode == "Dark" else 1,
            horizontal=True,
            label_visibility="collapsed",
            key="theme_mode_radio"
        )
    current_theme = "Dark" if "Dark" in selected_theme else "Light"
    st.session_state.theme_mode = current_theme
    st.divider()

# Apply Dynamic Light / Dark Theme CSS
if st.session_state.theme_mode == "Light":
    st.markdown("""
    <style>
        /* Base page in Light Mode */
        .stApp {
            background-color: #f8fafc !important;
            color: #0f172a !important;
        }
        .stApp [data-testid="stMarkdownContainer"] p,
        .stApp [data-testid="stMarkdownContainer"] span,
        .stApp [data-testid="stMarkdownContainer"] div,
        .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
        .stApp [data-testid="stWidgetLabel"] p,
        .stApp [data-testid="stWidgetLabel"] label,
        .stApp label {
            color: #0f172a !important;
        }

        /* Sidebar in Light Mode */
        section[data-testid="stSidebar"] {
            background-color: #f1f5f9 !important;
            border-right: 1px solid #cbd5e1 !important;
        }
        section[data-testid="stSidebar"] * {
            color: #0f172a !important;
        }
        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] span,
        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] div,
        section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
        section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] label,
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] h4,
        section[data-testid="stSidebar"] span {
            color: #0f172a !important;
        }
        section[data-testid="stSidebar"] [data-testid="stMetricValue"] div,
        section[data-testid="stSidebar"] [data-testid="stMetricValue"] {
            color: #1d4ed8 !important;
            font-weight: 700 !important;
        }
        section[data-testid="stSidebar"] [data-testid="stMetricLabel"] p,
        section[data-testid="stSidebar"] [data-testid="stMetricLabel"] {
            color: #475569 !important;
            font-weight: 600 !important;
        }
        section[data-testid="stSidebar"] p[data-testid="stCaptionContainer"],
        section[data-testid="stSidebar"] .stCaption {
            color: #475569 !important;
        }
        section[data-testid="stSidebar"] button {
            background-color: #ffffff !important;
            color: #0f172a !important;
            border: 1px solid #cbd5e1 !important;
            font-weight: 600 !important;
        }
        section[data-testid="stSidebar"] button:hover {
            background-color: #e2e8f0 !important;
            border-color: #94a3b8 !important;
        }

        /* Tabs in Light Mode */
        button[data-baseweb="tab"] {
            background-color: transparent !important;
        }
        button[data-baseweb="tab"] p,
        button[data-baseweb="tab"] div,
        button[data-baseweb="tab"] span {
            color: #475569 !important;
            font-weight: 500 !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] p,
        button[data-baseweb="tab"][aria-selected="true"] div,
        button[data-baseweb="tab"][aria-selected="true"] span {
            color: #1d4ed8 !important;
            font-weight: 700 !important;
        }

        /* Form Inputs & Selectbox in Light Mode */
        .stTextInput input, 
        .stTextArea textarea {
            background-color: #ffffff !important;
            color: #0f172a !important;
            border: 1.5px solid #cbd5e1 !important;
            border-radius: 8px !important;
        }
        .stTextInput input::placeholder, 
        .stTextArea textarea::placeholder {
            color: #64748b !important;
        }
        div[data-baseweb="select"] > div {
            background-color: #ffffff !important;
            border: 1.5px solid #cbd5e1 !important;
            border-radius: 8px !important;
        }
        div[data-baseweb="select"] * {
            color: #0f172a !important;
        }
        div[data-baseweb="popover"] ul,
        div[data-baseweb="popover"] li {
            background-color: #ffffff !important;
            color: #0f172a !important;
        }

        /* Expanders in Light Mode */
        div[data-testid="stExpander"] {
            background-color: #ffffff !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 8px !important;
        }
        div[data-testid="stExpander"] details summary span,
        div[data-testid="stExpander"] details summary p {
            color: #0f172a !important;
            font-weight: 600 !important;
        }
        div[data-testid="stExpander"] details > div {
            color: #0f172a !important;
        }

        /* Alert / Info Boxes in Light Mode */
        div[data-testid="stAlert"] {
            background-color: #eff6ff !important;
            border: 1px solid #bfdbfe !important;
        }
        div[data-testid="stAlert"] * {
            color: #1e3a8a !important;
        }

        /* Document and FAQ cards in Light Mode */
        .doc-card {
            background-color: #ffffff !important;
            border: 1px solid #e2e8f0 !important;
            box-shadow: 0 1px 4px rgba(0,0,0,0.05) !important;
        }
        .doc-card-title {
            color: #0f172a !important;
        }
        .doc-card p {
            color: #334155 !important;
        }
        .faq-answer-card {
            background: #f8fafc !important;
            border: 1px solid #cbd5e1 !important;
            border-left: 5px solid #2563eb !important;
            color: #0f172a !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
        }
        .formula-box {
            background-color: #ffffff !important;
            border: 1px dashed #cbd5e1 !important;
            color: #0f172a !important;
        }

        /* Header Banner retains white text on blue */
        .main-header {
            background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%) !important;
            box-shadow: 0 4px 15px rgba(37,99,235,0.15) !important;
        }
        .main-header h1, .main-header p, .main-header span, .badge-pill {
            color: #ffffff !important;
        }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
        .stApp {
            background-color: #0e1117 !important;
            color: #f1f5f9 !important;
        }
        section[data-testid="stSidebar"] {
            background-color: #161b22 !important;
            border-right: 1px solid #30363d !important;
        }
        .main-header {
            background: linear-gradient(135deg, #1e3a8a 0%, #0f172a 100%) !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.4) !important;
        }
        .main-header h1, .main-header p, .badge-pill {
            color: #ffffff !important;
        }
        .doc-card {
            background-color: #1e293b !important;
            border: 1px solid #334155 !important;
            box-shadow: 0 2px 6px rgba(0,0,0,0.25) !important;
        }
        .doc-card-title {
            color: #f8fafc !important;
        }
        .doc-card p {
            color: #cbd5e1 !important;
        }
        .faq-answer-card {
            background: #0f172a !important;
            border: 1px solid #1e3a8a !important;
            border-left: 5px solid #3b82f6 !important;
            color: #e2e8f0 !important;
        }
        .formula-box {
            background-color: #1e293b !important;
            border: 1px dashed #475569 !important;
            color: #e2e8f0 !important;
        }
        /* Form inputs styling for Dark Mode */
        .stTextInput input, .stTextArea textarea {
            background-color: #161b22 !important;
            color: #f1f5f9 !important;
            border: 1px solid #30363d !important;
        }
    </style>
    """, unsafe_allow_html=True)

# Header banner
st.markdown("""
<div class="main-header">
    <h1>Design & Implementation of a Simple Inverted Index Generator</h1>
    <p>Beginner-friendly Information Retrieval (IR) System with Boolean Query Processing</p>
    <div>
        <span class="badge-pill">📚 Course: Information Retrieval</span>
        <span class="badge-pill">⚡ Architecture: Inverted Index & Postings Lists</span>
        <span class="badge-pill">🔍 Retrieval: Keyword, Boolean AND, Boolean OR</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Resume Sidebar content
with st.sidebar:
    st.header("⚙️ Controls & Stats")

    # Document / Index Statistics
    stats = engine.get_statistics()
    st.subheader("📊 Collection Metrics")
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.metric("Total Documents", stats["total_documents"])
    with col_m2:
        st.metric("Unique Terms", stats["total_vocabulary"])

    st.caption(f"Total Postings: **{stats['total_postings']}** | Word Tokens: **{stats['total_word_occurrences']}**")
    st.divider()

    # Presets & Data Management
    st.subheader("📁 Sample Collections")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        if st.button("Classroom (3 Docs)", use_container_width=True, help="Load Doc 1, Doc 2, and Doc 3 standard example"):
            engine.clear()
            engine.load_sample_documents(preset="classroom")
            st.toast("Classroom samples loaded!", icon="✅")
            st.rerun()

    with col_p2:
        if st.button("Extended (6 Docs)", use_container_width=True, help="Load 6 documents on IR & Search Engines"):
            engine.clear()
            engine.load_sample_documents(preset="extended")
            st.toast("Extended samples loaded!", icon="✅")
            st.rerun()

    if st.button("🗑️ Reset & Clear All", type="secondary", use_container_width=True, help="Clear all documents and reset the index"):
        engine.clear()
        st.toast("Document collection and index reset to empty.", icon="ℹ️")
        st.rerun()

    st.divider()

    # Quick Term Lookup Tool
    st.subheader("🔎 Quick Term Lookup")
    lookup_term = st.text_input("Enter term to inspect:", placeholder="e.g. python").strip().lower()
    if lookup_term:
        index_dict = engine.get_index()
        if lookup_term in index_dict:
            postings = index_dict[lookup_term]
            st.success(f"**'{lookup_term}'** exists in: {', '.join([f'Doc {d}' for d in postings])}")
            st.caption(f"Posting list: `{postings}` (Document Frequency: {len(postings)})")
        else:
            st.warning(f"Term '{lookup_term}' is not in the vocabulary.")

    st.divider()
    st.markdown("### 📘 System Info")
    st.caption("**Course:** Information Retrieval (CS/IT)\n**Module:** Inverted Index & Query Processing")


# ----------------- MAIN TABS -----------------
tab1, tab2, tab3, tab4 = st.tabs([
    "🔍 Search Engine",
    "📄 Document Collection",
    "📑 Inverted Index Table",
    "⚙️ How to Work"
])


def highlight_text(text: str, terms: list[str]) -> str:
    """Escapes HTML and highlights matching search terms in text."""
    if not text:
        return ""
    safe_text = html.escape(text)
    for term in terms:
        if not term:
            continue
        pattern = re.compile(rf"\b({re.escape(term)})\b", re.IGNORECASE)
        safe_text = pattern.sub(r'<span class="highlight">\1</span>', safe_text)
    return safe_text


# ----------------- TAB 1: SEARCH ENGINE -----------------
with tab1:
    st.subheader("🔍 Search Query Interface")
    st.markdown("Search across all indexed documents using case-insensitive keywords or Boolean operators.")

    col_q, col_mode = st.columns([3, 1])
    with col_q:
        search_query = st.text_input(
            "Search Query:",
            placeholder="e.g. python, love, java, easy...",
            help="Type one or more words. Punctuation is stripped automatically."
        )
    with col_mode:
        search_mode = st.selectbox(
            "Search Mode:",
            ["Keyword / Phrase", "Boolean AND", "Boolean OR"],
            help="Keyword: finds matching docs. Boolean AND: requires all terms. Boolean OR: requires at least one term."
        )

    # Convert selectbox to internal mode
    mode_key = "KEYWORD"
    if search_mode == "Boolean AND":
        mode_key = "AND"
    elif search_mode == "Boolean OR":
        mode_key = "OR"

    if search_query:
        query_tokens = InvertedIndex.tokenize(search_query)

        # Query Inspection Box
        with st.expander("🛠️ Query Analysis & Execution Trace", expanded=False):
            st.markdown(f"- **Raw Query:** `{search_query}`")
            st.markdown(f"- **Extracted Tokens:** `{query_tokens}`")
            st.markdown(f"- **Search Strategy:** `{search_mode}`")
            if mode_key == "AND":
                steps = [f"Postings('{t}'): {engine.index.get(t, [])}" for t in query_tokens]
                st.markdown(f"- **Step 1: Term Postings:** {', '.join(steps)}")
                st.markdown("- **Step 2: Set Intersection (∩):** Retain only document IDs common to all terms.")
            elif mode_key == "OR":
                steps = [f"Postings('{t}'): {engine.index.get(t, [])}" for t in query_tokens]
                st.markdown(f"- **Step 1: Term Postings:** {', '.join(steps)}")
                st.markdown("- **Step 2: Set Union (∪):** Combine all unique document IDs across terms.")

        results = engine.search(search_query, mode=mode_key)

        st.markdown(f"### 📋 Search Results ({len(results)} found)")

        if not results:
            st.warning(f"No documents matched the query: **'{search_query}'** using **{search_mode}**.")
            st.info("💡 **Tips:** Verify your spelling, check the Inverted Index Table tab to inspect vocabulary, or try using **Boolean OR**.")
        else:
            for item in results:
                matched_badges = "".join([f'<span class="match-tag">✓ {html.escape(t)}</span>' for t in item["matched_terms"]])
                highlighted_content = highlight_text(item["content"], item["matched_terms"])
                highlighted_title = highlight_text(item["title"], item["matched_terms"])

                st.markdown(f"""
                <div class="doc-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <span class="doc-card-title">{highlighted_title}</span>
                        <span style="background-color: #2563eb; color: white; padding: 2px 10px; border-radius: 12px; font-size: 0.85rem; font-weight: bold;">
                            {item['doc_label']}
                        </span>
                    </div>
                    <p style="color: #334155; margin-bottom: 8px; font-size: 0.95rem; line-height: 1.5;">{highlighted_content}</p>
                    <div style="font-size: 0.85rem; color: #64748b;">
                        <span><strong>Matched Terms:</strong> {matched_badges}</span>
                        <span style="margin-left: 12px;"><strong>Term Occurrences:</strong> {item['frequency_count']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("👋 Enter a keyword or phrase above to search the document collection.")
        if stats["total_documents"] == 0:
            st.warning("Your collection is currently empty! Please load sample documents from the sidebar or add your own in the **Document Collection** tab.")


# ----------------- TAB 2: DOCUMENT COLLECTION -----------------
with tab2:
    st.subheader("📄 Document Management")
    st.markdown("Add documents to your Information Retrieval collection. The inverted index will update automatically.")

    with st.expander("➕ Add New Document", expanded=True):
        with st.form("add_doc_form", clear_on_submit=True):
            col_t1, col_t2 = st.columns([1, 2])
            with col_t1:
                new_title = st.text_input("Document Title (Optional):", placeholder="e.g. Python Guide")
            with col_t2:
                st.caption("A default title (e.g. Doc N) will be assigned if left empty.")

            new_content = st.text_area(
                "Document Content:*",
                placeholder="Enter text here (e.g. Python is widely used in Artificial Intelligence and Web Development)",
                height=110
            )

            submit_btn = st.form_submit_button("Index Document", type="primary")

            if submit_btn:
                if not new_content.strip():
                    st.error("Please enter some text content to index.")
                else:
                    new_id = engine.add_document(new_title, new_content)
                    st.success(f"✅ Added Document as **Doc {new_id}** and updated the Inverted Index!")
                    st.rerun()

    st.subheader(f"📚 Current Documents ({stats['total_documents']})")
    all_docs = engine.get_all_documents()

    if not all_docs:
        st.info("No documents in collection. Use the form above or click **Classroom (3 Docs)** in the sidebar.")
    else:
        for doc in all_docs:
            with st.container():
                st.markdown(f"""
                <div class="doc-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span class="doc-card-title">{html.escape(doc.title)}</span>
                        <span style="background-color: #475569; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.8rem;">
                            ID: {doc.doc_id}
                        </span>
                    </div>
                    <p style="color: #334155; margin-top: 6px; font-size: 0.95rem;">{html.escape(doc.content)}</p>
                </div>
                """, unsafe_allow_html=True)


# ----------------- TAB 3: INVERTED INDEX TABLE -----------------
with tab3:
    st.subheader("📑 Generated Inverted Index")
    st.markdown("""
    An **Inverted Index** is the fundamental data structure used by search engines.
    Instead of mapping *Documents → Words* (Forward Index), it maps **Words → Documents** (Inverted Index).
    """)

    table_data = engine.get_index_table_data()

    if not table_data:
        st.warning("The inverted index is currently empty because no documents have been added.")
    else:
        df = pd.DataFrame(table_data)

        # Search filter within index table
        filter_col, count_col = st.columns([3, 1])
        with filter_col:
            term_filter = st.text_input("Filter Vocabulary Terms:", placeholder="Type to filter terms...").strip().lower()
        with count_col:
            st.metric("Total Vocabulary", len(df))

        if term_filter:
            filtered_df = df[df["Term"].str.contains(term_filter, case=False, na=False)]
        else:
            filtered_df = df

        st.dataframe(
            filtered_df,
            column_config={
                "Term": st.column_config.TextColumn("Vocabulary Term (Word)", width="medium"),
                "Posting List (Doc IDs)": st.column_config.TextColumn("Posting List [Doc IDs]", width="medium"),
                "Document Labels": st.column_config.TextColumn("Documents", width="medium"),
                "Document Frequency (DF)": st.column_config.NumberColumn("Document Frequency (DF)", width="small")
            },
            use_container_width=True,
            hide_index=True
        )

        # Download index option
        csv_data = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Inverted Index as CSV",
            data=csv_data,
            file_name="inverted_index_data.csv",
            mime="text/csv"
        )


# ----------------- TAB 4: HOW TO WORK -----------------
with tab4:
    st.subheader("⚙️ How to Work & Algorithmic Explanation")

    st.markdown("### 1. How an Inverted Index Works")
    st.markdown(r"""
    In traditional file storage, documents contain words. Finding which documents contain the keyword *"Python"* would require a full text scan (**linear search / grep**), which takes $\mathcal{O}(N \times M)$ time and becomes unacceptably slow as collections grow.
    
    An **Inverted Index** reverses this relationship by creating a dictionary that maps each unique word directly to its containing documents:
    """)

    st.markdown("""
    ```
    Forward Index (Documents -> Words):   Inverted Index (Words -> Documents):
    Doc 1 -> [i, love, python]             easy   -> [Doc 2]
    Doc 2 -> [python, is, easy]     ==>    java   -> [Doc 3]
    Doc 3 -> [i, love, java]               love   -> [Doc 1, Doc 3]
                                           python -> [Doc 1, Doc 2]
    ```
    """)

    st.markdown("### 2. Step-by-Step Processing Pipeline")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("""
        **Step 1: Document Ingestion**
        - Assign sequential unique `doc_id`.
        - Clean and parse title and content.
        """)
    with c2:
        st.markdown("""
        **Step 2: Tokenization**
        - Split text into word tokens.
        - Strip punctuation and symbols.
        - Case fold to lowercase.
        """)
    with c3:
        st.markdown("""
        **Step 3: Index Construction**
        - Collect unique terms per document.
        - Append `doc_id` to posting list.
        - Prevent duplicate postings.
        """)
    with c4:
        st.markdown(r"""
        **Step 4: Query Evaluation**
        - Tokenize query terms.
        - Compute Set Logic:
          - Conjunction: $P(A) \cap P(B)$
          - Disjunction: $P(A) \cup P(B)$
        """)

    st.divider()

    st.markdown("### 3. Frequently Asked Questions (FAQ)")

    with st.expander("📌 What is an Inverted Index and why is it called 'inverted'?", expanded=True):
        st.markdown("""
        <div class="faq-answer-card">
            <span class="faq-badge">Answer</span>
            An <strong>inverted index</strong> is a dictionary-based data structure that maps words (vocabulary terms) to the identifiers of the documents containing them. It is called <em>"inverted"</em> because instead of pointing from documents to the words they contain (the forward index), it points in reverse: from words to the documents that contain them.
        </div>
        """, unsafe_allow_html=True)

    with st.expander("📌 What is a Posting List in Information Retrieval?", expanded=False):
        st.markdown("""
        <div class="faq-answer-card">
            <span class="faq-badge">Answer</span>
            A <strong>posting list</strong> (or inverted list) is an ordered list of document IDs associated with a specific vocabulary term. For example, for the term <code>python</code>, its posting list is <code>[1, 2]</code>, indicating that Doc 1 and Doc 2 contain the word.
        </div>
        """, unsafe_allow_html=True)

    with st.expander("📌 How do Boolean AND and OR searches operate on posting lists?", expanded=False):
        st.markdown(r"""
        <div class="faq-answer-card">
            <span class="faq-badge">Answer</span>
            Boolean queries are executed as direct set operations on the posting lists:
            <ul>
                <li><strong>Boolean AND (Conjunction):</strong> Finds the <em>intersection</em> of posting lists: $P(t_1) \cap P(t_2)$. Only documents present in both lists are returned.</li>
                <li><strong>Boolean OR (Disjunction):</strong> Finds the <em>union</em> of posting lists: $P(t_1) \cup P(t_2)$. Documents present in either list are returned.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("📌 How does the system prevent duplicate document IDs when a word appears repeatedly in a single document?", expanded=False):
        st.markdown("""
        <div class="faq-answer-card">
            <span class="faq-badge">Answer</span>
            Before appending a <code>doc_id</code> to a term's posting list, the system deduplicates terms within each document (or verifies <code>if doc_id not in index[term]</code>). The within-document term frequency is recorded for ranking, but the document identifier is saved only once in the posting list.
        </div>
        """, unsafe_allow_html=True)

    with st.expander("📌 What is the time complexity of searching with an Inverted Index versus Linear Scan?", expanded=False):
        st.markdown(r"""
        <div class="faq-answer-card">
            <span class="faq-badge">Answer</span>
            Comparing algorithmic efficiency:
            <ul>
                <li><strong>Linear Scan (Grep):</strong> $\mathcal{O}(N \times M)$ where $N$ is total documents and $M$ is average document length. Every single document must be completely scanned.</li>
                <li><strong>Inverted Index:</strong> $\mathcal{O}(1)$ average hash table lookup for each query term, followed by an $\mathcal{O}(L_1 + L_2)$ merge for posting lists of lengths $L_1$ and $L_2$. Only relevant documents are accessed!</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
