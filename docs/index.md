# funstat-api

**Python client for the [Funstat](http://funstat.in/?start=0108FC1E9BEF75617466) API** — Telegram user and group statistics.

Supports both **sync** and **async** modes out of the box.

---

## Installation

```bash
pip install funstat-api
```

## Quick Example

=== "Sync"

    ```python
    from funstat_api import FunstatClient

    with FunstatClient("your_token") as fs:
        stats = fs.stats("durov")
        print(stats.data.total_msg_count)
    ```

=== "Async"

    ```python
    import asyncio
    from funstat_api import AsyncFunstatClient

    async def main():
        async with AsyncFunstatClient("your_token") as fs:
            stats = await fs.stats("durov")
            print(stats.data.total_msg_count)

    asyncio.run(main())
    ```

---

## Features

- ✅ Sync client powered by `requests`
- ✅ Async client powered by `httpx`
- ✅ Fully typed — all responses are Pydantic models
- ✅ Accepts username, `@username`, numeric ID, or `t.me/` link
- ✅ Auto-resolves usernames to IDs internally

---

[Get Started :material-arrow-right:](getting-started.md){ .md-button .md-button--primary }

---

## Links

- [PyPI](https://pypi.org/project/funstat-api/)
- [GitHub](https://github.com/chizumeiji/funstat-api)
- [Funstat](http://funstat.in/?start=0108FC1E9BEF75617466)
