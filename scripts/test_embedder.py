"""Test Embedder."""

import asyncio
import sys
from pathlib import Path

from dotenv import load_dotenv

APP_PATH = Path(__file__).parent.parent / "app"
load_dotenv(APP_PATH / ".env")
sys.path.append(str(APP_PATH))

from core.embedder import EmbeddingClient


def main():
    embedding_client = EmbeddingClient()
    embeddings = asyncio.run(embedding_client.embed_document(["What is the Milvus?"]))
    print(embeddings)


if __name__ == "__main__":
    main()
