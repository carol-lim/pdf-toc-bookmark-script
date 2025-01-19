import fitz  # PyMuPDF
import re
import os

def get_user_input():
    """Prompt user for input and handle exceptions."""
    while True:
        try:
            # Get the PDF file path
            pdf_path = input("Enter the path to the PDF file: ").strip()
            
            # Validate the file path
            with open(pdf_path, "rb"):
                pass  # Check if the file exists and is accessible
            
            # Get the TOC page range (1-based index)
            toc_page_input = input(
                "Enter the Table of Content page(s) (e.g., 2 for single page or 2-4 for multiple pages): "
            ).strip()
                        
            # Parse the page input
            if "-" in toc_page_input:
                start, end = map(int, toc_page_input.split("-"))
                if start <= 0 or end <= 0 or start > end:
                    raise ValueError("Invalid range. Start and end must be positive, and start <= end.")
                toc_page_range = range(start, end + 1)
            else:
                single_page = int(toc_page_input)
                if single_page <= 0:
                    raise ValueError("Invalid page number. Page must be positive.")
                toc_page_range = range(single_page, single_page + 1)
            
            return pdf_path, toc_page_range  # Return as a range object
        
        except (ValueError, FileNotFoundError) as e:
            print(f"Error: {e}. Please try again.") 

def check_output_path(output_path):
    """Check if the output file already exists and append a number if necessary."""
    if os.path.exists(output_path):
        base, ext = os.path.splitext(output_path)
        counter = 1
        while os.path.exists(f"{base} ({counter}){ext}"):
            counter += 1
        # Return the new output path with a number in parentheses
        return f"{base} ({counter}){ext}"
    else:
        return output_path

# Get user inputs
pdf_path, toc_page_range = get_user_input()

# Specify the output file path
output_path = f"[Bookmark] {pdf_path.split('/')[-1]}"

# Check if the output path exists and handle overwriting
output_path = check_output_path(output_path)

# Open the PDF
doc = fitz.open(pdf_path)

# Initialize bookmarks
toc = []
toc.append([1, "Menu", toc_page_range.start])  # Use 1-based index for bookmarks

# Define regex patterns for "Part" and "Chapter" entries
part_pattern = r"(?i)(Part \w+ .*?)$"
chapter_pattern = r"(?i)(Chapter \d+ -.*?$)"

# Loop through specified TOC pages
for toc_page_number in toc_page_range:
    toc_page = doc[toc_page_number - 1]  # Convert to 0-based index
    links = toc_page.get_links()

    # Loop through links and add bookmarks
    for link in links:
        uri = link.get("uri")  # The hyperlink destination
        destination_page = link.get("page")  # Target page number (0-based index)

        if destination_page is not None:
            rect = link.get("from")  # Get the coordinates of the link
            text = toc_page.get_text("text", clip=rect)  # Extract text from the link's bounding box

            # If no text is extracted, use "Untitled" or a fallback
            title = text.strip() 

            if re.match(part_pattern, title, re.MULTILINE):
                # If the title matches "Part", append as Level 1
                toc.append([1, title, destination_page + 1])
            elif re.match(chapter_pattern, title, re.MULTILINE):
                # If the title matches "Chapter", append as Level 2
                toc.append([2, title, destination_page + 1])
            else:
                # Default to Level 1 for unmatched titles
                toc.append([1, title, destination_page + 1])

# Add bookmarks to the PDF
doc.set_toc(toc)

# Save the updated PDF
doc.save(output_path)
print(f"Bookmarks created and saved to {output_path}")
