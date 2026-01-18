"""Request and response schemas."""

from pydantic import BaseModel


class PDFInput(BaseModel):
    """User input for PDF ingestion."""

    content_type: str  # "application/pdf"
    data: str  # base64 encoded file data
