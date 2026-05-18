# Exceptions

```python
from funstat_api import FunstatError, ResolveError, ApiError
```

---

## `FunstatError`

Base exception for all funstat errors. Catch this to handle any library error:

```python
from funstat_api import FunstatError

try:
    result = fs.stats("someone")
except FunstatError as e:
    print(f"Something went wrong: {e}")
```

---

## `ResolveError`

Raised when a username or group cannot be resolved to a numeric ID.
See [`resolve_username`](sync.md#resolve_usernameusername--resolveduserresponse--none) and [`username_usage`](sync.md#username_usageusername--usernameusageresponse--none) for context.

```python
from funstat_api import ResolveError

try:
    result = fs.stats("nonexistent_xyz_404")
except ResolveError as e:
    print(f"Not found: {e}")
```

---

## `ApiError`

Raised when the API returns a non-200 HTTP status code.

| Attribute | Type | Description |
|-----------|------|-------------|
| `status_code` | `int` | HTTP status code returned by the API |
| `path` | `str` | API path that was requested |

```python
from funstat_api import ApiError

try:
    result = fs.stats("durov")
except ApiError as e:
    print(f"HTTP {e.status_code} on {e.path}")
```

---

## `UserHiddenError`

Raised specifically when the API returns a `403 Forbidden` status code, which usually indicates that a user's data is hidden by their privacy settings. Inherits from `ApiError`.

```python
from funstat_api import UserHiddenError

try:
    result = fs.stats("hidden_user")
except UserHiddenError as e:
    print(f"Data is hidden for {e.path}")
```

---

## Exception hierarchy

```
FunstatError
├── ResolveError   # username/group not found
└── ApiError       # non-200 HTTP response
    └── UserHiddenError # 403 Forbidden (privacy settings)
```
