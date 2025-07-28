import fitz  # PyMuPDF
import json
import os
import operator
from collections import defaultdict

def extract_outline(pdf_path):
    """
    Extracts the title and headings (H1, H2, H3) from a PDF file.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        dict: A dictionary containing the title and a list of headings.
    """
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"Error opening {pdf_path}: {e}")
        return None

    font_counts = defaultdict(int)
    potential_headings = []

    for page_num, page in enumerate(doc):
        blocks = page.get_text("dict", flags=fitz.TEXTFLAGS_FONT)
        for block in blocks["blocks"]:
            if "lines" in block:
                for line in block["lines"]:
                    if "spans" in line:
                        for span in line["spans"]:
                            font_counts[span["size"]] += 1
                            if span['flags'] & 2**4:  # Check for bold flag
                                potential_headings.append({
                                    "text": span["text"].strip(),
                                    "size": span["size"],
                                    "page": page_num + 1
                                })

    if not font_counts:
        return {"title": "", "outline": []}

    # Determine the most common font size to identify body text
    base_size = max(font_counts.items(), key=operator.itemgetter(1))[0]

    # Identify heading candidates (larger than base size)
    headings = [h for h in potential_headings if h["size"] > base_size]

    # Group headings by font size to determine levels
    size_to_level = defaultdict(list)
    for h in headings:
        size_to_level[h["size"]].append(h)

    # Sort font sizes to assign H1, H2, H3
    sorted_sizes = sorted(size_to_level.keys(), reverse=True)
    level_map = {size: f"H{i+1}" for i, size in enumerate(sorted_sizes[:3])}

    # Extract the final outline
    outline = []
    for size, mapped_level in level_map.items():
        for heading in size_to_level[size]:
            outline.append({
                "level": mapped_level,
                "text": heading["text"],
                "page": heading["page"]
            })

    # Sort the outline by page number and original position
    outline.sort(key=lambda x: (x["page"]))

    # Find the title (usually the largest text on the first page)
    title_text = ""
    if sorted_sizes:
        largest_size = sorted_sizes[0]
        for heading in size_to_level[largest_size]:
            if heading["page"] == 1:
                title_text = heading["text"]
                break
    # Fallback if no title is found
    if not title_text and doc and doc.page_count > 0:
        first_page_text = doc[0].get_text().split('\n')
        if first_page_text:
            title_text = first_page_text[0].strip()


    return {
        "title": title_text,
        "outline": outline
    }

def main():
    """
    Main function to process all PDFs in the input directory.
    """
    input_dir = "/app/input"
    output_dir = "/app/output"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(input_dir, filename)
            json_filename = os.path.splitext(filename)[0] + ".json"
            output_path = os.path.join(output_dir, json_filename)

            print(f"Processing {filename}...")
            outline_data = extract_outline(pdf_path)

            if outline_data:
                with open(output_path, 'w') as f:
                    json.dump(outline_data, f, indent=4)
                print(f"Successfully generated {json_filename}")

if __name__ == "__main__":
    main()