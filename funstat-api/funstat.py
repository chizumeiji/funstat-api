"""
Funstat API client — sync and async modes.

Sync usage:
    from funstat_api import FunstatClient
    fs = FunstatClient("token")
    print(fs.stats("durov"))

Async usage:
    from funstat_api import AsyncFunstatClient
    fs = AsyncFunstatClient("token")
    print(await fs.stats("durov"))
"""

from __future__ import annotations
import re
import time
from abc import ABC, abstractmethod
from typing import Any, Optional
import logging
from pydantic import BaseModel, Field

logger = logging.getLogger("funstat")

# ─────────────────────────────────────────────────────────────────────────────
#  Exceptions
# ─────────────────────────────────────────────────────────────────────────────

class FunstatError(Exception):
    """Base exception for all funstat API errors."""


class ResolveError(FunstatError):
    """Raised when a username or group cannot be resolved to a numeric ID."""


class ApiError(FunstatError):
    """Raised when the API returns a non-200 status code."""

    def __init__(self, status_code: int, path: str) -> None:
        self.status_code = status_code
        self.path = path
        super().__init__(f"HTTP {status_code} for {path}")

# ─────────────────────────────────────────────────────────────────────────────
#  Models — shared
# ─────────────────────────────────────────────────────────────────────────────

class TechInfo(BaseModel):
    request_cost: float
    current_ballance: float
    request_duration: str

class Paging(BaseModel):
    total: int
    current_page: int = Field(alias="currentPage")
    page_size: int = Field(alias="pageSize")
    total_pages: int = Field(alias="totalPages")
    model_config = {"populate_by_name": True}

# ─────────────────────────────────────────────────────────────────────────────
#  Models — domain
# ─────────────────────────────────────────────────────────────────────────────

class ResolvedUser(BaseModel):
    id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool
    is_bot: bool
    has_premium: Optional[bool] = None

class ChatInfo(BaseModel):
    id: int
    title: str
    is_private: bool = Field(alias="isPrivate")
    username: Optional[str] = None
    model_config = {"populate_by_name": True}

class ChatInfoExt(BaseModel):
    id: int
    title: str
    is_private: bool = Field(alias="isPrivate")
    is_channel: bool = Field(alias="isChannel")
    username: Optional[str] = None
    link: Optional[str] = None
    model_config = {"populate_by_name": True}

class UserStatsMin(BaseModel):
    id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_bot: bool
    is_active: bool
    first_msg_date: Optional[str] = None
    last_msg_date: Optional[str] = None
    total_msg_count: int
    msg_in_groups_count: int
    adm_in_groups: int
    usernames_count: int
    names_count: int
    total_groups: int

class UserStats(UserStatsMin):
    is_cyrillic_primary: Optional[bool] = None
    lang_code: Optional[str] = None
    unique_percent: Optional[float] = None
    circle_count: int
    voice_count: int
    reply_percent: float
    media_percent: float
    link_percent: float
    favorite_chat: Optional[ChatInfo] = None
    media_usage: Optional[str] = None
    stars_val: Optional[int] = None
    personal_channel_id: Optional[int] = None
    gift_count: Optional[int] = None
    stars_level: Optional[int] = None
    birth_day: Optional[int] = None
    birth_month: Optional[int] = None
    birth_year: Optional[int] = None
    about: Optional[str] = None

class UserMsg(BaseModel):
    date: str
    message_id: int = Field(alias="messageId")
    reply_to_message_id: Optional[int] = Field(default=None, alias="replyToMessageId")
    media_code: Optional[int] = Field(default=None, alias="mediaCode")
    media_name: Optional[str] = Field(default=None, alias="mediaName")
    text: Optional[str] = None
    group: ChatInfo
    model_config = {"populate_by_name": True}

class UserNameInfo(BaseModel):
    name: str
    date_time: str

class UsrChatInfo(BaseModel):
    chat: ChatInfo
    last_message_id: int = Field(alias="lastMessageId")
    messages_count: int = Field(alias="messagesCount")
    last_message: Optional[str] = Field(default=None, alias="lastMessage")
    first_message: Optional[str] = Field(default=None, alias="firstMessage")
    is_admin: bool = Field(alias="isAdmin")
    is_left: bool = Field(alias="isLeft")
    model_config = {"populate_by_name": True}

