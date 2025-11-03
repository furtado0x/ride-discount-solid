"""Use case for calculating ride discounts."""

from decimal import Decimal

from ride_discount.application.dtos import RideContext
from ride_discount.domain.rules.base import DiscountRule
from ride_discount.domain.value_objects import DiscountResult


class CalculateRideDiscountUseCase:
    """Use case for calculating final ride price with applicable discounts.

    This use case orchestrates all registered discount rules and applies them
    to calculate the final price, respecting a maximum total discount cap.

    Attributes:
        MAX_TOTAL_DISCOUNT: Maximum allowed total discount percentage (50%)
    """

    MAX_TOTAL_DISCOUNT = Decimal("50")

    def execute(self, context: RideContext) -> tuple[Decimal, list[DiscountResult]]:
        """Execute the use case to calculate final ride price.

        Args:
            context: The ride context containing all necessary information

        Returns:
            A tuple containing:
                - final_price: The final price after all discounts
                - applied_discounts: List of all discounts that were applied
        """
        applied_discounts = [
            discount_result
            for rule_class in DiscountRule.registered_rules
            if (discount_result := rule_class().calculate_discount(context))
        ]

        total_discount_percentage = min(
            sum((d.discount_percentage for d in applied_discounts), Decimal("0")),
            self.MAX_TOTAL_DISCOUNT,
        )

        discount_amount = context.base_price * (total_discount_percentage / Decimal("100"))
        final_price = context.base_price - discount_amount

        return final_price, applied_discounts
