import logging
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import Response

from app.dependencies import get_ingester
from app.ingester import Ingester
from config.schemas import PDFInput

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
