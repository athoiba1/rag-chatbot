from dataclasses import dataclass, field
from app.vectorstore import VectorStore
from app.llm import LLMClient


@dataclass
class RetrievalResult:
    answer: str
    sources: list[dict] = field(default_factory=list)
    scores: list[float] = field(default_factory=list)


class Retriever:
    def __init__(self):
        self.vectorstore = VectorStore()
        self.llm = LLMClient()

    def retrieve(self, query: str, chat_history: list[dict] | None = None) -> RetrievalResult:
        results_with_scores = self.vectorstore.similarity_search_with_score(query)

        documents = [doc for doc, _ in results_with_scores]
        scores = [score for _, score in results_with_scores]

        answer = self.llm.generate_response(query, documents, chat_history)

        sources = []
        seen = set()
        for doc in documents:
            source = doc.metadata.get("source", "Unknown")
            if source not in seen:
                seen.add(source)
                sources.append({
                    "source": source,
                    "page": doc.metadata.get("page", None),
                    "preview": doc.page_content[:200] + "...",
                })

        return RetrievalResult(
            answer=answer,
            sources=sources,
            scores=scores,
        )
