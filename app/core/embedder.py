from langchain_google_genai import GoogleGenerativeAIEmbeddings

from config.settings import settings


class EmbeddingClient:
    """Embedding client."""

    def __init__(self):
        self.model = GoogleGenerativeAIEmbeddings(  # type: ignore[call-arg]
            model=settings.EMBEDDING_MODEL_NAME,
            google_api_key=settings.GEMINI_API_KEY.get_secret_value(),
        )

    async def embed_document(self, documents: list[str]) -> list[list[float]]:
        """Embed a document string."""
        return await self.model.aembed_documents(documents)
