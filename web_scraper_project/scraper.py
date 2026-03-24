import requests
from bs4 import BeautifulSoup
import pandas as pd
import schedule
import time
import datetime

def scrape():
    print("Scraping started...")

    url = "https://quotes.toscrape.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    quotes = []
    authors = []

    # Clean quotes
    for quote in soup.find_all("span", class_="text"):
        clean_quote = quote.text.replace("“", "").replace("”", "").replace('"', "")
        quotes.append(clean_quote)

    # Clean authors
    for author in soup.find_all("small", class_="author"):
        authors.append(author.text.strip())

    # Create DataFrame with timestamp
    data = pd.DataFrame({
        "Quote": quotes,
        "Author": authors,
        "Time": datetime.datetime.now()
    })

    # Append data instead of overwrite
    data.to_csv("quotes.csv", index=False)

    print("Data updated ✅")

# Run once immediately
scrape()

# Schedule every 10 seconds (you can change later)
schedule.every(10).seconds.do(scrape)

print("Scheduler started...")

while True:
    schedule.run_pending()
    time.sleep(1)