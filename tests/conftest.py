from unittest.mock import MagicMock, patch

import pytest_asyncio
from httpx import ASGITransport, AsyncClient

_mock_chain = MagicMock()
_mock_chain.invoke.return_value = "mocked answer"
_mock_retriever = MagicMock()
_mock_retriever.invoke.return_value = []

# Патч до import app.main: иначе lifespan / Gradio дернут настоящий Qdrant.
patch("app.rag.chain.build_rag_chain", return_value=(_mock_chain, _mock_retriever)).start()

from app.main import app  # noqa: E402


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as c:
        yield c
