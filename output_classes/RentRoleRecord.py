from dataclasses import dataclass

from output_classes.LeaseDetails import LeaseDetails
from output_classes.RentalTerms import RentalTerms
from output_classes.Tenant import Tenant


@dataclass
class RentRollRecord:
    tenant: Tenant
    rental_terms: RentalTerms
    lease: LeaseDetails
