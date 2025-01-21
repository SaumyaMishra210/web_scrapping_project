import os
import requests
from bs4 import BeautifulSoup
import csv

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
BASE_PRODUCT_URL = "https://books.toscrape.com/catalogue/"
THUMBNAIL_FOLDER = "thumbnails"  # Folder to save images

# Ensure the thumbnail folder exists
os.makedirs(THUMBNAIL_FOLDER, exist_ok=True)

def sanitize_filename(title):
    """Sanitize the filename to remove invalid characters."""
    # Replace slashes and other invalid characters
    invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|', ',', '.']
    for char in invalid_chars:
        title = title.replace(char, "_")  # Replace with underscore
    return title

def download_thumbnail(thumbnail_url, title):
    """Download the thumbnail image and save it locally."""
    # Send a request to download the image
    response = requests.get(thumbnail_url)
    if response.status_code == 200:
        # Sanitize the title to ensure it is a valid filename
        safe_title = sanitize_filename(title)
        
        # Save the image as a file in the thumbnails folder
        image_filename = os.path.join(THUMBNAIL_FOLDER, f"{safe_title}.jpg")
        with open(image_filename, "wb") as file:
            file.write(response.content)
        print(f"Thumbnail image for '{safe_title}' saved.")
    else:
        print(f"Failed to download image for '{title}'.")

def scrape_product_details(product_url):
    """Scrape additional details from the individual product page."""
    response = requests.get(product_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        
        try:
            product_title = soup.find("div", {"class": "col-sm-6 product_main"}).find("h1").text
            product_price = soup.find("div", {"class": "col-sm-6 product_main"}).find("p", {"class": "price_color"}).text
            product_availability = soup.find("div", {"class": "col-sm-6 product_main"}).find("p", {"class": "instock availability"}).text.strip()
            product_description = soup.find("div", {"id": "product_description"}).find_next_sibling("p")
            product_description = product_description.text.strip() if product_description else "No description available"
            product_rating = soup.find("div", {"class": "col-sm-6 product_main"}).find("p", {"class": "star-rating"})["class"][1]
            product_category = soup.find("ul", {"class": "breadcrumb"}).find_all("a")[2].text.strip()
            
            # Return the product details
            return {
                "Title": product_title,
                "Price": product_price,
                "Availability": product_availability,
                "Rating": product_rating,
                "Category": product_category,
                "Description": product_description,
                "URL": product_url
            }
        except AttributeError:
            print(f"Error extracting details from {product_url}")
            return None
    else:
        print(f"Failed to fetch the product page. Status code: {response.status_code}")
        return None

def scrape_books():
    page = 1
    all_books = []  # List to store data from all pages

    while True:
        # Generate URL for the current page
        url = BASE_URL.format(page)
        
        # Make a GET request
        response = requests.get(url)
        
        # Check if the page exists
        if response.status_code != 200:
            print("No more pages to scrape.")
            break
        
        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Find all book containers
        books = soup.find_all("article", class_="product_pod")
        
        # Extract data for each book
        for book in books:
            title = book.h3.a["title"]  # Book title
            price = book.find("p", class_="price_color").text  # Price
            # Construct the product URL
            product_url = BASE_PRODUCT_URL + book.h3.a["href"].replace("../../", "")
            
            # Extract the thumbnail URL
            thumbnail_url = "https://books.toscrape.com/" + book.find("img")["src"].replace("../../", "")
            
            # Download the thumbnail image
            download_thumbnail(thumbnail_url, title)
            
            product_details = scrape_product_details(product_url)  # Scrape additional details
            
            if product_details:
                # Combine basic data and additional details
                product_details["Title"] = title
                product_details["Price"] = price
                all_books.append(product_details)
        
        # Move to the next page
        page += 1

    return all_books

def save_to_csv(books_data, filename="books_data.csv"):
    """Save the scraped book data into a CSV file."""
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=books_data[0].keys())
        
        # Write the header
        writer.writeheader()
        
        # Write the book data
        writer.writerows(books_data)
        print(f"Data saved to {filename}")

# Run the scraper
books_data = scrape_books()

# Save the scraped data to CSV
if books_data:
    save_to_csv(books_data)
else:
    print("No data to save.")
