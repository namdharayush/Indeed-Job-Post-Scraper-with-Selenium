# Indeed-Job-Post-Scrape-with-Selenium

A Python-based web scraper that automates the process of scraping job postings from Indeed. The scraper fetches job details, stores them in a MongoDB database, and saves the data to a CSV file.

## Features

- Scrapes job postings based on keywords and locations.
- Stores job data in a MongoDB database and saves it to a CSV file.
- Filters jobs based on posting date (last 14 days).
- Includes retry mechanisms for handling potential CAPTCHA or blocking issues.

## Prerequisites

- Python 3.7 or higher
- Google Chrome
- MongoDB
- ChromeDriver

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/namdharayush/Indeed-Job-Post-Scraper-with-Selenium.git

    ```

2. **Install the required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up MongoDB:**
    - Ensure MongoDB is installed and running on your local machine.
    - Modify the `Indeed_Mongo` class in `indeed_mongo.py` if needed to match your MongoDB connection settings.

4. **Download ChromeDriver:**
    - Download the ChromeDriver version compatible with your Chrome browser from [here](https://sites.google.com/a/chromium.org/chromedriver/).
    - Place the `chromedriver` executable in your system's PATH.

## Usage

1. **Run the scraper:**
    ```bash
    python indeed_scraper.py
    ```

2. **Modify Keywords and Locations:**
    - In the `scrape` method, modify the `keywords` dictionary to include your desired job titles and locations.

3. **CSV Output:**
    - The scraped data will be saved to `indeed.csv` in the project directory.

## MongoDB Integration

- The scraper saves all job postings to a MongoDB database named `indeed` under the `jobs` collection.
- The `Indeed_Mongo` class handles all MongoDB operations, including inserting job data and clearing old jobs (14 days or older).

## Customization

- **User-Agent:**
    - The `IndeedScraper` class allows for user-agent customization via the `fake_useragent` library (commented out in the code).

- **Retry Mechanism:**
    - Customize the retry mechanism in the `all_jobs_for_while` method to suit your needs.

## Troubleshooting

- **CAPTCHA Handling:**
    - If the scraper gets blocked by CAPTCHA, you can add or modify the retry logic to handle it more effectively.

- **No Jobs Found:**
    - If no jobs are found, ensure the XPath selectors are up to date as Indeed's structure may change.

## Thanks.
# Indeed-Job-Post-Scraped-with-Selenium
