from typing import Optional
from datetime import datetime


def second_difference(
    target_date: datetime, reference_date: Optional[datetime] = None
) -> int:
    """Calculate the difference in seconds between two dates."""
    if reference_date is None:
        reference_date = datetime.now()
    return (target_date - reference_date).total_seconds()


def hour_difference(
    target_date: datetime, reference_date: Optional[datetime] = None
) -> int:
    """Calculate the difference in seconds between two dates."""
    if reference_date is None:
        reference_date = datetime.now()
    return int((target_date - reference_date).total_seconds() / 3600)


def day_difference(
    target_date: datetime, reference_date: Optional[datetime] = None
) -> int:
    """Calculate the difference in days between two dates."""
    if reference_date is None:
        reference_date = datetime.now()
    return (target_date - reference_date).days
