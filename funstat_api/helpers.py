import logging
import re
from typing import Any

from pydantic import BaseModel

from .exceptions import ApiError
from .models import TechInfo, UserStatsMin, UserStatsMinResponse

logger = logging.getLogger("funstat")

DEFAULT_BASE_URL = "https://telelog.org/api/v1"


def _clean_username(username: str) -> str:
    """Clean username or invite link to standard format."""
    username = username.strip()
    username = re.sub(r"^https?://t\.me/", "", username)
    username = re.sub(r"^t\.me/", "", username)
    return username.lstrip("@").split("/")[0].split("?")[0]


def _make_empty_tech() -> TechInfo:
    return TechInfo(request_cost=0.0, current_ballance=0.0, request_duration="")


def _wrap(payload: dict[str, Any] | None, model: type[BaseModel]) -> BaseModel | None:
    if payload is None:
        return None
    if not payload.get("success", True):
        logger.warning("API returned success=false: %s", payload)
        # Assuming the API payload structure has some error message when success=False
        # If not, raising ApiError directly is a good pattern.
        raise ApiError(status_code=None, path=None, message=f"API returned success=false: {payload}")
    return model.model_validate(payload)


def _normalise_stats_min(payload: dict[str, Any] | None) -> UserStatsMinResponse | None:
    if payload is None:
        return None
    if "success" not in payload:
        return UserStatsMinResponse(
            success=True,
            tech=_make_empty_tech(),
            data=UserStatsMin.model_validate(payload),
        )
    if not payload.get("success", True):
        raise ApiError(status_code=None, path=None, message=f"API returned success=false: {payload}")
    return UserStatsMinResponse.model_validate(payload)


def _extract_tech(result: dict[str, Any] | None) -> TechInfo | None:
    if result and "tech" in result:
        return TechInfo.model_validate(result["tech"])
    return None
