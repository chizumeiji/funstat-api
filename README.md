# funstat-api

Python client for the [Funstat/Telelog](http://telelog.org/) API — Telegram user and group statistics.

Supports both **sync** and **async** usage.

Documentation: https://chizumeiji.github.io/funstat-api/

## Installation

```bash
pip install funstat-api
```

## Quick Start

### Sync

```python
from funstat_api import FunstatClient, FunstatConfig

# Optional: configure custom headers or base URL
config = FunstatConfig(headers={"X-My-Header": "Value"})
fs = FunstatClient("your_token", config=config)

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
from funstat_api import AsyncFunstatClient, UserHiddenError

async def main():
    async with AsyncFunstatClient("your_token") as fs:
        try:
            stats = await fs.stats("durov")
            print(stats.data.total_msg_count)
        except UserHiddenError:
            print("This user's data is hidden by privacy settings.")

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
| `name_usage(name)` | Search name usage |
| `rep(user)` | Get user reputation info |
| `common_groups_for_users(ids)` | Get common groups for specified users |
| `get_group_info(group)` | Get group/channel info |
| `get_group_members(group)` | Get group members |
| `search_text(query)` | Search messages by text |

`user` and `group` arguments accept: numeric ID, `@username`, or `https://t.me/...` link.

## Dependencies

- `pydantic >= 2.0`
- `requests >= 2.28` (sync client)
- `httpx >= 0.24` (async client)

## Credits

- **Author:** [@meiji_dev](https://t.me/meiji_dev)
- **Useful bots & links:** [@sgwlink](https://t.me/sgwlink)

## License

MIT