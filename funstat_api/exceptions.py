"""Exceptions for the Funstat API client."""


class FunstatError(Exception):
    """Base exception for all funstat API errors."""


class ResolveError(FunstatError):
    """Raised when a username or group cannot be resolved to a numeric ID."""


class ApiError(FunstatError):
    """Raised when the API returns a non-200 status code or success=False."""

    def __init__(self, status_code: int | None, path: str | None, message: str = "") -> None:
        self.status_code = status_code
        self.path = path
        msg = message or f"HTTP {status_code} for {path}"
        super().__init__(msg)


class UserHiddenError(ApiError):
    """Raised when the API returns a 403 Forbidden, usually indicating user hidden data."""

    def __init__(self, path: str | None, message: str = "") -> None:
        super().__init__(status_code=403, path=path, message=message or f"HTTP 403 (User Hidden Data) for {path}")
