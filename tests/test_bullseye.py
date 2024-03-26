#!/bin/env python3

"""testing suite of bullseye"""

from be import bullseye

from hypothesis import given
from hypothesis import assume
from hypothesis import strategies as st

import pytest

import numpy as np

from docopt import docopt

PREC = 14

def test_version():
    """tests  bullseye version number"""
    assert bullseye.__version__ == "0.2.0"


def round_down(x, precision=PREC):
    """helper function: round a float down to a given precision in order to
    avoid issues with floating point precision

    Args:
      x (float): the floating point number to be truncated
      precision (int): the number of decimal point to truncate x to.

    Returns:
       (float): a truncated number such that old_x - new_x < precision
    """
    return np.trunc(x*10**precision)/10**precision


@given(r=st.floats(min_value=0, max_value=1, allow_nan=False))
def test_update_perfect_hit(r):
    """The radius must not shrink if we hit the bullseye

    If we hit the center of the dartboard precisely, i.e. hit (0, 0), the
    radius should remain the same."""
    x, y = 0.0, 0.0
    r = round_down(r)
    np.testing.assert_almost_equal(bullseye.update(x, y, r), r, PREC-2)


@given(r=st.floats(min_value=0, max_value=1, allow_nan=False))
def test_update_perfect_miss(r):
    """The radius must be zero if we hit the border"""
    x, y = 0.0, 0.0
    r = round_down(r)
    np.testing.assert_almost_equal(bullseye.update(r, y, r),  0)
    np.testing.assert_almost_equal(bullseye.update(x, r, r),  0)


@given(r=st.floats(min_value=0, max_value=1, allow_nan=False),
       x=st.floats(min_value=0, max_value=1, allow_nan=False),
       y=st.floats(min_value=0, max_value=1, allow_nan=False)
       )
def test_update_miss_returns_minus_one(x, y, r):
    """update returns -1 if we hit a clear miss"""
    R = x**2+y**2
    r = r**2
    assume(R > r)
    assert bullseye.update(x, y, r) == -1

def test_game_scores_at_least_1():
    """the number of scores is the number of darts thrown, so it's at least
    one."""
    for game in range(10):
        assert bullseye.game() >= 1


def test_main():
    """for a random (but senisble) number of games, we should be able to
    recover almost :math:`e^\frac{\\pi}{4}`.

    We therefore first pick a random number of games to play, then calculate
    the mean of the scores. Then we check if
    :math:`e^\frac{\\pi}{4}` is almost identical to the number we
    found.
    """
    games = int(1e5)
    mean= bullseye.main(opts=None, games=games)
    np.testing.assert_almost_equal(mean, np.e**(np.pi/4), decimal=2)


def test_opts_accepts_games():
    """Tests whether get_opts gets the flag --games from stdin"""
    doc = bullseye.__doc__
    opts = docopt(doc, ["--games", "10"])
    assert opts["--games"] == "10"

def test_opts_accepts_seed():
    """Tests whether get_opts gets the flag --seed from stdin"""
    doc = bullseye.__doc__
    rand = np.random.randint(0, 1000)
    opts = docopt(doc, ["--seed", f"{rand}"])
    assert opts["--seed"] == str(rand)

def test_seed_is_set():
    """Tests whether the seed is set and thus the output is reproducable"""
    seed = np.random.randint(1, 10000000)
    games = 100000
    result1 = bullseye.main(opts={"--seed": str(seed), "--games": None}, games=games)
    result2 = bullseye.main(opts={"--seed": str(seed), "--games": None}, games=games)

    assert result1 == result2
