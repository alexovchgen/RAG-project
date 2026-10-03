import logging

from app.core.config import settings
from app.core.logging import setup_logging

setup_logging(settings.log_level)
logger = logging.getLogger(__name__)


from fastapi import FastAPI

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)

@app.get("/health")
async def health_check():
    logger.debug("health check details: status=ok")
    logger.info("health check called")
    return {"status": "ok"}
