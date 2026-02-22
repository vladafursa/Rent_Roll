import logging

import pymupdf

from constants import PDFType
from extractor.digital_pdf_parser import extract_digital_pdf_data
from extractor.scanned_pdf_parser import parse_scanned_pdf_data
from extractor.typization import recognise_pdf_type

logger = logging.getLogger(__name__)


def extract_text(path_to_pdf: str)->str:
    '''
    Extract text from all pages of a PDF, handling different page types appropriately.
    :param path_to_pdf: path to the PDF file
    :return:
    :raises: ValueError: If PDF is invalid
    '''
    doc = None
    text = []
    try:
        doc = pymupdf.open(path_to_pdf)
        logger.info(f"Processing PDF: {path_to_pdf} with {len(doc)} pages")
        for page_num, page in enumerate(doc, 1):
            page_type = recognise_pdf_type(page)
            logger.info(f"Page {page_num}: {page_type}")

            if page_type == PDFType.DIGITAL:
                text.append(extract_digital_pdf_data(page))
            elif page_type in [PDFType.SCANNED, PDFType.HYBRID]:
                text.append(parse_scanned_pdf_data(path_to_pdf, page_num))
            else:
                logger.warning(f"Page {page_num} has unknown type: {page_type}")
        return "\n".join(text)
    except Exception as e:
        logger.error(f"Failed to process PDF {path_to_pdf}: {e}")
        raise
    finally:
        if doc:
            doc.close()
