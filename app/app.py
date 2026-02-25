import sys
import os
import time
import uuid
import streamlit as st
from dotenv import load_dotenv
from prometheus_client import start_http_server, Counter, Histogram

# ---- 1. STREAMLIT PAGE CONFIG ----
st.set_page_config(page_title="📚 Book Recommender", layout="centered")

# ---- 2. PATH & ENVIRONMENT SETUP ----
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

load_dotenv()

from pipeline.recommendation_pipeline import BookRecommendationPipeline
from utils.logger import get_logger

logger = get_logger(__name__)

# ---- 3. THE ULTIMATE METRICS SETUP ----
@st.cache_resource
def init_metrics():
    try:
        start_http_server(8000)
    except OSError:
        pass
    
    # Traffic & Users
    req_total = Counter('rag_requests_total', 'Total requests')
    err_total = Counter('rag_errors_total', 'Total errors')
    users_total = Counter('rag_unique_users_total', 'Total unique visitors')
    
    # Speed
    lat_e2e = Histogram('rag_end_to_end_seconds', 'Total request time')
    
    # LLM Economics (Tokens & Cost)
    tokens_total = Counter('rag_tokens_total', 'Tokens used', ['token_type'])
    cost_total = Counter('rag_estimated_cost_usd', 'Estimated API cost in USD')
    
    # Quality
    user_feedback = Counter('rag_user_feedback_total', 'User satisfaction', ['sentiment'])
    
    return req_total, err_total, users_total, lat_e2e, tokens_total, cost_total, user_feedback

# Load the metrics engine securely
(m_requests, m_errors, m_users, m_latency_e2e, 
 m_tokens, m_cost, m_feedback) = init_metrics()


# ---- 4. TRACK UNIQUE VISITORS ----
# If this is a user's first time loading the page, generate an ID and count them!
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    m_users.inc()


# ---- 5. LOAD AI PIPELINE ----
@st.cache_resource
def load_pipeline():
    return BookRecommendationPipeline()

pipeline = load_pipeline()


# ---- 6. STREAMLIT UI & LOGIC ----
st.title("📚 AI Book Recommendation System")
st.write("Describe what kind of books you want to read.")

query = st.text_input(
    "Your preference",
    placeholder="e.g. dystopian novels with strong female protagonists"
)

if st.button("Get Recommendations"):
    if query.strip():
        m_requests.inc()
        
        with st.spinner("Finding recommendations..."):
            with m_latency_e2e.time():
                try:
                    # 1. Run your pipeline
                    result = pipeline.recommend(query)
                    
                    # 2. MIMIC TOKENS: 1 word is roughly 1.3 tokens
                    est_prompt_tokens = int(len(query.split()) * 1.3)
                    est_completion_tokens = int(len(str(result).split()) * 1.3)
                    
                    m_tokens.labels(token_type='prompt').inc(est_prompt_tokens)
                    m_tokens.labels(token_type='completion').inc(est_completion_tokens)
                    
                    # 3. MIMIC COST: Assuming standard pricing (e.g. $0.0005 per 1k input, $0.0015 per 1k output)
                    est_cost = (est_prompt_tokens / 1000 * 0.0005) + (est_completion_tokens / 1000 * 0.0015)
                    m_cost.inc(est_cost)
                    
                    st.subheader("📖 Recommendations")
                    st.write(result)
                    
                    # Optional: Show the user the estimated cost for transparency!
                    st.caption(f"⚙️ Generated in {est_prompt_tokens + est_completion_tokens} tokens (Est. Cost: ${est_cost:.5f})")
                    
                except Exception as e:
                    m_errors.inc()
                    logger.error(f"Error in recommendation pipeline: {e}")
                    st.error("Oops! Our AI librarian encountered an error. Please try again.")
    else:
        st.warning("Please enter a query.")


# ---- 7. USER FEEDBACK UI ----
st.divider()
st.write("How was this recommendation?")
col1, col2, col3 = st.columns([1, 1, 8])

with col1:
    if st.button("👍"):
        m_feedback.labels(sentiment='positive').inc()
        st.toast("Thanks for the feedback!")
with col2:
    if st.button("👎"):
        m_feedback.labels(sentiment='negative').inc()
        st.toast("We'll do better next time!")