class GroupMember(BaseModel):
    id: int
    username: Optional[str] = None
    name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_admin: Optional[bool] = None
    is_active: bool
    today_msg: int
    has_prem: Optional[bool] = None
    has_photo: bool
    dc_id: Optional[int] = None

class GiftRelationInfo(BaseModel):
    last_gift_date: Optional[str] = None
    from_user_id: int
    from_first_name: Optional[str] = None
    from_last_name: Optional[str] = None
    from_main_username: Optional[str] = Field(default=None, alias="from_mainUsername")
    from_is_active: bool
    to_user_id: int
    to_first_name: Optional[str] = None
    to_last_name: Optional[str] = None
    to_main_username: Optional[str] = Field(default=None, alias="to_mainUsername")
    to_is_active: bool
    model_config = {"populate_by_name": True}

class StickerInfo(BaseModel):
    sticker_set_id: int
    last_seen: str
    min_seen: str
    resolved: Optional[str] = None
    title: Optional[str] = None
    short_name: Optional[str] = None
    stickers_count: Optional[int] = None

class UCommonGroupInfo(BaseModel):
    user_id: int
    common_groups: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    is_user_active: bool

class UsernameUsageModel(BaseModel):
    actual_users: Optional[list[ResolvedUser]] = Field(default=None, alias="actualUsers")
    usage_by_users_in_the_past: Optional[list[ResolvedUser]] = Field(default=None, alias="usageByUsersInThePast")
    actual_groups_or_channels: Optional[list[ChatInfoExt]] = Field(default=None, alias="actualGroupsOrChannels")
    mention_by_channel_or_group_desc: Optional[list[ChatInfoExt]] = Field(default=None, alias="mentionByChannelOrGroupDesc")
    model_config = {"populate_by_name": True}

class WhoWroteText(BaseModel):
    message_id: int
    user_id: int
    date: str
    name: Optional[str] = None
    username: Optional[str] = None
    is_active: bool
    group: ChatInfoExt
    text: Optional[str] = None

class PingResult(BaseModel):
    request_ping: str
    responce_ping: float

# ─────────────────────────────────────────────────────────────────────────────
#  Models — API response wrappers
# ─────────────────────────────────────────────────────────────────────────────

class ResolvedUserResponse(BaseModel):
    success: bool
    tech: TechInfo
    data: Optional[list[ResolvedUser]] = None

class UserStatsMinResponse(BaseModel):
    success: bool
    tech: TechInfo
    data: Optional[UserStatsMin] = None

class UserStatsResponse(BaseModel):
    success: bool
    tech: TechInfo
    data: Optional[UserStats] = None

class UserMsgPagedResponse(BaseModel):
    success: bool
    tech: TechInfo
    paging: Paging
    data: Optional[list[UserMsg]] = None

class UserNameInfoResponse(BaseModel):
    success: bool
    tech: TechInfo
    data: Optional[list[UserNameInfo]] = None

class UsrChatInfoResponse(BaseModel):
    success: bool
    tech: TechInfo
    data: Optional[list[UsrChatInfo]] = None

class GroupMemberResponse(BaseModel):
    success: bool
    tech: TechInfo
    data: Optional[list[GroupMember]] = None

class GiftRelationResponse(BaseModel):
    success: bool
    tech: TechInfo
    data: Optional[list[GiftRelationInfo]] = None

class StickerInfoResponse(BaseModel):
    success: bool
    tech: TechInfo
    data: Optional[list[StickerInfo]] = None

class UCommonGroupInfoResponse(BaseModel):
    success: bool
    tech: TechInfo
    data: Optional[list[UCommonGroupInfo]] = None

class UsernameUsageResponse(BaseModel):
    success: bool
    tech: TechInfo
    data: Optional[UsernameUsageModel] = None

class ChatInfoExtResponse(BaseModel):
    success: bool
    tech: TechInfo
    data: Optional[list[ChatInfoExt]] = None

class WhoWroteTextPaged(BaseModel):
    total: int
    data: list[WhoWroteText]
    is_last_page: Optional[bool] = Field(default=None, alias="isLastPage")
    page_size: Optional[int] = Field(default=None, alias="pageSize")
    current_page: Optional[int] = Field(default=None, alias="currentPage")
    total_pages: Optional[int] = Field(default=None, alias="totalPages")
    is_sliding: Optional[bool] = Field(default=None, alias="isSliding")
    model_config = {"populate_by_name": True}

