"""Protocols for type checking in the ride discount system."""

from typing import Protocol

from ride_discount.application.dtos import RideContext
from ride_discount.domain.value_objects import DiscountResult


class DiscountRuleProtocol(Protocol):
    """Protocol defining the interface for discount rules.

    This protocol can be used for type hints when you need structural
    subtyping instead of nominal subtyping (ABC inheritance).
    """

    def calculate_discount(self, context: RideContext) -> DiscountResult | None:
        """Calculate the discount for the given ride context.

        Args:
            context: The ride context containing customer, distance, and time info

        Returns:
            DiscountResult if a discount applies, None otherwise
        """
        ...
