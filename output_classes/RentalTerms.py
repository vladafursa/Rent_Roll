from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from typing import List, Optional


class PaymentFrequency(Enum):
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    ANNUALLY = "annually"


@dataclass
class RentComponent:
    name: str
    amount: Decimal
    frequency: PaymentFrequency = PaymentFrequency.MONTHLY
    description: Optional[str] = None


@dataclass
class RentalTerms:
    base_rent_amount: Decimal
    base_rent_frequency: PaymentFrequency = PaymentFrequency.MONTHLY
    additional_rent_components: List[RentComponent] = field(default_factory=list)
    security_deposit: Optional[Decimal] = None
