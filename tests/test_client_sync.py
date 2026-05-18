import pytest
import requests_mock

from funstat_api import ApiError, FunstatClient, ResolveError
from funstat_api.helpers import DEFAULT_BASE_URL


@pytest.fixture
def client() -> FunstatClient:
    return FunstatClient("test_token")


def test_ping(client: FunstatClient) -> None:
    with requests_mock.Mocker() as m:
        m.get(
            f"{DEFAULT_BASE_URL}/users/resolve_username?name=q",
            json={
                "success": True,
                "tech": {"request_cost": 1.0, "current_ballance": 100.0, "request_duration": "0.01s"},
                "data": [{"id": 1, "is_active": True, "is_bot": False}],
            },
        )
        res = client.ping()
        assert res is not None
        assert res.request_ping == "0.01s"
        assert res.responce_ping >= 0


def test_resolve_user_success(client: FunstatClient) -> None:
    with requests_mock.Mocker() as m:
        m.get(
            f"{DEFAULT_BASE_URL}/users/resolve_username?name=durov",
            json={
                "success": True,
                "tech": {"request_cost": 1.0, "current_ballance": 100.0, "request_duration": "0.01s"},
                "data": [{"id": 12345, "username": "durov", "is_active": True, "is_bot": False}],
            },
        )
        user_id = client._resolve_user("durov")
        assert user_id == 12345


def test_resolve_user_error(client: FunstatClient) -> None:
    with requests_mock.Mocker() as m:
        m.get(
            f"{DEFAULT_BASE_URL}/users/resolve_username?name=unknown_user",
            json={
                "success": True,
                "tech": {"request_cost": 1.0, "current_ballance": 100.0, "request_duration": "0.01s"},
                "data": [],
            },
        )
        with pytest.raises(ResolveError):
            client._resolve_user("unknown_user")


def test_api_error(client: FunstatClient) -> None:
    with requests_mock.Mocker() as m:
        m.get(
            f"{DEFAULT_BASE_URL}/users/12345/stats",
            status_code=500,
        )
        with pytest.raises(ApiError) as exc:
            client.stats(12345)
        assert exc.value.status_code == 500


def test_get_balance(client: FunstatClient) -> None:
    with requests_mock.Mocker() as m:
        m.get(
            f"{DEFAULT_BASE_URL}/users/resolve_username?name=q",
            json={
                "success": True,
                "tech": {"request_cost": 0.0, "current_ballance": 99.5, "request_duration": "0.01s"},
                "data": [],
            },
        )
        res = client.get_balance()
        assert res is not None
        assert res.current_ballance == 99.5
