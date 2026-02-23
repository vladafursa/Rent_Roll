from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import List, Optional


class LeaseType(Enum):
    GROSS = "gross"
    NET = "net"
    DOUBLE_NET = "double_net"
    TRIPLE_NET = "triple_net"
    MODIFIED_GROSS = "modified_gross"
    PERCENTAGE = "percentage"


@dataclass
class LeaseOptions:
    renewal_options: List[str] = field(default_factory=list)
    termination_options: List[str] = field(default_factory=list)
    right_of_first_refusal: bool = False
    expansion_options: List[str] = field(default_factory=list)


@dataclass
class LeaseDates:
    start_date: date
    end_date: date
    lease_term_years: Optional[float] = None
    renewal_deadline: Optional[date] = None
    termination_notice_date: Optional[date] = None


@dataclass
class PremisesInfo:
    unit: str
    square_feet: float
    description: Optional[str] = None
    floor: Optional[str] = None
    building: Optional[str] = None


@dataclass
class LeaseDetails:
    lease_type: LeaseType
    premises: PremisesInfo
    dates: LeaseDates
    options: LeaseOptions = field(default_factory=LeaseOptions)
    tenant_improvement_allowance: Optional[str] = None
    tenant_obligations: List[str] = field(default_factory=list)
    special_provisions: List[str] = field(default_factory=list)
