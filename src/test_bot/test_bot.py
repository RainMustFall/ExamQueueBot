import pytest

from ..utils import parse_args


PARSE_ARGS_CASES = [
    (
        ["Bob", "James", "Patricia"],
        "/move 1 2",
        (0, 1)
    ),
    (
        ["Bob", "James", "Patricia"],
        "/move James 2",
        (1, 1)
    ),
    (
        ["Bob", "James", "Patricia"],
        "/move Bob Patricia",
        (0, 2)
    )
]


@pytest.mark.parametrize("people_list, message, expected", PARSE_ARGS_CASES)
def test_parse_args(people_list, message, expected):
    assert parse_args(people_list, message) == expected
