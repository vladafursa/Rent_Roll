from enum import IntEnum


# types of PDF blocks
class BlockType(IntEnum):
    TEXT = 0
    IMAGE = 1


TEXT_PERCENT_THRESHOLD = (
    0.01  # minimal percentage of text for page to be considered not scanned
)
IMAGE_PERCENT_SCANNED = (
    0.8  # minimal percentage of image cover to be considered as scanned
)
COVERAGE_OVERLAP_THRESHOLD = 1.5  # limit of overlapping

# Types of pdf documents
PDF_TYPE_SCANNED = "Scanned"
PDF_TYPE_DIGITAL = "Digital"
PDF_TYPE_HYBRID = "Hybrid"
