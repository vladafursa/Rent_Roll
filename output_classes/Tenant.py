import re
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class TenantType(Enum):
    INDUSTRIAL = "industrial"
    RESIDENTIAL = "residential"
    OTHER = "other"


@dataclass
class Tenant:
    name: str
    type: Optional[TenantType] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    tenant_id: Optional[str] = None

    def validate(self) -> List[str]:
        errors = []
        if not self.name:
            errors.append("Tenant name is required")
        if self.email and not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            errors.append(f"Invalid email format: {self.email}")
        return errors
