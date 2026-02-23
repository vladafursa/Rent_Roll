from dataclasses import dataclass
from datetime import date
from enum import Enum


class LeaseType(Enum):
    GROSS = "gross"
    NET = "net"
    TRIPLE_NET = "triple_net"
    PERCENTAGE = "percentage"


@dataclass
class LeaseDates:
    start_date: date
    end_date: date


@dataclass
class PremisesInfo:
    unit: str
    square_feet: float


@dataclass
class LeaseDetails:
    lease_type: LeaseType
    premises: PremisesInfo
    dates: LeaseDates
