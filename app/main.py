import logging

from app.core.config import settings
from app.core.logging import setup_logging

setup_logging(settings.log_level)
logger = logging.getLogger(__name__)

import asyncio
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, field_validator


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=200)


class Task(BaseModel):
    id: int
    title: str
    description: str
    done: bool = False


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=200)
    done: bool | None = None


tasks: dict[int, Task] = {}
next_id = 1



@app.get("/health")
async def health_check():
    logger.debug("health check details: status=ok")
    logger.info("health check called")
    return {"status": "ok"}
