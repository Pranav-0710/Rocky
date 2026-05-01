from unittest.mock import AsyncMock, Mock, patch

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.anyio
async def test_chat_returns_200_and_expected_shape() -> None:
    with patch("app.services.llm.get_reply", return_value="Mocked Rocky reply") as mock_llm, \
         patch("app.services.vector_db.query_memory", return_value="") as mock_memory:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://testserver"
        ) as client:
            response = await client.post(
                "/api/chat",
                json={"message": "hello", "history": []},
            )

    assert response.status_code == 200
    payload = response.json()
    assert set(payload.keys()) == {"reply", "actions"}
    assert payload["reply"] == "Mocked Rocky reply"
    assert isinstance(payload["actions"], list)
    assert payload["actions"] == []
    mock_llm.assert_called_once_with("hello", context="", history=[])
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


@pytest.mark.anyio
async def test_memory_debug_returns_collection_stats_and_sample() -> None:
    fake_client = Mock()
    fake_client.count.return_value = Mock(count=7)

    with patch("app.routes.memory.get_client", return_value=fake_client), \
         patch("app.routes.memory.query_memory", return_value="best friend: Sam"):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://testserver"
        ) as client:
            response = await client.get("/api/memory/debug")

    assert response.status_code == 200
    payload = response.json()
    assert payload["collection"] == "rocky_memory"
    assert payload["total_points"] == 7
    assert payload["sample_query"] == "best friend"
    assert payload["sample_result"] == "best friend: Sam"
    assert payload["embedder_status"] == "ok"
