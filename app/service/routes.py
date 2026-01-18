import logging
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, Response

from app.dependencies import get_ingester, get_retriever, get_summarizer
from app.ingester import Ingester
from app.retriever import Retriever
from app.summarizer import Summarizer
from config.schemas import PDFInput, RetrieveInput, RetrieveOutput, SummarizeInput, SummarizeOutput

router = APIRouter()
LOGGER = logging.getLogger("service")
LOGGER.setLevel(logging.INFO)


@router.get("/health_check", include_in_schema=False)
async def health_check() -> Response:
    """Health check endpoint."""
    return Response(content="OK", status_code=200)


@router.post("/ingest")
async def ingest(
    request: PDFInput, ingester: Annotated[Ingester, Depends(get_ingester)]
) -> Response:
    """Ingest sources for a bullet point."""
    await ingester.aingest(request)
    return Response(content="OK", status_code=200)


@router.post("/retrieve", response_model=RetrieveOutput)
async def retrieve(
    request: RetrieveInput, retriever: Annotated[Retriever, Depends(get_retriever)]
) -> JSONResponse:
    """Retrieve sources for a bullet point."""
    result = await retriever.aretrieve(request.query_texts)
    return JSONResponse(content=result)


@router.post("/summarize", response_model=SummarizeOutput)
async def summarize(
    request: SummarizeInput, summarizer: Annotated[Summarizer, Depends(get_summarizer)]
) -> JSONResponse:
    """Generate slide summaries from user input."""
    result = await summarizer.summarize(request)
    return JSONResponse(content=result)
