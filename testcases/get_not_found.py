import pytest

from cmd_get import get_by_id
from memdriver.driver import Driver, ErrNotFound
from engine import Engine
from state import StateCtx


def test_get_not_found():
    driver = Driver()
    e = Engine(driver)

    with pytest.raises(ErrNotFound):
        e.do(
            get_by_id(
                StateCtx(),
                "not_found",
                0,
            )
        )
