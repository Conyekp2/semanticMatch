import sys
from pathlib import Path

import streamlit as st

# ------------------------------------------------------------------
# Fix Python path so Streamlit can import from src/
# ------------------------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Now we can import project modules
from src.data_loader import load_faq_json
from src.matcher import SemanticMatcher
from src.config import MATCHING_CONFIG


# ------------------------------------------------------------------
# Cache matcher per domain for speed
# ------------------------------------------------------------------
@st.cache_resource
def get_matcher(domain: str) -> SemanticMatcher:
    """
    Build and cache a SemanticMatcher for a given domain.
    Avoids recomputing embeddings every time.
    """
    questions, answers = load_faq_json("data/samples/faq.json", domain=domain)
    return SemanticMatcher(questions, metadata=answers)


# ------------------------------------------------------------------
# Main UI
# ------------------------------------------------------------------
def main():
    st.set_page_config(
        page_title="SemanticMatch – Semantic FAQ Engine",
        page_icon="❓",
        layout="wide",
    )

    # Page Header
    st.markdown(
        """
        <div style="text-align: center;">
            <h1>SemanticMatch</h1>
            <p><b>AI-Powered Semantic FAQ Engine</b></p>
            <p>Ask a question in natural language and get Top-K closest FAQ matches.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Sidebar
    st.sidebar.header("Settings")

    domain = st.sidebar.selectbox(
        "Domain",
        options=["support", "hr", "education", "all"],
        index=0,
        help="Choose which FAQ domain to search."
    )

    top_k = st.sidebar.slider(
        "Number of results (Top-K)",
        min_value=1,
        max_value=5,
        value=3,
        help="How many matches to display."
    )

    threshold = st.sidebar.slider(
        "Similarity threshold",
        min_value=0.0,
        max_value=1.0,
        value=float(MATCHING_CONFIG.similarity_threshold),
        step=0.05,
        help="Minimum score for a confident match."
    )

    st.sidebar.markdown("---")
    st.sidebar.write("Embedding model:")

    # Try to get a reasonable model name from the config, whatever attribute it uses
    model_label = getattr(MATCHING_CONFIG, "model_name", None)
    if model_label is None:
        model_label = getattr(MATCHING_CONFIG, "embedding_model", None)
    if model_label is None:
        # Fallback if config doesn’t expose a name attribute
        model_label = "SentenceTransformers model"

    st.sidebar.code(str(model_label))

    # Input field
    st.markdown("### Ask a question")
    user_query = st.text_input(
        "Type your question here",
        placeholder="Example: Can I change my booking?"
    )

    # Button logic
    if st.button("Match FAQ") and user_query.strip():
        with st.spinner("Searching for matches..."):
            matcher = get_matcher(domain)

            # Temporarily adjust threshold
            original_threshold = MATCHING_CONFIG.similarity_threshold
            MATCHING_CONFIG.similarity_threshold = threshold

            result = matcher.match(user_query, top_k=top_k)

            # Restore threshold
            MATCHING_CONFIG.similarity_threshold = original_threshold

        st.markdown("### Results")
        st.write(f"**Best score:** {result['best_score']:.4f}")
        st.write(
            f"**Meets threshold?** "
            f"{'✅ Yes' if result['meets_threshold'] else '⚠️ Not confident'}"
        )

        st.markdown("---")

        # Show ranked matches
        for i, m in enumerate(result["matches"], start=1):
            st.markdown(f"#### #{i} – Score: {m['score']:.4f}")
            st.markdown(f"**Question:** {m['question']}")
            st.markdown(f"**Answer:** {m['metadata']}")
            st.progress(min(max(m['score'], 0.0), 1.0))
            st.markdown("---")

    else:
        st.info("Enter a question above and click **Match FAQ** to see results.")


# ------------------------------------------------------------------
# Run app
# ------------------------------------------------------------------
if __name__ == "__main__":
    main()
