import logging

logger = logging.getLogger(__name__)


def extract_digital_pdf_data(page) -> str:
    """
    Extract text from a digital PDF page.
    :param page: pymupdf.Page object representing a digital PDF
    :return: extracted text as a UTF-8 encoded string
    :raises RuntimeError: If text extraction fails
    """
    try:
        text = page.get_text()
        return text
    except Exception as e:
        logger.error(f"Failed to extract text from page: {e}")
        raise RuntimeError(f"Text extraction failed: {e}") from e
