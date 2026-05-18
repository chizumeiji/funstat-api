"""
Funstat API client — sync and async modes.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, cast

from .exceptions import ApiError, ResolveError, UserHiddenError
from .helpers import (
    DEFAULT_BASE_URL,
    _clean_username,
    _extract_tech,
    _normalise_stats_min,
    _wrap,
)
from .models import (
    ChatInfoExtResponse,
    GiftRelationResponse,
    GroupInfoResponse,
    GroupMemberResponse,
    NameUsageResponse,
    PingResult,
    ReputationResponse,
    ResolvedUserResponse,
    StickerInfoResponse,
    TechInfo,
    UCommonGroupInfoResponse,
    UserMsgPagedResponse,
    UserNameInfoResponse,
    UsernameUsageResponse,
    UserStatsMinResponse,
    UserStatsResponse,
    UsrChatInfoResponse,
    WhoWroteTextResponse,
)


@dataclass
class FunstatConfig:
    """Configuration for Funstat API clients."""

    base_url: str = DEFAULT_BASE_URL
    headers: dict[str, str] = field(default_factory=dict)


class FunstatClient:
    """Synchronous Funstat API client. Uses requests, no async/await needed.

    Example:
        fs = FunstatClient("mytoken")
        print(fs.stats("durov"))
        print(fs.get_group_members("https://t.me/mychat"))
    """

    def __init__(self, token: str, base_url: str = DEFAULT_BASE_URL) -> None:
        import requests as _requests

        self.token = token
        self.base_url = base_url.rstrip("/")
        self._session = _requests.Session()
        self._session.headers["Authorization"] = f"Bearer {token}"

    def close(self) -> None:
        """Close the underlying HTTP session."""
        self._session.close()

    def __enter__(self) -> FunstatClient:
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()

    def _get(self, path: str, **params: Any) -> dict[str, Any] | None:
        url = f"{self.base_url}/{path.lstrip('/')}"
        r = self._session.get(url, params=params or None)
        if r.status_code == 200:
            return cast(dict[str, Any], r.json())  # type: ignore[no-any-return]
        if r.status_code == 403:
            raise UserHiddenError(path)
        raise ApiError(r.status_code, path)

    # ── internal resolvers ────────────────────────────────────────────────────

    def _resolve_user(self, user: int | str) -> int:
        if isinstance(user, int):
            return user
        clean = _clean_username(str(user))
        if clean.lstrip("-").isdigit():
            return int(clean)
        result = self._get("users/resolve_username", name=clean)
        if result and result.get("data"):
            return cast(int, result["data"][0]["id"])
        raise ResolveError(f"User not found: {user!r}")

    def _resolve_group(self, group: int | str) -> int:
        if isinstance(group, int):
            return group
        clean = _clean_username(str(group))
        if clean.lstrip("-").isdigit():
            return int(clean)
        result = self._get("users/username_usage", username=clean)
        chats = ((result or {}).get("data") or {}).get("actualGroupsOrChannels") or []
        if chats:
            return cast(int, chats[0]["id"])
        raise ResolveError(f"Group not found: {group!r}")

    # ── public methods ────────────────────────────────────────────────────────

    def ping(self) -> PingResult | None:
        t0 = time.time()
        result = self._get("users/resolve_username", name="q")
        elapsed = time.time() - t0
        if result and "tech" in result:
            return PingResult(
                request_ping=result["tech"].get("request_duration", ""),
                responce_ping=elapsed,
            )
        return None

    def get_balance(self) -> TechInfo | None:
        return _extract_tech(self._get("users/resolve_username", name="q"))

    def resolve_username(self, username: str) -> ResolvedUserResponse | None:
        res = self._get("users/resolve_username", name=_clean_username(username))
        return _wrap(res, ResolvedUserResponse)  # type: ignore[return-value]

    def basic_info_by_id(self, ids: int | str | list[int | str]) -> ResolvedUserResponse | None:
        if not isinstance(ids, list):
            ids = [ids]
        resolved = [self._resolve_user(i) for i in ids]
        res = self._get("users/basic_info_by_id", id=resolved)
        return _wrap(res, ResolvedUserResponse)  # type: ignore[return-value]

    def stats_min(self, user: int | str) -> UserStatsMinResponse | None:
        return _normalise_stats_min(self._get(f"users/{self._resolve_user(user)}/stats_min"))

    def stats(self, user: int | str) -> UserStatsResponse | None:
        res = self._get(f"users/{self._resolve_user(user)}/stats")
        return _wrap(res, UserStatsResponse)  # type: ignore[return-value]

    def messages_count(self, user: int | str) -> int:
        res = self._get(f"users/{self._resolve_user(user)}/messages_count")
        return int(res) if res is not None else 0  # type: ignore[call-overload]

    def groups_count(self, user: int | str, only_msg: bool = False) -> int:
        res = self._get(f"users/{self._resolve_user(user)}/groups_count", onlyMsg=str(only_msg).lower())
        return int(res) if res is not None else 0  # type: ignore[call-overload]

    def get_messages(
        self,
        user: int | str,
        filter: str | None = None,
        group: int | str | None = None,
        limit: int = 20,
        page: int = 1,
    ) -> UserMsgPagedResponse | None:
        params: dict[str, Any] = {"page": page, "pageSize": limit}
        if filter:
            params["text_contains"] = filter
        if group is not None:
            params["group_id"] = self._resolve_group(group)
        res = self._get(f"users/{self._resolve_user(user)}/messages", **params)
        return _wrap(res, UserMsgPagedResponse)  # type: ignore[return-value]

    def get_chats(self, user: int | str) -> UsrChatInfoResponse | None:
        res = self._get(f"users/{self._resolve_user(user)}/groups")
        return _wrap(res, UsrChatInfoResponse)  # type: ignore[return-value]

    def get_names(self, user: int | str) -> UserNameInfoResponse | None:
        res = self._get(f"users/{self._resolve_user(user)}/names")
        return _wrap(res, UserNameInfoResponse)  # type: ignore[return-value]

    def get_usernames(self, user: int | str) -> UserNameInfoResponse | None:
        res = self._get(f"users/{self._resolve_user(user)}/usernames")
        return _wrap(res, UserNameInfoResponse)  # type: ignore[return-value]

    def rep(self, user: int | str) -> ReputationResponse | None:
        res = self._get("users/reputation", id=self._resolve_user(user))
        return _wrap(res, ReputationResponse)  # type: ignore[return-value]

    def common_groups(self, user: int | str) -> UCommonGroupInfoResponse | None:
        res = self._get(f"users/{self._resolve_user(user)}/common_groups_stat")
        return _wrap(res, UCommonGroupInfoResponse)  # type: ignore[return-value]

    def get_stickers(self, user: int | str) -> StickerInfoResponse | None:
        res = self._get(f"users/{self._resolve_user(user)}/stickers")
        return _wrap(res, StickerInfoResponse)  # type: ignore[return-value]

    def get_gifts(self, user: int | str, limit: int = 20, page: int = 1) -> GiftRelationResponse | None:
        res = self._get(f"users/{self._resolve_user(user)}/gifts_relation", page=page, pageSize=limit)
        return _wrap(res, GiftRelationResponse)  # type: ignore[return-value]

    def username_usage(self, username: str) -> UsernameUsageResponse | None:
        res = self._get("users/username_usage", username=_clean_username(username))
        return _wrap(res, UsernameUsageResponse)  # type: ignore[return-value]

    def common_groups_for_users(self, ids: list[int | str]) -> ChatInfoExtResponse | None:
        resolved = [self._resolve_user(i) for i in ids]
        res = self._get("groups/common_groups", id=resolved)
        return _wrap(res, ChatInfoExtResponse)  # type: ignore[return-value]

    def get_group_info(self, group: int | str) -> GroupInfoResponse | None:
        res = self._get(f"groups/{self._resolve_group(group)}")
        return _wrap(res, GroupInfoResponse)  # type: ignore[return-value]

    def get_group_members(self, group: int | str) -> GroupMemberResponse | None:
        res = self._get(f"groups/{self._resolve_group(group)}/members")
        return _wrap(res, GroupMemberResponse)  # type: ignore[return-value]

    def search_text(self, query: str, page: int = 1, page_size: int = 20) -> WhoWroteTextResponse | None:
        res = self._get("text/search", input=query, page=page, pageSize=page_size)
        return _wrap(res, WhoWroteTextResponse)  # type: ignore[return-value]


class AsyncFunstatClient:
    """Asynchronous Funstat API client. Uses httpx, all methods must be awaited.

    Example:
        fs = AsyncFunstatClient("mytoken")
        print(await fs.stats("durov"))
        print(await fs.get_group_members("https://t.me/mychat"))
    """

    def __init__(self, token: str, config: FunstatConfig | None = None, base_url: str | None = None) -> None:
        import httpx

        self.token = token

        # Backward compatibility with base_url kwarg
        if config is None:
            config = FunstatConfig(base_url=base_url or DEFAULT_BASE_URL)
        elif base_url:
            config.base_url = base_url

        self.config = config
        self.base_url = self.config.base_url.rstrip("/")

        headers = dict(self.config.headers)
        headers["Authorization"] = f"Bearer {token}"
        self._client = httpx.AsyncClient(headers=headers)

    async def close(self) -> None:
        """Close the underlying HTTP client and release connections."""
        await self._client.aclose()

    async def __aenter__(self) -> AsyncFunstatClient:
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.close()

    async def _get(self, path: str, **params: Any) -> dict[str, Any] | None:
        url = f"{self.base_url}/{path.lstrip('/')}"
        r = await self._client.get(url, params=params or None)
        if r.status_code == 200:
            return cast(dict[str, Any], r.json())  # type: ignore[no-any-return]
        if r.status_code == 403:
            raise UserHiddenError(path)
        raise ApiError(r.status_code, path)

    # ── internal resolvers ────────────────────────────────────────────────────

    async def _resolve_user(self, user: int | str) -> int:
        if isinstance(user, int):
            return user
        clean = _clean_username(str(user))
        if clean.lstrip("-").isdigit():
            return int(clean)
        result = await self._get("users/resolve_username", name=clean)
        if result and result.get("data"):
            return cast(int, result["data"][0]["id"])
        raise ResolveError(f"User not found: {user!r}")

    async def _resolve_group(self, group: int | str) -> int:
        if isinstance(group, int):
            return group
        clean = _clean_username(str(group))
        if clean.lstrip("-").isdigit():
            return int(clean)
        result = await self._get("users/username_usage", username=clean)
        chats = ((result or {}).get("data") or {}).get("actualGroupsOrChannels") or []
        if chats:
            return cast(int, chats[0]["id"])
        raise ResolveError(f"Group not found: {group!r}")

    # ── public methods ────────────────────────────────────────────────────────

    async def ping(self) -> PingResult | None:
        t0 = time.time()
        result = await self._get("users/resolve_username", name="q")
        elapsed = time.time() - t0
        if result and "tech" in result:
            return PingResult(
                request_ping=result["tech"].get("request_duration", ""),
                responce_ping=elapsed,
            )
        return None

    async def get_balance(self) -> TechInfo | None:
        return _extract_tech(await self._get("users/resolve_username", name="q"))

    async def resolve_username(self, username: str) -> ResolvedUserResponse | None:
        res = await self._get("users/resolve_username", name=_clean_username(username))
        return _wrap(res, ResolvedUserResponse)  # type: ignore[return-value]

    async def basic_info_by_id(self, ids: int | str | list[int | str]) -> ResolvedUserResponse | None:
        import asyncio

        if not isinstance(ids, list):
            ids = [ids]
        resolved = list(await asyncio.gather(*[self._resolve_user(i) for i in ids]))
        res = await self._get("users/basic_info_by_id", id=resolved)
        return _wrap(res, ResolvedUserResponse)  # type: ignore[return-value]

    async def stats_min(self, user: int | str) -> UserStatsMinResponse | None:
        return _normalise_stats_min(await self._get(f"users/{await self._resolve_user(user)}/stats_min"))

    async def stats(self, user: int | str) -> UserStatsResponse | None:
        res = await self._get(f"users/{await self._resolve_user(user)}/stats")
        return _wrap(res, UserStatsResponse)  # type: ignore[return-value]

    async def messages_count(self, user: int | str) -> int:
        res = await self._get(f"users/{await self._resolve_user(user)}/messages_count")
        return int(res) if res is not None else 0  # type: ignore[call-overload]

    async def groups_count(self, user: int | str, only_msg: bool = False) -> int:
        res = await self._get(f"users/{await self._resolve_user(user)}/groups_count", onlyMsg=str(only_msg).lower())
        return int(res) if res is not None else 0  # type: ignore[call-overload]

    async def get_messages(
        self,
        user: int | str,
        filter: str | None = None,
        group: int | str | None = None,
        limit: int = 20,
        page: int = 1,
    ) -> UserMsgPagedResponse | None:
        params: dict[str, Any] = {"page": page, "pageSize": limit}
        if filter:
            params["text_contains"] = filter
        if group is not None:
            params["group_id"] = await self._resolve_group(group)
        res = await self._get(f"users/{await self._resolve_user(user)}/messages", **params)
        return _wrap(res, UserMsgPagedResponse)  # type: ignore[return-value]

    async def get_chats(self, user: int | str) -> UsrChatInfoResponse | None:
        res = await self._get(f"users/{await self._resolve_user(user)}/groups")
        return _wrap(res, UsrChatInfoResponse)  # type: ignore[return-value]

    async def get_names(self, user: int | str) -> UserNameInfoResponse | None:
        res = await self._get(f"users/{await self._resolve_user(user)}/names")
        return _wrap(res, UserNameInfoResponse)  # type: ignore[return-value]

    async def get_usernames(self, user: int | str) -> UserNameInfoResponse | None:
        res = await self._get(f"users/{await self._resolve_user(user)}/usernames")
        return _wrap(res, UserNameInfoResponse)  # type: ignore[return-value]

    async def rep(self, user: int | str) -> ReputationResponse | None:
        res = await self._get("users/reputation", id=await self._resolve_user(user))
        return _wrap(res, ReputationResponse)  # type: ignore[return-value]

    async def common_groups(self, user: int | str) -> UCommonGroupInfoResponse | None:
        res = await self._get(f"users/{await self._resolve_user(user)}/common_groups_stat")
        return _wrap(res, UCommonGroupInfoResponse)  # type: ignore[return-value]

    async def get_stickers(self, user: int | str) -> StickerInfoResponse | None:
        res = await self._get(f"users/{await self._resolve_user(user)}/stickers")
        return _wrap(res, StickerInfoResponse)  # type: ignore[return-value]

    async def get_gifts(self, user: int | str, limit: int = 20, page: int = 1) -> GiftRelationResponse | None:
        res = await self._get(f"users/{await self._resolve_user(user)}/gifts_relation", page=page, pageSize=limit)
        return _wrap(res, GiftRelationResponse)  # type: ignore[return-value]

    async def username_usage(self, username: str) -> UsernameUsageResponse | None:
        res = await self._get("users/username_usage", username=_clean_username(username))
        return _wrap(res, UsernameUsageResponse)  # type: ignore[return-value]

    async def name_usage(self, name: str, page: int = 1, page_size: int = 20) -> NameUsageResponse | None:
        res = await self._get("users/name_usage", name=name, page=page, pageSize=page_size)
        return _wrap(res, NameUsageResponse)  # type: ignore[return-value]

    async def common_groups_for_users(self, ids: list[int | str]) -> ChatInfoExtResponse | None:
        import asyncio

        resolved = list(await asyncio.gather(*[self._resolve_user(i) for i in ids]))
        res = await self._get("groups/common_groups", id=resolved)
        return _wrap(res, ChatInfoExtResponse)  # type: ignore[return-value]

    async def get_group_info(self, group: int | str) -> GroupInfoResponse | None:
        res = await self._get(f"groups/{await self._resolve_group(group)}")
        return _wrap(res, GroupInfoResponse)  # type: ignore[return-value]

    async def get_group_members(self, group: int | str) -> GroupMemberResponse | None:
        res = await self._get(f"groups/{await self._resolve_group(group)}/members")
        return _wrap(res, GroupMemberResponse)  # type: ignore[return-value]

    async def search_text(self, query: str, page: int = 1, page_size: int = 20) -> WhoWroteTextResponse | None:
        res = await self._get("text/search", input=query, page=page, pageSize=page_size)
        return _wrap(res, WhoWroteTextResponse)  # type: ignore[return-value]
