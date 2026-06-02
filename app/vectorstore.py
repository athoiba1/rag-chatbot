from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from app.config import settings


class VectorStore:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            model=settings.EMBEDDING_MODEL,
            dimensions=settings.EMBEDDING_DIMENSIONS,
            openai_api_key=settings.OPENAI_API_KEY,
        )
        self._store = None

    @property
    def store(self) -> Chroma:
        if self._store is None:
            self._store = Chroma(
                collection_name="rag_chatbot",
                embedding_function=self.embeddings,
                persist_directory=str(settings.VECTORSTORE_DIR),
            )
        return self._store

    def add_documents(self, documents: list[Document]) -> list[str]:
        return self.store.add_documents(documents)

    def similarity_search(self, query: str, k: int = None) -> list[Document]:
        k = k or settings.TOP_K
        return self.store.similarity_search(query, k=k)

    def similarity_search_with_score(self, query: str, k: int = None):
        k = k or settings.TOP_K
        return self.store.similarity_search_with_score(query, k=k)

    def delete_collection(self):
        self.store.delete_collection()
        self._store = None

    def get_stats(self) -> dict:
        collection = self.store._collection
        return {
            "total_chunks": collection.count(),
            "collection_name": "rag_chatbot",
        }
