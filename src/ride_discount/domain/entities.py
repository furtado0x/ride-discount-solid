"""Domain entities for ride discount system."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Customer:
    """Customer entity representing a ride-sharing service user.

    Attributes:
        id: Unique customer identifier
        total_rides: Total number of rides completed by the customer
    """

    id: str
    total_rides: int

    def __post_init__(self) -> None:
        """Validate entity invariants."""
        if self.total_rides < 0:
            raise ValueError("total_rides must be non-negative")
