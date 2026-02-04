from dotenv import load_dotenv
from utils.logger import get_logger
from utils.custom_exception import CustomException

from src.dataloader import BookDataLoader
from src.vectorising import BookVectoriser

load_dotenv()
logger = get_logger(__name__)


def main():
    try:
        logger.info("Starting book vector store build pipeline...")

        # 1. Load and preprocess data
        loader = BookDataLoader(
            input_csv="Novels_Data/book_details.csv",
            output_csv="Novels_Data/book_processed.csv"
        )
        loader.load_and_process()

        logger.info("Book data loaded and processed successfully")

        # 2. Build and persist vector store
        vectoriser = BookVectoriser(
            csv_path="Novels_Data/book_processed.csv",
            persist_directory="Vector_Chroma"
        )
        vectoriser.vectorise()

        logger.info("Vector store built and persisted successfully")

    except Exception as e:
        logger.error(f"Pipeline build failed: {str(e)}")
        raise CustomException("Error during vector store build pipeline", e)


if __name__ == "__main__":
    main()
