# Document Processing Pipeline

## Overview

This project implements a modular pipeline for automated text extraction from the PDF documents.

PDF files often contain a mixture of:

- Digital text documents
- Scanned pages
- Hybrid documents

A single extraction strategy is not sufficient. This system automatically detects the type of each page and applies an appropriate extraction method.

The pipeline is designed with a modular architecture allowing additional processing stages to be added in the future.

---

## Features

### Automatic PDF Typization

Each page is classified as:

- Digital PDF
- Scanned PDF
- Hybrid PDF

Classification is based on structural analysis of page content:

- Text coverage
- Image coverage
- Vector graphics

This allows the system to choose the correct extraction strategy automatically.


#### Digital PDFs

Digital pages are processed using direct text extraction.

Advantages:

- Fast
- Accurate
- Preserves original text

---

#### Scanned PDFs

Scanned pages are processed using OCR.

Pipeline:
PDF → Image → OCR → Text
Steps:

1. Convert PDF page to image
2. Validate image
3. Apply OCR
4. Return extracted text

OCR is implemented using Tesseract.

---

#### Hybrid PDFs

Hybrid pages are treated as scanned documents.

This ensures text embedded inside images is captured reliably.

---

## Architecture

### High-Level Pipeline
PDF
↓
Page Iteration
↓
Page Type Detection
↓
Extraction Strategy Selection
↓
Text Extraction
↓
Output

### Robust Error Handling

The system includes structured error handling:

- Invalid PDFs detected
- Corrupted images handled
- OCR failures reported
- Logging for debugging
---

### Logging

Structured logging is implemented across the system.

Example events:

- PDF opened
- Page classified
- OCR completed
- Errors detected

This makes the pipeline production-friendly.

---

## Technologies

- Python
- PyMuPDF
- Tesseract OCR
- pdf2image
- Pillow

---