class WhoWroteTextResponse(BaseModel):
    success: bool
    tech: TechInfo
    data: Optional[WhoWroteTextPaged] = None

# ─────────────────────────────────────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────────────────────────────────────

BASE_URL = "/api/v1"

def _clean_username(username: str) -> str:
    username = username.strip()
    username = re.sub(r"^https?://t\.me/", "", username)
    username = re.sub(r"^t\.me/", "", username)
    return username.lstrip("@").split("/")[0].split("?")[0]

def _make_empty_tech() -> TechInfo:
    return TechInfo(request_cost=0, current_ballance=0, request_duration="")

def _wrap(payload: dict | None, model: type[BaseModel]) -> BaseModel | None:
    if payload is None:
        return None
    if not payload.get("success", True):
        logger.warning("API returned success=false: %s", payload)
    return model.model_validate(payload)

def _normalise_stats_min(payload: dict | None) -> UserStatsMinResponse | None:
    if payload is None:
        return None
    if "success" not in payload:
        return UserStatsMinResponse(
            success=True,
            tech=_make_empty_tech(),
            data=UserStatsMin.model_validate(payload),
        )
    return UserStatsMinResponse.model_validate(payload)

def _extract_tech(result: dict | None) -> TechInfo | None:
    if result and "tech" in result:
        return TechInfo.model_validate(result["tech"])
    return None

# ─────────────────────────────────────────────────────────────────────────────
#  Sync client
# ─────────────────────────────────────────────────────────────────────────────

