import sys
import os
import streamlit as st
from dotenv import load_dotenv

# ---- Add project root to path ----
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)
# ---------------------------------

from pipeline.recommendation_pipeline import BookRecommendationPipeline
from utils.logger import get_logger
from utils.custom_exception import CustomException

load_dotenv()
logger = get_logger(__name__)

st.set_page_config(page_title="📚 Book Recommender", layout="centered")

st.title("📚 AI Book Recommendation System")
st.write("Describe what kind of books you want to read.")

@st.cache_resource
def load_pipeline():
    return BookRecommendationPipeline()

pipeline = load_pipeline()

query = st.text_input(
    "Your preference",
    placeholder="e.g. dystopian novels with strong female protagonists"
)

if st.button("Get Recommendations"):
    if query.strip():
        with st.spinner("Finding recommendations..."):
            result = pipeline.recommend(query)
        st.subheader("📖 Recommendations")
        st.write(result)
    else:
        st.warning("Please enter a query.")
