# PDF to JPEG Converter

This Flask application converts PDF files to JPEG images and downloads them as a ZIP archive.

## Prerequisites

Before running the application, ensure you have the following installed:

* **Python 3.6+:** You can download it from [python.org](https://www.python.org/downloads/).
* **pip:** Python's package installer (usually included with Python).
* **Poppler:** Required by the `pdf2image` library. See installation instructions below.

## Installation

1.  **Clone the repository (or download the files):**

    ```bash
    git clone https://github.com/pillaiharish/ForgeHub.git
    cd ForgeHub/data-processing-tools/image-processing/pdf-to-jpeg-converter
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python3 -m venv myenv
    source myenv/bin/activate  

    ```

3.  **Install the required Python packages:**

    ```bash
    pip install Flask pdf2image Pillow
    ```

4.  **Install Poppler:**

    * **macOS (using Homebrew):**
        ```bash
        brew install poppler
        ```
    * **Linux (Ubuntu/Debian):**
        ```bash
        sudo apt-get update
        sudo apt-get install poppler-utils
        ```
    * **Linux (Fedora/CentOS/RHEL):**
        ```bash
        sudo dnf install poppler-utils
        ```
    * **Windows:**
        * Download Poppler binaries from a reliable source.
        * Extract the archive.
        * Add the `bin` directory of the extracted Poppler folder to your system's PATH environment variable.
        * Restart your command prompt after adding to path.

5.  **Create the necessary directories (if not present):**

    ```bash
    mkdir uploads downloads
    ```

## Running the Application

1.  **Start the Flask application:**

    ```bash
    python app.py
    ```

2.  **Open your web browser and navigate to:**

    ```
    [http://0.0.0.0:5001/](https://www.google.com/search?q=http://0.0.0.0:5001/)
    ```

3.  **Upload a PDF file using the form.**

4.  **Click the "Convert" button.**

5.  **You will be redirected to a result page with a download link for the ZIP archive containing the JPEG images.**

## Application Structure

* `app.py`: The main Flask application file.
* `templates/`: Contains the HTML templates for the web pages.
    * `index.html`: The main upload form page.
    * `result.html`: The result page with the download link.
* `uploads/`: Stores the uploaded PDF files.
* `downloads/`: Stores the generated JPEG images and ZIP archives.

## Important Notes

* Ensure that Poppler's `pdfinfo` utility is accessible from your system's PATH.
* The application saves uploaded PDF files to the `uploads/` directory and generated files to the `downloads/` directory. These directories must exist.
* The application runs on host 0.0.0.0, and port 5001. If you need a different setting, change the app.run parameters.
* The debug setting is set to true. Change to false for production.
