"""Ride discount system - Clean Architecture implementation."""

from ride_discount.application.dtos import RideContext
from ride_discount.application.use_cases import CalculateRideDiscountUseCase
from ride_discount.domain.entities import Customer

# Import rules to trigger auto-registration
from ride_discount.domain.rules import (  # noqa: F401
    DiscountRule,
    OffPeakDiscountRule,
    ProportionalDistanceDiscountRule,
    RideFrequencyDiscountRule,
)
from ride_discount.domain.value_objects import DiscountResult

__all__ = [
    "Customer",
    "RideContext",
    "DiscountResult",
    "CalculateRideDiscountUseCase",
]
