"""Value objects for ride discount system."""

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class DiscountResult:
    """Immutable value object representing a discount calculation result.

    Attributes:
        discount_percentage: The discount percentage (0-100)
        reason: Human-readable explanation of why this discount was applied
    """

    discount_percentage: Decimal
    reason: str

    def __post_init__(self) -> None:
        """Validate value object invariants."""
        if self.discount_percentage < 0:
            raise ValueError("discount_percentage must be non-negative")
        if self.discount_percentage > 100:
            raise ValueError("discount_percentage cannot exceed 100")
