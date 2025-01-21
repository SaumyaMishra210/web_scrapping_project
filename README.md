---

# Web Scraping Project: Books to Scrape

## Overview

This project involves scraping book data from the **Books to Scrape** website. The script fetches details such as book titles, prices, and ratings from multiple pages on the website. It is designed to handle pagination and store the scraped data in a structured format, such as a CSV file.

## Features

- Scrapes book data from **all pages** of the website.
- Extracts the following information for each book:
  - Title
  - Price
  - Rating
  - Availability (In stock or out of stock)
  - Category
- Handles **pagination** to fetch data from multiple pages.
- Saves the scraped data in a **CSV file** for easy analysis and storage.
- Optional: Download **thumbnail images** and save them locally.

## Requirements

- Python 3.x
- `requests` library
- `beautifulsoup4` library

To install the required dependencies, run the following command:

```bash
pip install requests beautifulsoup4
```

## Usage

1. Clone this repository to your local machine:

```bash
git clone https://github.com/your-username/books-scraping-project.git
cd books-scraping-project
```

2. Run the Python script to scrape data:

```bash
python scrape_books.py
```

The script will output the scraped book details and save the data in a CSV file named `books_data.csv`.

### Example Output (CSV)
The script will save the scraped data in a CSV file with the following columns:
- **Title**: Book title
- **Price**: Book price
- **Stock Availability**: Whether the book is in stock or not
- **Rating**: Book rating (e.g., "Three", "Five")
- **Category**: Book category
- **Product Page URL**: The URL to the individual book's page

## File Structure

```
books-scraping-project/
│
├── scrape_books.py            # Python script to scrape book data
├── books_data.csv             # CSV file where scraped data is saved
├── thumbnails/                # Folder to store book thumbnail images (optional)
├── README.md                  # Project documentation
└── requirements.txt           # List of required Python libraries
```

## How It Works

1. **Fetching Pages**: The script starts by fetching the first page of the website.
2. **Scraping Data**: For each page, the script extracts:
   - Book title
   - Book price
   - Book rating
   - Stock availability
   - Category
3. **Pagination**: After scraping the data from a page, the script checks for the presence of a "next" button and proceeds to the next page.
4. **Saving Data**: All scraped data is stored in a CSV file for further analysis.
5. **(Optional) Image Download**: The script can download and store the book's thumbnail image in a local folder.

