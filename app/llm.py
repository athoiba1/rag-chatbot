from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from app.config import settings


SYSTEM_PROMPT = """You are a helpful AI assistant that answers questions based on the provided context.

Rules:
1. Only answer based on the provided context. If the context doesn't contain enough information, say so.
2. Be concise and direct.
3. Cite your sources when possible.
4. If asked about something not in the context, politely explain you can only answer based on the provided documents."""


class LLMClient:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.LLM_MODEL,
            temperature=settings.LLM_TEMPERATURE,
            max_tokens=settings.LLM_MAX_TOKENS,
            openai_api_key=settings.OPENAI_API_KEY,
        )

    def _format_context(self, documents: list) -> str:
        parts = []
        for i, doc in enumerate(documents, 1):
            source = doc.metadata.get("source", "Unknown")
            parts.append(f"[Source {i}: {source}]\n{doc.page_content}")
        return "\n\n---\n\n".join(parts)

    def generate_response(
        self,
        query: str,
        context_docs: list,
        chat_history: list[dict] | None = None,
    ) -> str:
        context = self._format_context(context_docs)

        messages = [SystemMessage(content=SYSTEM_PROMPT)]

        if chat_history:
            for msg in chat_history[-6:]:
                if msg["role"] == "user":
                    messages.append(HumanMessage(content=msg["content"]))
                else:
                    messages.append(AIMessage(content=msg["content"]))

        user_message = f"""Context:
{context}

---

Question: {query}

Answer based on the context above:"""

        messages.append(HumanMessage(content=user_message))

        response = self.llm.invoke(messages)
        return response.content
