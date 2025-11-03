"""Data Transfer Objects for the application layer."""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from ride_discount.domain.entities import Customer


@dataclass(frozen=True)
class RideContext:
    """DTO containing all information needed to calculate ride discounts.

    This is an input DTO for the CalculateRideDiscount use case.

    Attributes:
        customer: The customer taking the ride
        distance_km: Distance of the ride in kilometers
        base_price: Base price before any discounts
        ride_datetime: Date and time when the ride occurs
    """

    customer: Customer
    distance_km: Decimal
    base_price: Decimal
    ride_datetime: datetime

    def __post_init__(self) -> None:
        """Validate DTO invariants."""
        if self.distance_km < 0:
            raise ValueError("distance_km must be non-negative")
        if self.base_price < 0:
            raise ValueError("base_price must be non-negative")
