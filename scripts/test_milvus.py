"""Test Milvus."""

import asyncio
import sys
from pathlib import Path

from dotenv import load_dotenv

APP_PATH = Path(__file__).parent.parent / "app"
load_dotenv(APP_PATH / ".env")
sys.path.append(str(APP_PATH))

from app.core.embedder import EmbeddingClient
from app.memory.milvus_manager import MilvusManager, create_milvus_manager
from app.utils.pdf_processor import PDFProcessor


async def execute_similarity_search(
    query: str, embedding_client: EmbeddingClient, milvus_manager: MilvusManager
):
    """Execute similarity search."""
    results = await milvus_manager.asearch([query], embedding_client)
    for search_hits in results:
        for search_hit in search_hits:
            score = search_hit["distance"]
            page_number = search_hit["entity"]["page_number"]
            content = search_hit["entity"]["text_content"][:150].replace("\n", " ")
            print(f"[Score: {score:.4f} | Page: {page_number}] - Text: {content}...")


async def ingest_pdf(
    pdf_path: Path, embedding_client: EmbeddingClient, milvus_manager: MilvusManager
):
    """Ingest PDF into Milvus."""
    pdf_processor = PDFProcessor()
    chunks = pdf_processor.load_and_chunk(Path(pdf_path))

    # Insert chunks into Milvus
    print("Inserting chunks into Milvus")
    await milvus_manager.insert_chunks(chunks, embedding_client)
    print("PDF ingested successfully")


def main():
    embedding_client = EmbeddingClient()
    try:
        milvus_manager = create_milvus_manager()
    except ConnectionError as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    sample_pdf_path = Path(__file__).parent.parent / "assets" / "sample.pdf"
    asyncio.run(ingest_pdf(sample_pdf_path, embedding_client, milvus_manager))

    query = "What is the Milvus?"
    print(f"Testing Search - '{query}'")
    asyncio.run(execute_similarity_search(query, embedding_client, milvus_manager))


if __name__ == "__main__":
    main()
