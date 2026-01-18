import base64
import logging
import tempfile
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config.settings import settings
from utils.logger import configure_logging

configure_logging()
LOGGER = logging.getLogger("pdf_processor")
LOGGER.setLevel(logging.INFO)

SEPARATORS = [
    "\n\n",
    "\n",
    "\uff0e",  # Fullwidth full stop
    "\u3002",  # Ideographic full stop
    "\uff0c",  # Fullwidth comma
    "\u3001",  # Ideographic comma
    ".",
    ",",
    " ",
    "\u200b",  # Zero-width space
    "",
]


class PDFProcessor:
    """PDF Processor for RAG."""

    def save_pdf(self, base64_data: str) -> Path:
        """Save PDF to temporary file."""
        if base64_data.startswith("data:"):
            base64_data = base64_data.split(",", 1)[1]

        pdf_bytes = base64.b64decode(base64_data)

        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp.write(pdf_bytes)
            return Path(tmp.name)

    def load(self, file_path: Path) -> list[Document]:
        """Loads PDF and returns list of documents."""
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        LOGGER.info(f"Loaded {len(docs)} pages.")
        return docs

    def chunk(self, docs: list[Document]) -> list[Document]:
        """Chunk PDF into smaller documents."""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            separators=SEPARATORS,
        )
        chunks = text_splitter.split_documents(docs)
        LOGGER.info(f"Split PDF into {len(chunks)} text chunks.")
        return chunks

    def load_and_chunk(self, file_path: Path) -> list[Document]:
        """Load PDF and split it into chunks."""
        return self.chunk(self.load(file_path))
