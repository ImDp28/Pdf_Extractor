# PDF Outline Extractor

This solution extracts structured outlines—including the title and headings (H1, H2, H3)—from PDF files and outputs them in a JSON format. It is designed to be run within a Docker container and works completely offline.

## **Approach**

The core of the solution is a Python script that uses the `PyMuPDF` library to analyze the content of PDF files. The process for identifying the title and headings is as follows:

1.  **Text Block Analysis:** The script iterates through each page of the PDF, extracting all text blocks along with their properties, such as font size, font name, and flags (e.g., bold).

2.  **Font Size Statistics:** It calculates the most common font size in the document to establish a baseline for normal text. This helps in distinguishing headings, which are typically larger.

3.  **Title Identification:** The title is assumed to be the text with the largest font size, usually found on the first page of the document.

4.  **Heading Classification:**
    * Text blocks with a font size larger than the most common size are considered potential headings.
    * These potential headings are then grouped by font size to identify distinct heading levels.
    * The groups are sorted in descending order of font size, and the top three are designated as H1, H2, and H3, respectively.

5.  **JSON Output:** The extracted title and a chronologically sorted list of headings (with their level and page number) are compiled into a dictionary and then written to a JSON file.

This method avoids hardcoding and is robust enough to handle variations in PDF formatting without relying on simple font size rules alone.

## **Libraries Used**

* **PyMuPDF (fitz):** A high-performance Python library for data extraction from PDF documents.

## **How to Build and Run**

The solution is containerized using Docker and is designed to process all PDF files from an input directory and save the resulting JSON files to an output directory.

### **Prerequisites**

* Docker must be installed on your system.

### **Build the Docker Image**

To build the Docker image, run the following command from the root directory of the project:

```bash
docker build --platform linux/amd64 -t pdf-outline-extractor .