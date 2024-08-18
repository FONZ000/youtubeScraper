# Email Scraper for Playboard

This script scrapes email addresses from Playboard based on user-defined criteria. It uses `Selenium` to interact with the website and `BeautifulSoup` to parse the HTML content. The extracted emails are saved into a CSV file.

## Features

- Scrapes emails based on category, date range, country, and subscriber count.
- Saves the emails to a CSV file.
- Allows setting a limit on the number of emails to scrape.

## Requirements

- Python 3.x
- Selenium
- BeautifulSoup4
- Chrome WebDriver

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/email-scraper.git
    cd email-scraper
    ```

2. **Install the required Python packages**:

    ```bash
    pip install selenium beautifulsoup4
    ```

3. **Download Chrome WebDriver**:

   Download the [Chrome WebDriver](https://sites.google.com/a/chromium.org/chromedriver/) corresponding to your Chrome version and place it in a directory included in your system's PATH.

## Usage

1. **Run the script**:

    ```bash
    python email_scraper.py
    ```

2. **Follow the on-screen prompts**:
    - Enter the category (e.g., Crypto, Tech review) or press ENTER for no category.
    - Enter the number of emails you want to scrape.
    - Set subscriber range, date range, and country if desired.

3. **The script will**:
    - Navigate to the Playboard search results.
    - Scroll through the page to load content.
    - Extract emails from the descriptions.
    - Save the emails to a CSV file named `scraped_data.csv`.

## Configuration

- **Email Limit**: Set the number of emails to scrape. The script will stop once this limit is reached.
- **Subscriber Range**: Specify a range of subscribers for the channels you want to target.
- **Date Range**: Choose between the last 15 or 30 days of promotion activity.
- **Country**: Select the country to filter channels by.

## Example

```plaintext
Category examples: Crypto, Tech review, travelling, programming, ..., etc
Please enter the category you desire (Press ENTER if you don't want a category): programming
Please enter the number of emails you want to scrape: 500
Enter subscribers minimum bound of range: 1000
Enter subscribers maximum bound of range: 50000
Choose last promotion if you don't want to choose just press 0!:
1: Past 15 days
2: past 30 days
Enter subscribers range (1 or 2): 1
Choose Country if you don't want to choose just press 0!:
1: Russian Federation
2: United States
3: United Kingdom
4: Canada
5: France
6: Japan
7: India
Choose country if you don't want to choose just press 0!: 2
