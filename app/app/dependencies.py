"""Dependency injection for singleton instances."""

from functools import lru_cache

from app.ingester import Ingester
from core.embedder import EmbeddingClient
from memory.milvus_manager import MilvusManager, create_milvus_manager


@lru_cache
def get_embedding_client() -> EmbeddingClient:
    """Get or create the singleton EmbeddingClient instance.

    :return: The singleton EmbeddingClient instance.
    """
    return EmbeddingClient()


@lru_cache
def get_milvus_manager() -> MilvusManager:
    """Get or create the singleton MilvusManager instance.

    :return: The singleton MilvusManager instance.
    """
    return create_milvus_manager()


@lru_cache
def get_ingester() -> Ingester:
    """Get or create the singleton Ingester instance.

    :return: The singleton Ingester instance.
    """
    return Ingester(get_milvus_manager(), get_embedding_client())
