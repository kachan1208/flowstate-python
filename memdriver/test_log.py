from memdriver.log import match_labels
from state import State


def test_match_labels():
    assert True == match_labels(
        state=State(labels={"k": "v"}),
        or_labels=[{"k": "v"}],
    )


def test_match_labels_state_with_multiple_labels():
    assert True == match_labels(
        state=State(labels={"k": "v", "k2": "v2", "k3": "v3"}),
        or_labels=[{"k2": "v2"}],
    )


def test_match_labels_no_labels():
    assert True == match_labels(
        state=State(labels={"k": "v", "k2": "v2", "k3": "v3"}),
        or_labels=[],
    )


def test_match_labels_state_no_labels():
    assert False == match_labels(
        state=State(labels={}),
        or_labels=[{"k": "v"}],
    )


def test_match_labels_match_multiple():
    assert True == match_labels(
        state=State(labels={"k": "v", "k2": "v2", "k3": "v3"}),
        or_labels=[{"k": "v", "k2": "v2"}],
    )


def test_match_labels_multiple_one_not_found():
    assert False == match_labels(
        state=State(labels={"k": "v", "k2": "v2", "k3": "v3"}),
        or_labels=[{"k": "v", "k2": "v2", "kk": "vv"}],
    )


def test_match_labels_not_found():
    assert False == match_labels(
        state=State(labels={"k": "v", "k2": "v2", "k3": "v3"}),
        or_labels=[{"kk": "vv"}],
    )


def test_match_labels_not_found_empty_label():
    assert False == match_labels(
        state=State(labels={"k": "v", "k2": "v2", "k3": "v3"}),
        or_labels=[{"": ""}],
    )
