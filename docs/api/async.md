# Async Client

```python
from funstat_api import AsyncFunstatClient
```

## `AsyncFunstatClient(token)`

Creates an asynchronous client. Uses `httpx` under the hood. All methods must be `await`-ed.

| Parameter | Type | Description |
|-----------|------|-------------|
| `token` | `str` | Your Funstat API token |

---

## Methods

All methods are identical to the [Sync Client](sync.md) but are coroutines — prefix every call with `await`.
Return types and parameters are the same — refer to [Sync Client](sync.md) for the full reference and [Models](models.md) for response type details.

```python
async with AsyncFunstatClient("your_token") as fs:
    stats    = await fs.stats("durov")
    messages = await fs.get_messages("durov", limit=50)
    members  = await fs.get_group_members("https://t.me/mychat")
    usage    = await fs.username_usage("durov")
```

---

### Parallel requests

Because the client is async, you can fire multiple requests concurrently with `asyncio.gather`:

```python
import asyncio
from funstat_api import AsyncFunstatClient

async def main():
    async with AsyncFunstatClient("your_token") as fs:
        stats, chats, names = await asyncio.gather(
            fs.stats("durov"),       # → UserStatsResponse
            fs.get_chats("durov"),   # → UsrChatInfoResponse
            fs.get_names("durov"),   # → UserNameInfoResponse
        )

asyncio.run(main())
```

---

### close

`async close()`

Closes the underlying `httpx.AsyncClient`. Called automatically when using `async with`.
