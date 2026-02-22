from dataclasses import dataclass
from enum import Enum, IntEnum
from typing import Final


# types of PDF blocks
class BlockType(IntEnum):
    TEXT = 0
    IMAGE = 1


@dataclass(frozen=True)
class PDFContentThresholds:
    TEXT_PERCENT: Final[
        float
    ] = 0.01  # minimal percentage of text for page to be considered not scanned
    IMAGE_PERCENT: Final[
        float
    ] = 0.8  # minimal percentage of image cover to be considered as scanned
    COVERAGE_OVERLAP: Final[float] = 1.5  # limit of overlapping


# Types of pdf documents
class PDFType(str, Enum):
    SCANNED = "Scanned"
    DIGITAL = "Digital"
    HYBRID = "Hybrid"

    def __str__(self):  # nice output
        return self.value
