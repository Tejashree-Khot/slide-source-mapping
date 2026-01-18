import logging

from langchain_core.documents import Document

from config.schemas import PDFInput
from core.embedder import EmbeddingClient
from memory.milvus_manager import MilvusManager
from utils.logger import configure_logging
from utils.pdf_processor import PDFProcessor

configure_logging()
LOGGER = logging.getLogger("ingester")
LOGGER.setLevel(logging.INFO)


class Ingester:
    """Ingester."""

    def __init__(self, milvus_manager: MilvusManager, embedder: EmbeddingClient = None):
        self.embedder = embedder
        self.milvus_manager = milvus_manager
        self.pdf_processor = PDFProcessor()

    async def aingest(self, payload: PDFInput):
        """Ingest sources for a bullet point."""
        if payload.content_type == "application/pdf":
            tmp_path = self.pdf_processor.save_pdf(payload.data)
            documents = self.pdf_processor.load_and_chunk(tmp_path)
        else:
            documents = [Document(page_content=payload.data, metadata={"page": 0})]

        await self.milvus_manager.insert_chunks(documents, self.embedder)
        LOGGER.info("Ingested sources successfully.")
