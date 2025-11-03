"""Domain layer for ride discount system."""

from ride_discount.domain.entities import Customer
from ride_discount.domain.value_objects import DiscountResult

__all__ = ["Customer", "DiscountResult"]
