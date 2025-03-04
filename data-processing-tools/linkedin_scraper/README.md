# LinkedIn Job Scraper

This Python script uses Selenium to scrape job postings from LinkedIn based on a specified keyword. It extracts job titles, company names, job descriptions, and relevant skills, then provides a count of the most frequently mentioned skills.

## Prerequisites

Before running the script, ensure you have the following installed:

* **Python 3.6+:** You can download it from [python.org](https://www.python.org/downloads/).
* **pip:** Python's package installer (usually included with Python).
* **Selenium:** `pip install selenium`
* **Chrome WebDriver:** Download the appropriate WebDriver for your Chrome version from [chromedriver.chromium.org](https://chromedriver.chromium.org/downloads). Place the executable in a directory included in your system's PATH.
* **Collections:** This is a default python library.
* **Chrome Browser:** This script uses Chrome browser.

## Installation

1.  **Clone the repository (or download the script):**

    ```bash
    git clone https://github.com/pillaiharish/ForgeHub.git
    cd ForgeHub/data-processing-tools/linkedin_scraper
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python3 -m venv myenv
    source myenv/bin/activate  # On macOS/Linux
    myenv\Scripts\activate  # On Windows
    ```

3.  **Install the required Python packages:**

    ```bash
    pip install selenium
    ```

4.  **Download and place the Chrome WebDriver:**
    * Download the correct chromedriver version for your chrome browser.
    * Place the chromedriver executable in a directory that is in your system's PATH.

## Running the Script

1.  **Run the Python script:**

    ```bash
    python linkedin_scraper.py
    ```

2.  **Modify the script as needed:**
    * Change the `keyword` variable to the job search term you want to use.
    * Adjust the `num_pages` variable to control how many pages of job listings are scraped.
    * Modify the `skills` list within the `extract_skills` function to include the skills you want to extract.
    * Adjust the url variable.

3.  **View the output:**
    * The script will print the job titles, company names, job links, and extracted skills.
    * It will also display a list of the most frequently mentioned skills and their counts.

## Script Functionality

* **`scrape_linkedin_jobs(keyword, num_pages)`:**
    * Opens a Chrome browser with Selenium.
    * Navigates to the LinkedIn job search page for the given keyword.
    * Scrolls down to load more job listings.
    * Extracts job titles, company names, job links, and job descriptions.
    * Extracts skills from the job descriptions.
    * Returns a list of extracted skills.
* **`extract_job_description(driver)`:**
    * Extracts the job description text from the job page.
* **`expand_description(driver)`:**
    * Clicks the show more button if it exists.
* **`extract_skills(description)`:**
    * Extracts skills from the job description based on a predefined list of skills.
* **Main execution block (`if __name__ == "__main__":`)**
    * Sets up the keyword and number of pages to scrape.
    * Calls the `scrape_linkedin_jobs` function.
    * Counts the occurrences of each skill.
    * Prints the most common skills.

## Notes

* LinkedIn's website structure may change, which could break the script. You may need to update the CSS selectors if this occurs.
* The script runs in headless mode, meaning you won't see the Chrome browser window. Remove the `--headless` argument from the Chrome options to see the browser.
* The script uses a basic skill extraction method. You can improve it by using more advanced techniques like natural language processing (NLP).
* The script is currently configured to scrape Golang developer jobs. Change the keyword and skills list to scrape other job types.