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


class SummarizeInput(BaseModel):
    """User input for summarization."""

    content_type: str  # "application/pdf" or "text/plain"
    data: str  # base64 encoded file data or text


class Slide(BaseModel):
    """Slide with title, subtitle, and content blocks."""

    slide_num: int
    title: str | None = None
    subtitle: str | None = None
    content: list[dict[str, str | list[dict[str, str]]]]


class SummarizeOutput(BaseModel):
    """Output for summarization.
    Example:
    ```json
        {
          "slides": [
          {
            "slide_num": 1,
            "title": "Title",
            "subtitle": "Subtitle",
            "content": [
              {
                "type": "text",
                "content": "Some text"
              },
              {
                "type": "bullets",
                "bullets": [
                  { "id": "1", "text": "Point one" },
                  { "id": "2", "text": "Point two" }
                ]
              }
          }
        ]
        }
    ```
    """

    slides: list[Slide]
