"""Dependency injection for singleton instances."""

from functools import lru_cache

from app.ingester import Ingester
from app.retriever import Retriever
from app.summarizer import Summarizer
from core.embedder import EmbeddingClient
from core.llm import LLMClient
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


@lru_cache
def get_retriever() -> Retriever:
    """Get or create the singleton Retriever instance.

    :return: The singleton Retriever instance.
    """
    return Retriever(get_milvus_manager(), get_embedding_client())


@lru_cache
def get_llm_client() -> LLMClient:
    """Get or create the singleton LLMClient instance.

    :return: The singleton LLMClient instance.
    """
    return LLMClient()


@lru_cache
def get_summarizer() -> Summarizer:
    """Get or create the singleton Summarizer instance.

    :return: The singleton Summarizer instance.
    """
    return Summarizer(get_llm_client())
