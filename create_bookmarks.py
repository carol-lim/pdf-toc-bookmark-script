import fitz  # PyMuPDF
import re

# Path to the input and output PDF files
pdf_path = "Carnegie's The Advantages of Human Nature.pdf"
output_path = "[Bookmark]Carnegie's The Advantages of Human Nature.pdf"

# Specify the page number containing the table of contents (0-based index)
toc_page_number = 1  # Adjust this to match the ToC page in your PDF

# Open the PDF
doc = fitz.open(pdf_path)

# Initialize bookmarks
toc = []
toc.append([1, "Menu", toc_page_number + 1])
# Extract links from the specified ToC page
toc_page = doc[toc_page_number]
links = toc_page.get_links()
print(links)

# Define regex patterns for "Part" and "Chapter" entries
part_pattern = r"(?i)(Part \w+ .*?)$"
chapter_pattern = r"(?i)(Chapter \d+ -.*?$)"


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
