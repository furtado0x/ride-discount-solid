"""Base discount rule for the domain layer."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, ClassVar

from ride_discount.domain.value_objects import DiscountResult

if TYPE_CHECKING:
    from ride_discount.application.dtos import RideContext


class DiscountRule(ABC):
    """Abstract base class for discount rules.

    This class implements the Strategy Pattern with automatic registration.
    All subclasses are automatically registered when they are defined,
    allowing the system to be extended without modifying existing code
    (Open/Closed Principle).

    Class Attributes:
        registered_rules: List of all registered discount rule classes
    """

    registered_rules: ClassVar[list[type[DiscountRule]]] = []

    def __init_subclass__(cls) -> None:
        """Automatically register new discount rule subclasses.

        This method is called when a new subclass is defined, ensuring
        automatic registration without manual intervention.
        """
        super().__init_subclass__()
        DiscountRule.registered_rules.append(cls)

    @abstractmethod
    def calculate_discount(self, context: RideContext) -> DiscountResult | None:
        """Calculate the discount for the given ride context.

        Args:
            context: The ride context containing customer, distance, and time info

        Returns:
            DiscountResult if a discount applies, None otherwise
        """
        pass