class FunstatClient:
    """Synchronous Funstat API client. Uses requests, no async/await needed.

    Example:
        fs = FunstatClient("mytoken")
        print(fs.stats("durov"))
        print(fs.get_group_members("https://t.me/mychat"))
    """

    def __init__(self, token: str) -> None:
        import requests as _requests
        self.token = token
        self._session = _requests.Session()
        self._session.headers["Authorization"] = f"Bearer {token}"
    def close(self) -> None:
        """Close the underlying HTTP session."""
        self._session.close()

    def __enter__(self) -> "FunstatClient":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()

    def _get(self, path: str, **params: Any) -> dict | None:
        url = f"{BASE_URL}/{path.lstrip('/')}"
        r = self._session.get(url, params=params or None)
        if r.status_code == 200:
            return r.json()
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
            return result["data"][0]["id"]
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
            return chats[0]["id"]
        raise ResolveError(f"Group not found: {group!r}")

    # ── public methods ────────────────────────────────────────────────────────

    def ping(self) -> PingResult | None:
        t0 = time.time()
        result = self._get("users/resolve_username", name="q")
        elapsed = time.time() - t0
        if result and "tech" in result:
            return PingResult(request_ping=result["tech"].get("request_duration", ""), responce_ping=elapsed)
        return None

    def get_balance(self) -> TechInfo | None:
        return _extract_tech(self._get("users/resolve_username", name="q"))

    def resolve_username(self, username: str) -> ResolvedUserResponse | None:
        return _wrap(self._get("users/resolve_username", name=_clean_username(username)), ResolvedUserResponse)

    def basic_info_by_id(self, ids: int | str | list[int | str]) -> ResolvedUserResponse | None:
        if not isinstance(ids, list):
            ids = [ids]
        resolved = [self._resolve_user(i) for i in ids]
        return _wrap(self._get("users/basic_info_by_id", id=resolved), ResolvedUserResponse)

    def stats_min(self, user: int | str) -> UserStatsMinResponse | None:
        return _normalise_stats_min(self._get(f"users/{self._resolve_user(user)}/stats_min"))

    def stats(self, user: int | str) -> UserStatsResponse | None:
        return _wrap(self._get(f"users/{self._resolve_user(user)}/stats"), UserStatsResponse)

    def messages_count(self, user: int | str) -> int:
        return self._get(f"users/{self._resolve_user(user)}/messages_count") or 0

    def groups_count(self, user: int | str, only_msg: bool = False) -> int:
        return self._get(f"users/{self._resolve_user(user)}/groups_count", onlyMsg=str(only_msg).lower()) or 0

    def get_messages(self, user: int | str, filter: str | None = None, group: int | str | None = None, limit: int = 20, page: int = 1) -> UserMsgPagedResponse | None:
        params: dict = {"page": page, "pageSize": limit}
        if filter:
            params["text_contains"] = filter
        if group is not None:
            params["group_id"] = self._resolve_group(group)
        return _wrap(self._get(f"users/{self._resolve_user(user)}/messages", **params), UserMsgPagedResponse)

    def get_chats(self, user: int | str) -> UsrChatInfoResponse | None:
        return _wrap(self._get(f"users/{self._resolve_user(user)}/groups"), UsrChatInfoResponse)

    def get_names(self, user: int | str) -> UserNameInfoResponse | None:
        return _wrap(self._get(f"users/{self._resolve_user(user)}/names"), UserNameInfoResponse)

    def get_usernames(self, user: int | str) -> UserNameInfoResponse | None:
        return _wrap(self._get(f"users/{self._resolve_user(user)}/usernames"), UserNameInfoResponse)

    def rep(self, user: int | str) -> dict | None:
        return self._get("users/reputation", id=self._resolve_user(user))

    def common_groups(self, user: int | str) -> UCommonGroupInfoResponse | None:
        return _wrap(self._get(f"users/{self._resolve_user(user)}/common_groups_stat"), UCommonGroupInfoResponse)

    def get_stickers(self, user: int | str) -> StickerInfoResponse | None:
        return _wrap(self._get(f"users/{self._resolve_user(user)}/stickers"), StickerInfoResponse)

    def get_gifts(self, user: int | str, limit: int = 20, page: int = 1) -> GiftRelationResponse | None:
        return _wrap(self._get(f"users/{self._resolve_user(user)}/gifts_relation", page=page, pageSize=limit), GiftRelationResponse)

    def username_usage(self, username: str) -> UsernameUsageResponse | None:
        return _wrap(self._get("users/username_usage", username=_clean_username(username)), UsernameUsageResponse)

    def common_groups_for_users(self, ids: list[int | str]) -> ChatInfoExtResponse | None:
        resolved = [self._resolve_user(i) for i in ids]
        return _wrap(self._get("groups/common_groups", id=resolved), ChatInfoExtResponse)

    def get_group_info(self, group: int | str) -> dict | None:
        return self._get(f"groups/{self._resolve_group(group)}")

    def get_group_members(self, group: int | str) -> GroupMemberResponse | None:
        return _wrap(self._get(f"groups/{self._resolve_group(group)}/members"), GroupMemberResponse)

    def search_text(self, query: str, page: int = 1, page_size: int = 20) -> WhoWroteTextResponse | None:
        return _wrap(self._get("text/search", input=query, page=page, pageSize=page_size), WhoWroteTextResponse)

# ─────────────────────────────────────────────────────────────────────────────
#  Async client
# ─────────────────────────────────────────────────────────────────────────────

