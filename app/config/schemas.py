"""Request and response schemas."""

from pydantic import BaseModel


class PDFInput(BaseModel):
    """User input for PDF ingestion."""

    content_type: str  # "application/pdf"
    data: str  # base64 encoded file data


class RetrieveInput(BaseModel):
    """User input for retrieval."""

    query_texts: list[str]


class RetrieveOutput(BaseModel):
    """Output for retrieval."""

    query_contexts: list[dict[str, str | list[str]]]
