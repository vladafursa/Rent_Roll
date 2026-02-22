import logging
import os

import pytesseract
from pdf2image import convert_from_path
from PIL import Image

from constants import OUTPUT_DIR

logger = logging.getLogger(__name__)


def parse_scanned_pdf_data(path_to_pdf: str, page_num: int) -> str:
    """
    Extract text from a scanned PDF page by converting to image and applying OCR
    :param path_to_pdf: path to the source PDF file
    :param page_num: page number to process
    :return: extracted text from the scanned page
    :raises RuntimeError If OCR fails or temporary files cannot be created
    """
    try:
        image_path = _find_image_path(path_to_pdf, page_num)
        _convert_to_image(path_to_pdf, image_path)
        return _extract_scanned_pdf_data(image_path)
    except (ValueError, RuntimeError) as e:
        logger.error(f"Failed to process scanned page {page_num}: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error processing page {page_num}: {e}")
        raise RuntimeError(f"Failed to parse scanned PDF data: {e}") from e


def _convert_to_image(path_to_pdf: str, output_path: str) -> None:
    """
    Converts page into jpg image
    :param path_to_pdf: path to the input PDF file
    :param output_path: path where the output JPEG image will be saved
    :return: None
    :raises IOError: If the output file cannot be written
    """
    try:
        image = convert_from_path(path_to_pdf)

        # check if any pages were converted
        if not image:
            raise ValueError(f"No pages found in PDF: {path_to_pdf}")

        image[0].save(output_path, "JPEG")
        logger.info(f"Successfully converted {path_to_pdf} to {output_path}")

    except PermissionError as e:
        logger.error(f"Permission denied: {e}")
        raise IOError(f"Cannot write to {output_path}") from e
    except Exception as e:
        logger.error(f"Unexpected error converting PDF to image: {e}")
        raise RuntimeError(f"PDF conversion failed: {e}") from e


def _find_image_path(path_to_pdf: str, page_num: int) -> str:
    """
    Generate output path for a converted PDF page image.
    :param path_to_pdf: full path to the source PDF file
    :param page_num: page number to include in filename
    :return: full path to the output image file
    """
    try:
        file_name_with_extension = os.path.basename(path_to_pdf)
        file_name = os.path.splitext(file_name_with_extension)
        new_file_name = file_name[0] + str(page_num) + ".jpg"
        output_path = os.path.join(OUTPUT_DIR, new_file_name)
        logger.debug(f"Generated output path: {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"Failed to generate output path: {e}")
        raise RuntimeError(f"Could not generate output path for {path_to_pdf}") from e


def _extract_scanned_pdf_data(image_path: str) -> str:
    """
    Extract text from a scanned PDF page image using OCR (Tesseract).
    :param image_path: path to the jpg file
    :return: extracted text from the image
    :raises RuntimeError: If Tesseract is not installed or OCR fails
    :raises ValueError: If the image is invalid or corrupted
    """
    try:
        with Image.open(image_path) as image:
            image.verify()  # verify image is valid
        with Image.open(image_path) as image:
            extracted_text = pytesseract.image_to_string(image)
            logger.info(
                f"Successfully extracted {len(extracted_text)} characters from {image_path}"
            )
            return extracted_text
    except (IOError, SyntaxError) as e:
        logger.error(f"Invalid or corrupted image: {image_path} - {e}")
        raise ValueError(f"Cannot read image file: {image_path}") from e
    except pytesseract.TesseractNotFoundError as e:
        logger.error("Tesseract is not installed or not in PATH")
        raise RuntimeError(
            "Tesseract OCR is not installed. Please install it:\n"
        ) from e
    except pytesseract.TesseractError as e:
        logger.error(f"Tesseract OCR error: {e}")
        raise RuntimeError(f"OCR processing failed: {e}") from e
    except Exception as e:
        logger.error(f"Unexpected error during OCR: {e}")
        raise RuntimeError(f"Failed to extract text from {image_path}") from e
