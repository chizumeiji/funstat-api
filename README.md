# funstat-api

Python client for the [Funstat](http://funstat.in/?start=0108FC1E9BEF75617466) API — Telegram user and group statistics.

Supports both **sync** and **async** usage.

## Installation

```bash
pip install funstat-api
```

## Quick Start

### Sync

```python
from funstat_api import FunstatClient

fs = FunstatClient("your_token")

# Get user stats
stats = fs.stats("durov")
print(stats.data.total_msg_count)

# Get group members
members = fs.get_group_members("https://t.me/mychat")

# Use as context manager
with FunstatClient("your_token") as fs:
    print(fs.ping())
```

### Async

```python
import asyncio
from funstat_api import AsyncFunstatClient

async def main():
    async with AsyncFunstatClient("your_token") as fs:
        stats = await fs.stats("durov")
        print(stats.data.total_msg_count)

asyncio.run(main())
```

## Available Methods

| Method | Description |
|--------|-------------|
| `ping()` | Check API availability and latency |
| `get_balance()` | Get current token balance |
| `resolve_username(username)` | Resolve username to user info |
| `basic_info_by_id(ids)` | Get basic info by user ID(s) |
| `stats_min(user)` | Get minimal user statistics |
| `stats(user)` | Get full user statistics |
| `messages_count(user)` | Get total message count |
| `groups_count(user)` | Get number of groups |
| `get_messages(user, ...)` | Get paginated message list |
| `get_chats(user)` | Get user's chat list |
| `get_names(user)` | Get name history |
| `get_usernames(user)` | Get username history |
| `get_stickers(user)` | Get used sticker packs |
| `get_gifts(user)` | Get gift relations |
| `common_groups(user)` | Get common groups stats |
| `username_usage(username)` | Who uses or used a username |
| `get_group_info(group)` | Get group/channel info |
| `get_group_members(group)` | Get group members |
| `search_text(query)` | Search messages by text |

`user` and `group` arguments accept: numeric ID, `@username`, or `https://t.me/...` link.

## Dependencies

- `pydantic >= 2.0`
- `requests >= 2.28` (sync client)
- `httpx >= 0.24` (async client)

## License

MIT