from unittest.mock import AsyncMock, patch

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.anyio
async def test_chat_returns_200_and_expected_shape() -> None:
    with patch("app.routes.chat.get_reply", return_value="Mocked Rocky reply") as mock_llm, \
         patch("app.routes.chat.query_memory", return_value="") as mock_memory:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://testserver"
        ) as client:
            response = await client.post("/api/chat", json={"message": "hello"})

    assert response.status_code == 200
    payload = response.json()
    assert set(payload.keys()) == {"reply", "actions"}
    assert payload["reply"] == "Mocked Rocky reply"
    assert isinstance(payload["actions"], list)
    assert payload["actions"] == []
    mock_llm.assert_called_once_with("hello", context="")
    mock_memory.assert_called_once_with("hello")


@pytest.mark.anyio
async def test_memory_upload_returns_success_with_mocked_vector_store() -> None:
    mocked_store = AsyncMock(return_value=2)
    with patch("app.routes.memory.store_file", new=mocked_store):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://testserver"
        ) as client:
            response = await client.post(
                "/api/memory/upload",
                files={"file": ("memory.txt", b"mock content", "text/plain")},
            )

    assert response.status_code == 200
    assert response.json() == {"status": "success", "chunks_added": 2}
    mocked_store.assert_awaited_once()
