# Accessed and modified from: https://stackoverflow.com/a/67938713
import logging

import fitz

from constants import BlockType, PDFContentThresholds, PDFType

logger = logging.getLogger(__name__)


def recognise_pdf_type(page):
    """
    function that identifies page type based on text and image coverage.
    :params page: fitz.Page object
    :return:  string - type of pdf
    :raises ValueError: If page is invalid
    """

    if not page or not page.rect:
        logger.error(f"Invalid page object")
        raise ValueError("Invalid page object")
    try:
        page_area = abs(page.rect)  # calculating the whole area of the page

        if page_area <= 0:
            logger.warning(f"Page {page.number} his empty, treating as digital")
            return PDFType.DIGITAL  # Default for empty pages

        img_area = 0.0
        text_area = 0.0
        other_area = 0.0
        blocks = page.get_text("blocks")

        for block in blocks:
            rect = fitz.Rect(block[:4])
            block_type = block[
                6
            ]  # (x0, y0, x1, y1, "lines in block", block_no, block_type) - format of blocks
            if block_type == BlockType.IMAGE:  # block_type = 1 for images
                img_area += abs(rect)  # S
            elif block_type == BlockType.TEXT:  # block_type = 0 for text
                text_area += abs(rect)
            else:  # other types (vector graphic)
                other_area += abs(rect)

        total_covered = img_area + text_area + other_area
        if (
            total_covered > page_area * PDFContentThresholds.COVERAGE_OVERLAP
        ):  # check overlapping
            # normalise to scale
            scale = page_area / total_covered
            img_area *= scale
            text_area *= scale

        img_perc = img_area / page_area  # image area proportion
        text_perc = text_area / page_area  # text area proportion

        if text_perc < PDFContentThresholds.TEXT_PERCENT:  # No text = Scanned
            page_type = PDFType.SCANNED
        elif (
            img_perc > PDFContentThresholds.IMAGE_PERCENT
        ):  # Has text but very large images = hybrid
            page_type = PDFType.HYBRID
        else:
            page_type = PDFType.DIGITAL
        return page_type
    except Exception as e:
        logger.error(f"Error processing page {getattr(page, 'number', 'unknown')}: {e}")
        return PDFType.UNKNOWN
