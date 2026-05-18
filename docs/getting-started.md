# Getting Started

## Requirements

- Python 3.10+
- A Funstat API token — get one via bot: [Funstat / Telelog](https://t.me/FiveFohyBot)

## Installation

```bash
pip install funstat-api
```

## Authentication

Pass your token when creating a client:

```python
from funstat_api import FunstatClient

fs = FunstatClient("your_token_here")
```

### Custom Configuration (Headers / Base URL)

If you need to pass custom headers or override the base URL, you can use `FunstatConfig`:

```python
from funstat_api import FunstatClient, FunstatConfig

config = FunstatConfig(
    base_url="https://telelog.org/api/v1",
    headers={"X-My-Custom-Header": "Value"}
)
fs = FunstatClient("your_token", config=config)
```

## Checking the connection

```python
ping = fs.ping()
print(ping.responce_ping)   # round-trip time in seconds

balance = fs.get_balance()
print(balance.current_ballance)
```

## Identifying users

All methods that accept a `user` argument are flexible — you can pass:

```python
fs.stats(12345678)               # numeric ID
fs.stats("durov")                # username without @
fs.stats("@durov")               # username with @
fs.stats("https://t.me/durov")   # full t.me link
```

The same applies to `group` arguments.

## Context managers

Both clients support context managers to ensure connections are closed properly:

=== "Sync"

    ```python
    with FunstatClient("your_token") as fs:
        print(fs.stats("durov"))
    ```

=== "Async"

    ```python
    async with AsyncFunstatClient("your_token") as fs:
        print(await fs.stats("durov"))
    ```

## Error handling

```python
from funstat_api import FunstatClient, ResolveError, ApiError, UserHiddenError

fs = FunstatClient("your_token")

try:
    stats = fs.stats("nonexistent_user_xyz")
except ResolveError as e:
    print(f"User not found: {e}")
except UserHiddenError as e:
    print(f"User data is hidden by privacy settings (HTTP 403 on {e.path})")
except ApiError as e:
    print(f"API error {e.status_code} on {e.path}")
```
