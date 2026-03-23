# Sync Client

```python
from funstat_api import FunstatClient
```

## `FunstatClient(token)`

Creates a synchronous client. Uses `requests` under the hood.

| Parameter | Type | Description |
|-----------|------|-------------|
| `token` | `str` | Your Funstat API token |

---

## Methods

### ping

`ping() →` [`PingResult`](models.md#pingresult) `| None`

Check API availability and measure round-trip latency.

```python
result = fs.ping()
print(result.responce_ping)   # seconds
```

---

### get_balance

`get_balance() →` [`TechInfo`](models.md#techinfo) `| None`

Get current token balance and cost info.

```python
balance = fs.get_balance()
print(balance.current_ballance)
```

---

### resolve_username

`resolve_username(username) →` [`ResolvedUserResponse`](models.md#resolveduserresponse) `| None`

Resolve a username to full user info.

```python
result = fs.resolve_username("durov")
user = result.data[0]
print(user.id, user.first_name)
```

---

### basic_info_by_id

`basic_info_by_id(ids) →` [`ResolvedUserResponse`](models.md#resolveduserresponse) `| None`

Get basic info for one or multiple users by numeric ID.

```python
result = fs.basic_info_by_id([123, 456])
```

---

### stats_min

`stats_min(user) →` [`UserStatsMinResponse`](models.md#userstatsminresponse) `| None`

Get minimal statistics for a user.

```python
result = fs.stats_min("durov")
print(result.data.total_msg_count)
```

---

### stats

`stats(user) →` [`UserStatsResponse`](models.md#userstatsresponse) `| None`

Get full statistics for a user.

```python
result = fs.stats("durov")
print(result.data.reply_percent)
```

---

### messages_count

`messages_count(user) → int`

Get total message count for a user.

---

### groups_count

`groups_count(user, only_msg=False) → int`

Get number of groups a user belongs to.
Set `only_msg=True` to count only groups where the user has sent messages.

---

### get_messages

`get_messages(user, filter=None, group=None, limit=20, page=1) →` [`UserMsgPagedResponse`](models.md#usermsgpagedresponse) `| None`

Get paginated message history for a user.

| Parameter | Type | Description |
|-----------|------|-------------|
| `user` | `int \| str` | User identifier |
| `filter` | `str \| None` | Filter by text content |
| `group` | `int \| str \| None` | Filter by group |
| `limit` | `int` | Page size (default 20) |
| `page` | `int` | Page number (default 1) |

```python
result = fs.get_messages("durov", filter="hello", limit=50)
for msg in result.data:
    print(msg.date, msg.text)
```

---

### get_chats

`get_chats(user) →` [`UsrChatInfoResponse`](models.md#usrchatinforesponse) `| None`

Get list of chats the user participates in.

---

### get_names

`get_names(user) →` [`UserNameInfoResponse`](models.md#usernameinforesponse) `| None`

Get name change history for a user.

---

### get_usernames

`get_usernames(user) →` [`UserNameInfoResponse`](models.md#usernameinforesponse) `| None`

Get username change history for a user.

---

### get_stickers

`get_stickers(user) →` [`StickerInfoResponse`](models.md#stickerinforesponse) `| None`

Get sticker packs used by a user.

---

### get_gifts

`get_gifts(user, limit=20, page=1) →` [`GiftRelationResponse`](models.md#giftrelationresponse) `| None`

Get gift relations (sent/received) for a user.

---

### common_groups

`common_groups(user) →` [`UCommonGroupInfoResponse`](models.md#ucommongroupinforesponse) `| None`

Get statistics on common groups with other users.

---

### rep

`rep(user) → dict | None`

Get reputation data for a user.

---

### username_usage

`username_usage(username) →` [`UsernameUsageResponse`](models.md#usernameusageresponse) `| None`

Find who currently uses or has previously used a username.

```python
result = fs.username_usage("durov")
print(result.data.actual_users)
```

---

### common_groups_for_users

`common_groups_for_users(ids) →` [`ChatInfoExtResponse`](models.md#chatinfoextresponse) `| None`

Find groups that a list of users all share.

```python
result = fs.common_groups_for_users([123, 456, 789])
```

---

### get_group_info

`get_group_info(group) → dict | None`

Get raw info about a group or channel.

---

### get_group_members

`get_group_members(group) →` [`GroupMemberResponse`](models.md#groupmemberresponse) `| None`

Get member list of a group.

```python
result = fs.get_group_members("https://t.me/mychat")
for member in result.data:
    print(member.id, member.username)
```

---

### search_text

`search_text(query, page=1, page_size=20) →` [`WhoWroteTextResponse`](models.md#whowrotetextresponse) `| None`

Search all indexed messages by text content.

```python
result = fs.search_text("hello world")
for item in result.data.data:
    print(item.user_id, item.text)
```

---

### close

`close()`

Close the underlying HTTP session. Called automatically when using `with`.
