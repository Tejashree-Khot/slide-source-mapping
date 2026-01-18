import logging

from langchain_core.documents import Document
from pymilvus import DataType, MilvusClient

from config.settings import settings
from core.embedder import EmbeddingClient
from utils.logger import configure_logging

configure_logging()
LOGGER = logging.getLogger("milvus_manager")
LOGGER.setLevel(logging.INFO)


class MilvusManager:
    def __init__(self):
        self.client = MilvusClient(uri=settings.MILVUS_URI, token=settings.MILVUS_TOKEN)
        self.batch_size = settings.MILVUS_BATCH_SIZE
        self.collection_name = settings.MILVUS_COLLECTION_NAME
        self.embedding_dim = settings.MILVUS_EMBEDDING_DIM
        LOGGER.info(f"Connected to Milvus at {settings.MILVUS_URI}")

    def create_collection(self, drop_old=True):
        """Defines schema and creates the collection."""
        if drop_old and self.client.has_collection(self.collection_name):
            self.client.drop_collection(self.collection_name)
            LOGGER.info(f"Dropped existing collection: {self.collection_name}")

        LOGGER.info("Creating Schema")
        schema = self.client.create_schema(auto_id=True, enable_dynamic_field=False)

        # Schema Definition
        schema.add_field("id", DataType.INT64, is_primary=True)
        schema.add_field("vector", DataType.FLOAT_VECTOR, dim=self.embedding_dim)
        schema.add_field("text_content", DataType.VARCHAR, max_length=65535)
        schema.add_field("page_number", DataType.INT64)

        index_params = self.client.prepare_index_params()
        index_params.add_index(
            field_name="vector", metric_type="COSINE", index_type="IVF_FLAT", params={"nlist": 128}
        )

        self.client.create_collection(
            collection_name=self.collection_name, schema=schema, index_params=index_params
        )
        LOGGER.info(f"Collection '{self.collection_name}' created successfully.")

    async def insert_chunks(self, chunks: list[Document], embedding_client: EmbeddingClient):
        """Embeds text chunks and inserts them into Milvus in batches."""
        total_chunks = len(chunks)
        # split chunks into batches
        batches = [chunks[i : i + self.batch_size] for i in range(0, len(chunks), self.batch_size)]

        LOGGER.info("Starting Insertion")
        for i, batch in enumerate(batches):
            texts = [chunk.page_content for chunk in batch]

            vectors = await embedding_client.embed_document(texts)

            data_rows = []
            for j, vector in enumerate(vectors):
                data_rows.append(
                    {
                        "vector": vector,
                        "text_content": texts[j],
                        "page_number": batch[j].metadata.get("page", 0),
                    }
                )

            self.client.insert(self.collection_name, data_rows)
            LOGGER.info(f"Inserted batch {i + 1}/{total_chunks}")

    async def asearch(
        self, query_texts: list[str], embedding_model: EmbeddingClient, limit: int = 3
    ):
        """Performs a semantic search."""
        query_vectors = await embedding_model.embed_document(query_texts)

        return self.client.search(
            collection_name=self.collection_name,
            data=query_vectors,
            limit=limit,
            output_fields=["text_content", "page_number"],
        )


def create_milvus_manager() -> MilvusManager:
    """Create a Milvus manager instance."""
    manager = MilvusManager()
    # Only create collection if it doesn't exist
    if not manager.client.has_collection(manager.collection_name):
        LOGGER.info(f"Collection '{manager.collection_name}' does not exist. Creating...")
        manager.create_collection(drop_old=True)
    return manager
