from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from src.prompt_templates import get_book_recommender_prompt


class BookRecommender:
    def __init__(self, retriever, api_key: str, model_name: str):
        # LLM
        self.llm = ChatGroq(
            api_key=api_key,
            model=model_name,
            temperature=0
        )

        # Prompt
        prompt_str = get_book_recommender_prompt().template
        self.prompt = ChatPromptTemplate.from_template(prompt_str)

        # Build LCEL chain
        self.chain = (
            {
                "context": retriever,
                "question": RunnablePassthrough()
            }
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    def get_recommendation(self, query: str) -> str:
        return self.chain.invoke(query)
