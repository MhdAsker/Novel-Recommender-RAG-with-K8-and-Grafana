from src.vectorising import BookVectoriser
from src.recommender import BookRecommender
from config.config import GROQ_API_KEY, MODEL_NAME
from utils.logger import get_logger
from utils.custom_exception import CustomException

logger = get_logger(__name__)


class BookRecommendationPipeline:
    def __init__(self, persist_dir="Vector_Chroma"):
        try:
            logger.info("Initializing Book Recommendation Pipeline")

            vectoriser = BookVectoriser(
                csv_path=None,
                persist_directory=persist_dir
            )
            vector_store = vectoriser.load_vector_store()

            retriever = vector_store.as_retriever(search_kwargs={"k": 5})

            self.recommender = BookRecommender(
                retriever=retriever,
                api_key=GROQ_API_KEY,
                model_name=MODEL_NAME
            )

            logger.info("Book Recommendation Pipeline initialized successfully")

        except Exception as e:
            logger.error(f"Pipeline initialization failed: {str(e)}")
            raise CustomException("Pipeline initialization error", e)

    def recommend(self, query: str) -> str:
        try:
            return self.recommender.get_recommendation(query)
        except Exception as e:
            logger.error(f"Recommendation failed: {str(e)}")
            raise CustomException("Recommendation error", e)
