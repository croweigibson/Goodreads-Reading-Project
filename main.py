import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {"User-Agent": "Mozilla/5.0"}
base_url = "https://www.goodreads.com/review/list/40791379?page="
books_list = []
page_num = 1

while True:
    response = requests.get(base_url + str(page_num), headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    books = soup.find_all("tr", class_="bookalike review")

    if not books:
        break  # Exit when no more books are found

    for book in books:
        try:
            title = book.find('td', class_='field title').find('div', class_='value').get_text(strip=True)
            author = book.find('td', class_='field author').find('div', class_='value').find('a').get_text(strip=True)
            rating = book.find('td', class_='field rating').find('div', class_='value').get_text(strip=True)
            avg_rating = book.find('td', class_='field avg_rating').find('div', class_='value').get_text(strip=True)
            date_added = book.find('td', class_='field date_added').find('div', class_='value').get_text(strip=True)
            num_pages = book.find('td', class_='field num_pages').find('div', class_='value').get_text(strip=True)
        except AttributeError:
            continue  # Skip if any field is missing

        books_list.append({
            "Title": title,
            "Author": author,
            "Rating": rating,
            "Avg Rating": avg_rating,
            "Date Added": date_added,
            "Num Pages": num_pages
        })

    print(f"Scraped page {page_num} ✅")
    page_num += 1

# Save to CSV
df = pd.DataFrame(books_list)
df.to_csv("goodreads_books.csv", index=False)
print(f"✅ Finished! Total books collected: {len(df)}")
