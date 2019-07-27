import pytest

from local_search.neighbours import random_transition
from local_search.neighbours import swap
from local_search.neighbours import invert
from local_search.neighbours import insert


@pytest.fixture
def state():
    return list(range(10))


def test_random_transition():
    for n in range(5, 11):
        i, j = random_transition(n)

        assert i < j
        assert i >= 0 and j >= 0


def test_swap(state):
    new_state = swap(state, 0, 9)
    assert new_state == [9, 1, 2, 3, 4, 5, 6, 7, 8, 0]


def test_invert(state):
    new_state = invert(state, 2, 8)
    assert new_state == [0, 1, 7, 6, 5, 4, 3, 2, 8, 9]


def test_insert(state):
    new_state = insert(state, 2, 8)
    assert new_state == [0, 1, 3, 4, 5, 6, 7, 8, 2, 9]
