from typing import AsyncGenerator

import pytest
import respx
from httpx import Response

from funstat_api import ApiError, AsyncFunstatClient, ResolveError
from funstat_api.helpers import DEFAULT_BASE_URL


@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncFunstatClient, None]:
    client = AsyncFunstatClient("test_token")
    yield client
    await client.close()


@pytest.mark.asyncio
async def test_ping(async_client: AsyncFunstatClient) -> None:
    with respx.mock:
        respx.get(f"{DEFAULT_BASE_URL}/users/resolve_username").mock(
            return_value=Response(
                200,
                json={
                    "success": True,
                    "tech": {"request_cost": 1.0, "current_ballance": 100.0, "request_duration": "0.01s"},
                    "data": [],
                },
            )
        )
        res = await async_client.ping()
        assert res is not None
        assert res.request_ping == "0.01s"


@pytest.mark.asyncio
async def test_resolve_user_success(async_client: AsyncFunstatClient) -> None:
    with respx.mock:
        respx.get(f"{DEFAULT_BASE_URL}/users/resolve_username?name=durov").mock(
            return_value=Response(
                200,
                json={
                    "success": True,
                    "tech": {"request_cost": 1.0, "current_ballance": 100.0, "request_duration": "0.01s"},
                    "data": [{"id": 12345, "username": "durov", "is_active": True, "is_bot": False}],
                },
            )
        )
        user_id = await async_client._resolve_user("durov")
        assert user_id == 12345


@pytest.mark.asyncio
async def test_resolve_user_error(async_client: AsyncFunstatClient) -> None:
    with respx.mock:
        respx.get(f"{DEFAULT_BASE_URL}/users/resolve_username?name=unknown").mock(
            return_value=Response(
                200,
                json={
                    "success": True,
                    "tech": {"request_cost": 1.0, "current_ballance": 100.0, "request_duration": "0.01s"},
                    "data": [],
                },
            )
        )
        with pytest.raises(ResolveError):
            await async_client._resolve_user("unknown")


@pytest.mark.asyncio
async def test_api_error(async_client: AsyncFunstatClient) -> None:
    with respx.mock:
        respx.get(f"{DEFAULT_BASE_URL}/users/12345/stats").mock(return_value=Response(404))
        with pytest.raises(ApiError) as exc:
            await async_client.stats(12345)
        assert exc.value.status_code == 404
