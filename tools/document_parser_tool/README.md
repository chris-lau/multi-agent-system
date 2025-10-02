# Document Parsing Tool

The Document Parsing Tool enables agents to parse content from various document formats such as PDF, DOCX, and TXT.

## Overview
This tool provides document parsing capabilities to agents in the Multi-Agent Research System. It allows agents to extract content from various document formats for analysis.

## Parameters
- `file_path` (string, required): Path to the document file to be parsed
- `format` (string, optional, default: "txt"): Document format (txt, pdf, docx, etc.)

## Output
The tool returns a structured response with:
- `file_path`: Path of the parsed document
- `format`: Format of the document
- `parsed_content`: Extracted text content from the document
- `metadata`: Metadata about the document (word count, page count, title)

## Usage Example
```json
{
  "file_path": "/path/to/document.pdf",
  "format": "pdf"
}
```

## Note
This is currently a mock implementation. In a real system, this would use libraries like PyPDF2 for PDF files and python-docx for Word documents.