class AsyncFunstatClient:
    """Asynchronous Funstat API client. Uses httpx, all methods must be awaited.

    Example:
        fs = AsyncFunstatClient("mytoken")
        print(await fs.stats("durov"))
        print(await fs.get_group_members("https://t.me/mychat"))
    """

    def __init__(self, token: str) -> None:
        import httpx
        self.token = token
        self._client = httpx.AsyncClient(headers={"Authorization": f"Bearer {token}"})
    async def close(self) -> None:
        """Close the underlying HTTP client and release connections."""
        await self._client.aclose()

    async def __aenter__(self) -> "AsyncFunstatClient":
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.close()

    async def _get(self, path: str, **params: Any) -> dict | None:
        url = f"{BASE_URL}/{path.lstrip('/')}"
        r = await self._client.get(url, params=params or None)
        if r.status_code == 200:
            return r.json()
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
            return result["data"][0]["id"]
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
            return chats[0]["id"]
        raise ResolveError(f"Group not found: {group!r}")

    # ── public methods ────────────────────────────────────────────────────────

    async def ping(self) -> PingResult | None:
        t0 = time.time()
        result = await self._get("users/resolve_username", name="q")
        elapsed = time.time() - t0
        if result and "tech" in result:
            return PingResult(request_ping=result["tech"].get("request_duration", ""), responce_ping=elapsed)
        return None

    async def get_balance(self) -> TechInfo | None:
        return _extract_tech(await self._get("users/resolve_username", name="q"))

    async def resolve_username(self, username: str) -> ResolvedUserResponse | None:
        return _wrap(await self._get("users/resolve_username", name=_clean_username(username)), ResolvedUserResponse)

    async def basic_info_by_id(self, ids: int | str | list[int | str]) -> ResolvedUserResponse | None:
        import asyncio
        if not isinstance(ids, list):
            ids = [ids]
        resolved = list(await asyncio.gather(*[self._resolve_user(i) for i in ids]))
        return _wrap(await self._get("users/basic_info_by_id", id=resolved), ResolvedUserResponse)

    async def stats_min(self, user: int | str) -> UserStatsMinResponse | None:
        return _normalise_stats_min(await self._get(f"users/{await self._resolve_user(user)}/stats_min"))

    async def stats(self, user: int | str) -> UserStatsResponse | None:
        return _wrap(await self._get(f"users/{await self._resolve_user(user)}/stats"), UserStatsResponse)

    async def messages_count(self, user: int | str) -> int:
        return await self._get(f"users/{await self._resolve_user(user)}/messages_count") or 0

    async def groups_count(self, user: int | str, only_msg: bool = False) -> int:
        return await self._get(f"users/{await self._resolve_user(user)}/groups_count", onlyMsg=str(only_msg).lower()) or 0

    async def get_messages(self, user: int | str, filter: str | None = None, group: int | str | None = None, limit: int = 20, page: int = 1) -> UserMsgPagedResponse | None:
        params: dict = {"page": page, "pageSize": limit}
        if filter:
            params["text_contains"] = filter
        if group is not None:
            params["group_id"] = await self._resolve_group(group)
        return _wrap(await self._get(f"users/{await self._resolve_user(user)}/messages", **params), UserMsgPagedResponse)

    async def get_chats(self, user: int | str) -> UsrChatInfoResponse | None:
        return _wrap(await self._get(f"users/{await self._resolve_user(user)}/groups"), UsrChatInfoResponse)

    async def get_names(self, user: int | str) -> UserNameInfoResponse | None:
        return _wrap(await self._get(f"users/{await self._resolve_user(user)}/names"), UserNameInfoResponse)

    async def get_usernames(self, user: int | str) -> UserNameInfoResponse | None:
        return _wrap(await self._get(f"users/{await self._resolve_user(user)}/usernames"), UserNameInfoResponse)

    async def rep(self, user: int | str) -> dict | None:
        return await self._get("users/reputation", id=await self._resolve_user(user))

    async def common_groups(self, user: int | str) -> UCommonGroupInfoResponse | None:
        return _wrap(await self._get(f"users/{await self._resolve_user(user)}/common_groups_stat"), UCommonGroupInfoResponse)

    async def get_stickers(self, user: int | str) -> StickerInfoResponse | None:
        return _wrap(await self._get(f"users/{await self._resolve_user(user)}/stickers"), StickerInfoResponse)

    async def get_gifts(self, user: int | str, limit: int = 20, page: int = 1) -> GiftRelationResponse | None:
        return _wrap(await self._get(f"users/{await self._resolve_user(user)}/gifts_relation", page=page, pageSize=limit), GiftRelationResponse)

    async def username_usage(self, username: str) -> UsernameUsageResponse | None:
        return _wrap(await self._get("users/username_usage", username=_clean_username(username)), UsernameUsageResponse)

    async def common_groups_for_users(self, ids: list[int | str]) -> ChatInfoExtResponse | None:
        import asyncio
        resolved = list(await asyncio.gather(*[self._resolve_user(i) for i in ids]))
        return _wrap(await self._get("groups/common_groups", id=resolved), ChatInfoExtResponse)

    async def get_group_info(self, group: int | str) -> dict | None:
        return await self._get(f"groups/{await self._resolve_group(group)}")

    async def get_group_members(self, group: int | str) -> GroupMemberResponse | None:
        return _wrap(await self._get(f"groups/{await self._resolve_group(group)}/members"), GroupMemberResponse)

    async def search_text(self, query: str, page: int = 1, page_size: int = 20) -> WhoWroteTextResponse | None:
        return _wrap(await self._get("text/search", input=query, page=page, pageSize=page_size), WhoWroteTextResponse)