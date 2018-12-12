from pathlib import Path

import pytest
from twitter.error import TwitterError

from coo import Coo
from coo.exceptions import TweetTypeError, ScheduleError


# Mock Update list
m_updates = ["mock1", "mock2", "mock3", "mock4", "mock5"]


@pytest.fixture
def coo_preview_instance():
    yield Coo("mock", "mock", "mock", "mock", preview=True)


@pytest.fixture
def coo_mock_instance():
    yield Coo("mock1", "mock2", "mock3", "mock4")


# API
def test_wrong_credentials_TwitterError(coo_mock_instance):
    with pytest.raises(TwitterError):
        coo_mock_instance.verify


# TWEET
@pytest.mark.parametrize(
    "updates, delay, interval, template, time_zone",
    [
        (m_updates, None, None, None, None),
        # One None
        (m_updates, None, "now", "$message", "local"),
        (m_updates, "now", None, "$message", "local"),
        (m_updates, "now", "now", None, "local"),
        (m_updates, "now", "now", "$message", None),
        # Two None
        (m_updates, None, None, "$message", "local"),
        (m_updates, "now", None, None, "local"),
        (m_updates, "now", "now", None, None),
        (m_updates, None, "now", "$message", None),
        # Delay
        (m_updates, "now", None, None, None),
        (m_updates, 0, None, None, None),
        # Interval
        (m_updates, None, "now", None, None),
        (m_updates, None, 0, None, None),
        # Template
        (m_updates, None, None, "$message", None),
        # Time zone
        (m_updates, None, None, None, "local"),
        (m_updates, None, None, None, "America/Santiago "),
    ],
)
def test_tweet(coo_preview_instance, updates, delay, interval, template, time_zone):
    coo_preview_instance.tweet(updates, delay, interval, template, time_zone)


@pytest.mark.parametrize(
    "updates",
    [
        # update is not a instance of list:
        ((1, 2, 3)),
        ({1, 2, 3}),
        (123),
        ("string"),
        # The instances 'in' the list are no strings:
        ([(1, 2, 3)]),
        ([{1, 2, 3}]),
        ([[1, 2, 3]]),
        ([1, 2, 3]),
    ],
)
def test_tweet_TweetTypeError(coo_preview_instance, updates):
    with pytest.raises(TweetTypeError):
        coo_preview_instance.tweet(updates)


def test_tweet_random(coo_preview_instance):
    updates = ["mock1", "mock2", "mock3", "mock4", "mock5"]
    coo_preview_instance.tweet(m_updates, aleatory=True)
    assert updates != m_updates


def test_tweet_media_update(coo_preview_instance):
    coo_preview_instance.tweet(["mock"], media="../coo.png")
    assert coo_preview_instance.media == Path("../coo.png")


@pytest.mark.parametrize(
    "tz",
    [
        ("Canada/Yukon"),
        ("Brazil/Acre"),
        ("Australia/Tasmania"),
        ("America/Santiago"),
        ("America/Detroit"),
        ("Asia/Atyrau"),
    ],
)
def test_tweet_time_zone(coo_preview_instance, tz):
    coo_preview_instance.tweet(["mock"], time_zone=tz)
    assert coo_preview_instance.time_zone == tz


# SCHEDULE
@pytest.mark.parametrize(
    "updates",
    [
        (
            [
                ("now", "template", "update"),
                (0, "template", "update"),
                ("now", None, "update"),
                (0, None, "update"),
            ]
        )
    ],
)
def test_schedule_time_zone_media(coo_preview_instance, updates):
    coo_preview_instance.schedule(updates, time_zone="Canada/Yukon", media="../coo.png")
    assert coo_preview_instance.time_zone == "Canada/Yukon"
    assert coo_preview_instance.media == Path("../coo.png")
    assert coo_preview_instance.global_media == Path("../coo.png")


@pytest.mark.parametrize(
    "updates",
    [
        ([["update1", "update2"]]),
        ([{"update1", "update2"}]),
        (["update1", "update2"]),
        ([123, 456, 789]),
    ],
)
def test_schedule_ScheduleError(coo_preview_instance, updates):
    with pytest.raises(ScheduleError):
        coo_preview_instance.schedule(updates)


def test_schedule_len_tuple_ScheduleError():
    # TODO: write a test for ScheduleError for the wrong len(tuple).
    pass


# STR UPDATE
@pytest.mark.parametrize(
    "update, template", [("My Twitter Update", None), ("My Twitter Update", "$message")]
)
def test_str_update(coo_preview_instance, update, template):
    coo_preview_instance.str_update(update, template)


# def test_str_update_media(coo_preview_instance):
    # TODO: test string update with media file
    # coo_preview_instance.str_update("update", media="../coo.png")
    # assert coo_preview_instance.media == Path("../coo.png")


# DELAY
@pytest.mark.parametrize("delay", [(0), ("now")])
def test_delay(coo_preview_instance, delay):
    coo_preview_instance.delay(delay)


# INTERVAL
@pytest.mark.parametrize("interval", [(0), ("now")])
def test_interval(coo_preview_instance, interval):
    coo_preview_instance.interval(interval)
