import pytest

from funstat_api.helpers import _clean_username


@pytest.mark.parametrize(
    ("input_str", "expected"),
    [
        ("durov", "durov"),
        ("@durov", "durov"),
        ("https://t.me/durov", "durov"),
        ("http://t.me/durov", "durov"),
        ("t.me/durov", "durov"),
        ("https://t.me/durov/123", "durov"),
        ("https://t.me/durov?start=123", "durov"),
        ("  @durov  ", "durov"),
        ("-100123456", "-100123456"),
        ("123456", "123456"),
    ],
)
def test_clean_username(input_str: str, expected: str) -> None:
    assert _clean_username(input_str) == expected
