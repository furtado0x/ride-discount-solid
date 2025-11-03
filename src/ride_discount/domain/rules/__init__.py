"""Discount rules for the domain layer."""

from ride_discount.domain.rules.base import DiscountRule
from ride_discount.domain.rules.distance import ProportionalDistanceDiscountRule
from ride_discount.domain.rules.frequency import RideFrequencyDiscountRule
from ride_discount.domain.rules.offpeak import OffPeakDiscountRule

__all__ = [
    "DiscountRule",
    "RideFrequencyDiscountRule",
    "ProportionalDistanceDiscountRule",
    "OffPeakDiscountRule",
]
