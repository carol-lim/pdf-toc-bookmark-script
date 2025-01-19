# PDF Table of Contents Bookmarking Script

This script extracts the Table of Contents (ToC) from a PDF file and adds bookmarks to it. The user is prompted to provide the PDF file path and specify the page range containing the ToC. The script automatically generates an output PDF file with the added bookmarks.

## Features
- Extracts links from the specified ToC pages in the input PDF.
- Automatically assigns bookmarks to "Part" and "Chapter" headings.
- Handles user input for the file path and ToC page range.
- Automatically checks if the output file already exists and appends a number to the filename if needed.

## Prerequisites
- Python 3.x
- `PyMuPDF` library (install via `pip install pymupdf`)
- PDF file that contains Table of Content page(s) which titles are hyperlinked to content pages correctly

## Usage

1. Ensure you have Python 3.x installed on your system.
2. Install the required dependencies:
   ```bash
   pip install pymupdf
   ```
3. Run the script:
   ```bash
   python create_bookmarks.py
   ```
4. Follow the prompts to:
   - Enter the PDF file path (e.g., `input.pdf`).
   - Specify the page range of the Table of Contents (e.g., `2` or `2-4` for pages 2 to 4).
   - The script will handle naming the output file based on the input file name and will check for existing files.

5. The script will save the new PDF with the bookmarks in the same location as the input file.

## Example Output

```
Enter the PDF file path: Carnegie's The Advantages of Human Nature.pdf
Enter the TOC page range (e.g., 2-4): 2
Bookmarks created and saved to [Bookmark] Carnegie's The Advantages of Human Nature.pdf
```

![image](https://github.com/user-attachments/assets/aeabf9a5-b233-445b-afd2-871006ad1274)


## License
This script is open-source and available for personal or educational use. Feel free to contribute or modify the code.
```
