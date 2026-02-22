from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from enum import Enum
from typing import List, Optional


class PaymentFrequency(Enum):
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    SEMI_ANNUALLY = "semi_annually"
    ANNUALLY = "annually"


@dataclass
class RentComponent:
    name: str
    amount: Decimal
    frequency: PaymentFrequency = PaymentFrequency.MONTHLY
    description: Optional[str] = None


@dataclass
class RentEscalation:
    effective_date: date
    new_base_rent: Decimal
    description: Optional[str] = None


@dataclass
class RentalTerms:
    base_rent_amount: Decimal
    base_rent_frequency: PaymentFrequency = PaymentFrequency.MONTHLY
    additional_rent_components: List[RentComponent] = field(default_factory=list)
    escalations: List[RentEscalation] = field(default_factory=list)
    security_deposit: Optional[Decimal] = None
    rent_abatement: Optional[str] = None

    def total_monthly_rent(self) -> Decimal:
        total = self.base_rent_amount
        for comp in self.additional_rent_components:
            if comp.frequency == PaymentFrequency.MONTHLY:
                total += comp.amount
            elif comp.frequency == PaymentFrequency.QUARTERLY:
                total += comp.amount / 3
            elif comp.frequency == PaymentFrequency.ANNUALLY:
                total += comp.amount / 12

        return total
