# Models

All API responses are typed Pydantic v2 models. Import them directly:

```python
from funstat_api import UserStats, GroupMember, ChatInfo  # etc.
```

---

## Response wrappers

Every method returns a response wrapper with a consistent shape:

| Field | Type | Description |
|-------|------|-------------|
| `success` | `bool` | Whether the request succeeded |
| `tech` | [`TechInfo`](#techinfo) | Request cost and balance info |
| `data` | `... \| None` | The actual payload |
| `paging` | [`Paging`](#paging)` \| None` | Pagination info (paginated endpoints only) |

---

## TechInfo

```python
class TechInfo:
    request_cost: float
    current_ballance: float
    request_duration: str
```

---

## Paging

```python
class Paging:
    total: int
    current_page: int
    page_size: int
    total_pages: int
```

---

## ResolvedUser

```python
class ResolvedUser:
    id: int
    username: str | None
    first_name: str | None
    last_name: str | None
    is_active: bool
    is_bot: bool
    has_premium: bool | None
```

---

## UserStatsMin

```python
class UserStatsMin:
    id: int
    first_name: str | None
    last_name: str | None
    is_bot: bool
    is_active: bool
    first_msg_date: str | None
    last_msg_date: str | None
    total_msg_count: int
    msg_in_groups_count: int
    adm_in_groups: int
    usernames_count: int
    names_count: int
    total_groups: int
```

---

## UserStats

Extends [`UserStatsMin`](#userstatsmin) with additional fields:

```python
class UserStats(UserStatsMin):
    is_cyrillic_primary: bool | None
    lang_code: str | None
    unique_percent: float | None
    circle_count: int
    voice_count: int
    reply_percent: float
    media_percent: float
    link_percent: float
    favorite_chat: ChatInfo | None
    media_usage: str | None
    stars_val: int | None
    gift_count: int | None
    about: str | None
    # ... and more
```

---

## ChatInfo

```python
class ChatInfo:
    id: int
    title: str
    is_private: bool
    username: str | None
```

---

## ChatInfoExt

Extends [`ChatInfo`](#chatinfo):

```python
class ChatInfoExt(ChatInfo):
    is_channel: bool
    link: str | None
```

---

## GroupMember

```python
class GroupMember:
    id: int
    username: str | None
    name: str | None
    first_name: str | None
    last_name: str | None
    is_admin: bool | None
    is_active: bool
    today_msg: int
    has_prem: bool | None
    has_photo: bool
    dc_id: int | None
```

---

## UserMsg

```python
class UserMsg:
    date: str
    message_id: int
    reply_to_message_id: int | None
    media_code: int | None
    media_name: str | None
    text: str | None
    group: ChatInfo
```

---

## UserNameInfo

```python
class UserNameInfo:
    name: str
    date_time: str
```

---

## UsrChatInfo

```python
class UsrChatInfo:
    chat: ChatInfo
    last_message_id: int
    messages_count: int
    last_message: str | None
    first_message: str | None
    is_admin: bool
    is_left: bool
```

---

## GiftRelationInfo

```python
class GiftRelationInfo:
    last_gift_date: str | None
    from_user_id: int
    from_first_name: str | None
    from_last_name: str | None
    from_main_username: str | None
    from_is_active: bool
    to_user_id: int
    to_first_name: str | None
    to_last_name: str | None
    to_main_username: str | None
    to_is_active: bool
```

---

## StickerInfo

```python
class StickerInfo:
    sticker_set_id: int
    last_seen: str
    min_seen: str
    resolved: str | None
    title: str | None
    short_name: str | None
    stickers_count: int | None
```

---

## UCommonGroupInfo

```python
class UCommonGroupInfo:
    user_id: int
    common_groups: int
    first_name: str | None
    last_name: str | None
    username: str | None
    is_user_active: bool
```

---

## UsernameUsageModel

```python
class UsernameUsageModel:
    actual_users: list[ResolvedUser] | None
    usage_by_users_in_the_past: list[ResolvedUser] | None
    actual_groups_or_channels: list[ChatInfoExt] | None
    mention_by_channel_or_group_desc: list[ChatInfoExt] | None
```

---

## WhoWroteText

```python
class WhoWroteText:
    message_id: int
    user_id: int
    date: str
    name: str | None
    username: str | None
    is_active: bool
    group: ChatInfoExt
    text: str | None
```

---

## WhoWroteTextPaged

```python
class WhoWroteTextPaged:
    total: int
    data: list[WhoWroteText]
    is_last_page: bool | None
    page_size: int | None
    current_page: int | None
    total_pages: int | None
```

---

## PingResult

```python
class PingResult:
    request_ping: str     # duration reported by the API
    responce_ping: float  # actual round-trip in seconds
```

---

## Response wrappers reference

| Class | `.data` type |
|-------|-------------|
| `ResolvedUserResponse` | `list[`[`ResolvedUser`](#resolveduser)`]` |
| `UserStatsMinResponse` | [`UserStatsMin`](#userstatsmin) |
| `UserStatsResponse` | [`UserStats`](#userstats) |
| `UserMsgPagedResponse` | `list[`[`UserMsg`](#usermsg)`]` |
| `UserNameInfoResponse` | `list[`[`UserNameInfo`](#usernameinfo)`]` |
| `UsrChatInfoResponse` | `list[`[`UsrChatInfo`](#usrchatinfo)`]` |
| `GroupMemberResponse` | `list[`[`GroupMember`](#groupmember)`]` |
| `GiftRelationResponse` | `list[`[`GiftRelationInfo`](#giftrelationinfo)`]` |
| `StickerInfoResponse` | `list[`[`StickerInfo`](#stickerinfo)`]` |
| `UCommonGroupInfoResponse` | `list[`[`UCommonGroupInfo`](#ucommongroupinfo)`]` |
| `UsernameUsageResponse` | [`UsernameUsageModel`](#usernameusagemodel) |
| `ChatInfoExtResponse` | `list[`[`ChatInfoExt`](#chatinfoext)`]` |
| `WhoWroteTextResponse` | [`WhoWroteTextPaged`](#whowrotetextpaged) |

---

## ResolvedUserResponse

`success` · [`TechInfo`](#techinfo) · `data: list[`[`ResolvedUser`](#resolveduser)`]`

## UserStatsMinResponse

`success` · [`TechInfo`](#techinfo) · `data:` [`UserStatsMin`](#userstatsmin)

## UserStatsResponse

`success` · [`TechInfo`](#techinfo) · `data:` [`UserStats`](#userstats)

## UserMsgPagedResponse

`success` · [`TechInfo`](#techinfo) · [`Paging`](#paging) · `data: list[`[`UserMsg`](#usermsg)`]`

## UserNameInfoResponse

`success` · [`TechInfo`](#techinfo) · `data: list[`[`UserNameInfo`](#usernameinfo)`]`

## UsrChatInfoResponse

`success` · [`TechInfo`](#techinfo) · `data: list[`[`UsrChatInfo`](#usrchatinfo)`]`

## GroupMemberResponse

`success` · [`TechInfo`](#techinfo) · `data: list[`[`GroupMember`](#groupmember)`]`

## GiftRelationResponse

`success` · [`TechInfo`](#techinfo) · `data: list[`[`GiftRelationInfo`](#giftrelationinfo)`]`

## StickerInfoResponse

`success` · [`TechInfo`](#techinfo) · `data: list[`[`StickerInfo`](#stickerinfo)`]`

## UCommonGroupInfoResponse

`success` · [`TechInfo`](#techinfo) · `data: list[`[`UCommonGroupInfo`](#ucommongroupinfo)`]`

## UsernameUsageResponse

`success` · [`TechInfo`](#techinfo) · `data:` [`UsernameUsageModel`](#usernameusagemodel)

## ChatInfoExtResponse

`success` · [`TechInfo`](#techinfo) · `data: list[`[`ChatInfoExt`](#chatinfoext)`]`

## WhoWroteTextResponse

`success` · [`TechInfo`](#techinfo) · `data:` [`WhoWroteTextPaged`](#whowrotetextpaged)
