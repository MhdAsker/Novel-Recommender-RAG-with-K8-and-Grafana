from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_huggingface import HuggingFaceEmbeddings


class BookVectoriser:
    def __init__(self, csv_path: str, persist_directory: str = "Vector_Chroma"):
        self.csv_path = csv_path
        self.persist_directory = persist_directory
        self.embedding = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

    def vectorise(self) -> Chroma:
        loader = CSVLoader(file_path=self.csv_path, encoding="utf-8")
        documents = loader.load()

        splitter = RecursiveCharacterTextSplitter(chunk_size=1000)
        docs = splitter.split_documents(documents)

        vector_store = Chroma.from_documents(
            documents=docs,
            embedding=self.embedding,
            persist_directory=self.persist_directory
        )
        vector_store.persist()
        return vector_store

    def load_vector_store(self) -> Chroma:
        return Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embedding
        )
