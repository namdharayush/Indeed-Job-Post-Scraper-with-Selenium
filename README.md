# Indeed Job Post Scraper with Selenium | Python-Based Web Scraper for Job Listings

This Python-based web scraper leverages Selenium to automate the extraction of job postings from Indeed.com. It's an ideal tool for developers, data scientists, and recruiters looking to gather job data efficiently. The scraper stores job details in a MongoDB database and exports the data to a CSV file for easy analysis.


### Key Features
- **Targeted Job Scraping:** Customize your search criteria with specific keywords and locations to gather the most relevant job postings.
- **Database & CSV Integration:** Effortlessly save scraped data into MongoDB and export it to CSV for easy access and analysis.
- **Smart Filtering:** Automatically filter job postings based on the latest posting dates (last 14 days).
- **Robust Retry Mechanism:** Utilize built-in retries to handle CAPTCHA challenges and minimize scraping interruptions.


### Prerequisites

- Python 3.7 or higher
- Google Chrome
- MongoDB
- ChromeDriver

### Installation Guide
Follow these steps to set up and run the Indeed Job Post Scraper on your local machine:


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
    - Download the ChromeDriver version compatible with your Chrome browser from [here](https://googlechromelabs.github.io/chrome-for-testing/).
    - Place the `chromedriver` executable in your system's PATH.

### Usage

1. **Run the scraper:**
    ```bash
    python indeed.py
    ```

2. **Modify Keywords and Locations:**
    - In the `scrape` method, modify the `keywords` dictionary to include your desired job titles and locations.

3. **CSV Output:**
    - The scraped data will be saved to `indeed.csv` in the project directory.

### Seamless MongoDB Database Integration

The scraper saves all job postings to a MongoDB database named `indeed` under the `jobs` collection. The `Indeed_Mongo` class manages all MongoDB operations, including inserting job data and clearing old postings (14 days or older).


### Customization
1. **User-Agent:**
   - Customize the user-agent in the `IndeedScraper` class using the `fake_useragent` library (commented out in the code).
2. **Retry Mechanism:**
   - Adjust the retry logic in the `all_jobs_for_while` method to suit your needs.

### Troubleshooting
1. **CAPTCHA Handling:**
   - If the scraper encounters CAPTCHA blocks, you can modify or add retry logic to handle it more effectively.
2. **No Jobs Found:**
   - If no jobs are found, ensure that the XPath selectors are current, as Indeed's website structure may change.

### Thanks.
