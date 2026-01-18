import logging

from fastapi import APIRouter
from fastapi.responses import Response

router = APIRouter()
LOGGER = logging.getLogger("service")
LOGGER.setLevel(logging.INFO)


@router.get("/health_check", include_in_schema=False)
async def health_check() -> Response:
    """Health check endpoint."""
    return Response(content="OK", status_code=200)
