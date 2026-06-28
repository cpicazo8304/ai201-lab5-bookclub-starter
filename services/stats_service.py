"""
services/stats_service.py — BookClub

Computes reading statistics for a user: streak, books finished this month,
and total pages read.
"""

from datetime import date, datetime, timezone
from services import reading_service


def calculate_streak(user_id: str) -> int:
    """
    Calculate a user's current reading streak in consecutive days.

    A streak is the number of consecutive calendar days on which the user
    finished at least one book, counting back from today (or yesterday, if
    nothing has been finished today yet).

    Returns 0 if the user has no reading history or if there is a gap of
    more than one day since their most recent finished book.

    Args:
        user_id: ID of the user.

    Returns:
        The streak count as an integer.
    """
    events = reading_service.get_reading_history(user_id)
    if not events:
        return 0

    # Collect unique reading dates, most recent first.
    dates = sorted(
        set(e.finished_at.date() for e in events),
        reverse=True,
    )

    today = date.today()

    # Streak must start from today or yesterday — otherwise it has already broken.
    if (today - dates[0]).days > 1:
        return 0

    streak = 1
    for i in range(len(dates) - 1):
        delta = (dates[i] - dates[i + 1]).days
        if delta == 1:
            streak += 1
        else:
            break

    return streak


def books_this_month(user_id: str) -> int:
    """
    Count the number of books the user finished in the current calendar month.

    Args:
        user_id: ID of the user.

    Returns:
        Count of books finished this month.
    """
    events = reading_service.get_reading_history(user_id)
    today = date.today()
    return sum(
        1
        for e in events
        if e.finished_at.year == today.year and e.finished_at.month == today.month
    )


def total_pages_read(user_id: str) -> int:
    """
    Sum the page counts of all books the user has finished.

    Args:
        user_id: ID of the user.

    Returns:
        Total pages read as an integer.
    """
    events = reading_service.get_reading_history(user_id)
    return sum(e.book.pages for e in events)


def calculate_genre_streak(user_id: str, genre: str) -> int:
    """
    Calculate a user's current reading streak in consecutive days for a specific genre.

    A streak is the number of consecutive calendar days on which the user
    finished at least one book of the specified genre, counting back from today (or yesterday, if
    nothing has been finished today yet).

    Returns 0 if the user has no reading history for that genre or if there is a gap of
    more than one day since their most recent finished book of that genre.

    Args:
        user_id: ID of the user.
        genre: The genre to filter by.
    """
    events = reading_service.get_reading_history(user_id)
    if not events:
        return 0

    # Collect unique reading dates, most recent first. Filter out specific genre
    dates = sorted(
        set(e.finished_at.date() for e in events if e.book.genre == genre),
        reverse=True,
    )
    
    if not dates:
        return 0
    
    today = date.today()

    # Streak must start from today or yesterday — otherwise it has already broken.
    if (today - dates[0]).days > 1:
        return 0

    streak = 1
    for i in range(len(dates) - 1):
        delta = (dates[i] - dates[i + 1]).days
        if delta == 1:
            streak += 1
        else:
            break

    return streak
