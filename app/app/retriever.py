import asyncio
import logging

from config.schemas import RetrieveOutput
from core.embedder import EmbeddingClient
from memory.milvus_manager import MilvusManager
from utils.logger import configure_logging

configure_logging()
LOGGER = logging.getLogger("retriever")
LOGGER.setLevel(logging.INFO)


class Retriever:
    """Milvus cosine retriever."""

    def __init__(
        self, milvus_manager: MilvusManager, embedder: EmbeddingClient = None, top_k: int = 5
    ):
        self.embedder = embedder
        self.top_k = top_k
        self.milvus_manager = milvus_manager

    async def aretrieve(self, query_texts: list[str]) -> dict:
        """Retrieve relevant documents for a query."""
        results = await self.milvus_manager.asearch(query_texts, self.embedder, limit=self.top_k)
        query_contexts: list[dict[str, str | list[str]]] = []
        for i, result in enumerate(results):
            contexts = [context["entity"]["text_content"] for context in result]
            query_contexts.append({"query": query_texts[i], "contexts": contexts})
        return RetrieveOutput(query_contexts=query_contexts).model_dump()


if __name__ == "__main__":
    retriever = Retriever(milvus_manager=MilvusManager(), embedder=EmbeddingClient())
    print(
        asyncio.run(
            retriever.aretrieve(
                [
                    "What is the main idea of the document?",
                    "What is the conclusion of the document?",
                ]
            )
        )
    )
