# Accessed and modified from: https://stackoverflow.com/a/67938713
import logging
from typing import Tuple

import pymupdf

from constants import BlockType, PDFContentThresholds, PDFType

logger = logging.getLogger(__name__)


def recognise_pdf_type(page) -> PDFType:
    """
    identifies page type based on text and image coverage.
    :params page: pymupdf.Page object to analyze
    :return:  PDFType: SCANNED, DIGITAL, HYBRID, or UNKNOWN
    :raises ValueError: If page is invalid
    """

    _validate_page(page)

    try:
        page_area = abs(page.rect)  # calculating the whole area of the page

        if page_area <= 0:
            logger.warning(f"Page {page.number} his empty, treating as digital")
            return PDFType.DIGITAL  # Default for empty pages

        img_area, text_area, other_area = _calculate_areas(page)
        img_area, text_area, other_area = _scale(
            img_area, text_area, other_area, page_area
        )

        img_perc = _calculate_coverage(img_area, page_area)  # image area proportion
        text_perc = _calculate_coverage(text_area, page_area)  # text area proportion
        other_perc = _calculate_coverage(other_area, page_area)

        return _determine_page_type(text_perc, img_perc, other_perc)
    except Exception as e:
        logger.error(f"Error processing page {getattr(page, 'number', 'unknown')}: {e}")
        return PDFType.UNKNOWN


def _validate_page(page):
    """
    Validates page object
    :params page: pymupdf.Page object
    :raises ValueError: If page is invalid
    """
    if not page or not page.rect:
        logger.error("Invalid page object")
        raise ValueError("Invalid page object")


def _calculate_areas(page) -> Tuple[float, float, float]:
    """
    calculates the area that is covered by text, image, other
    :param page: pymupdf.Page object
    :return: image area, text area, other area
    """
    img_area = 0.0
    text_area = 0.0
    other_area = 0.0
    blocks = page.get_text("blocks")

    for block in blocks:
        rect = pymupdf.Rect(block[:4])
        block_type = block[
            6
        ]  # (x0, y0, x1, y1, "lines in block", block_no, block_type) - format of blocks
        if block_type == BlockType.IMAGE:  # block_type = 1 for images
            img_area += abs(rect)  # S
        elif block_type == BlockType.TEXT:  # block_type = 0 for text
            text_area += abs(rect)
        else:  # other types (vector graphic)
            other_area += abs(rect)

    return img_area, text_area, other_area


def _scale(
    img_area: float, text_area: float, other_area: float, page_area: float
) -> Tuple[float, float, float]:
    """
    Scale block areas if they overlap significantly.
    :param img_area: total area covered by images
    :param text_area: total area covered by text
    :param other_area: total area covered by other elements
    :param page_area: total area of the page
    :return: scaled areas (image, text, other)
    """
    total_covered = img_area + text_area + other_area
    if (
        total_covered > page_area * PDFContentThresholds.COVERAGE_OVERLAP
    ):  # check overlapping
        # normalise to scale
        scale = page_area / total_covered
        img_area *= scale
        text_area *= scale
        other_area *= scale
    return img_area, text_area, other_area


def _calculate_coverage(covered_area: float, total_area: float) -> float:
    return covered_area / total_area


def _determine_page_type(
    text_perc: float, img_perc: float, other_perc: float
) -> PDFType:
    """
    :param text_perc: percentage of text covering the page
    :param img_perc: percentage of image covering the page
    :param other_perc: percentage of othere types covering the page
    :return: string: type of pdf ("Scanned", "Digital", "Hybrid")
    """
    if text_perc < PDFContentThresholds.TEXT_PERCENT:  # No text = Scanned
        page_type = PDFType.SCANNED
    elif (
        img_perc > PDFContentThresholds.IMAGE_PERCENT
    ):  # Has text but very large images = hybrid
        page_type = PDFType.HYBRID
    else:
        page_type = PDFType.DIGITAL
    return page_type
