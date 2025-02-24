
import requests
from bs4 import BeautifulSoup

# URL of the website
url = "http://books.toscrape.com/"

# Send a GET request to fetch the raw HTML content
response = requests.get(url)

# Parse the page content using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find all book containers (each book is within a `article` tag with class `product_pod`)
books = soup.find_all('article', class_='product_pod')

# Loop through each book and extract details
for book in books:
    # Get the book title
    title = book.find('h3').find('a')['title']
    
    # Get the book price
    price = book.find('p', class_='price_color').text
    
    # Get the book's link
    link = book.find('h3').find('a')['href']
    
    # Print the details
    print(f"Title: {title}")
    print(f"Price: {price}")
    print(f"Link: {url + link}")
    print("-" * 50)