import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

headers = {"User-Agent": "Mozilla/5.0"}
base_url = "https://www.goodreads.com/review/list/40791379?page="
books_list = []
page_num = 1

while True:
    print(f"Scraping page {page_num}...")
    response = requests.get(base_url + str(page_num), headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    books = soup.find_all("tr", class_="bookalike review")

    if not books:
        print("No more books found, ending scrape.")
        break  # no more books, stop scraping

    for book in books:
        try:
            title = book.find('td', class_='field title').find('div', class_='value').get_text(strip=True)
            author = book.find('td', class_='field author').find('div', class_='value').find('a').get_text(strip=True)
            rating = book.find('td', class_='field rating').find('div', class_='value').get_text(strip=True)
            avg_rating = book.find('td', class_='field avg_rating').find('div', class_='value').get_text(strip=True)
            date_added = book.find('td', class_='field date_added').find('div', class_='value').get_text(strip=True)
            num_pages = book.find('td', class_='field num_pages').find('div', class_='value').get_text(strip=True)

            # Get book URL
            book_link_tag = book.find('td', class_='field title').find('div', class_='value').find('a')
            book_url = "https://www.goodreads.com" + book_link_tag['href'] if book_link_tag else None

            genre = "Unknown"
            if book_url:
                # Request the book page and parse genres
                book_resp = requests.get(book_url, headers=headers)
                book_soup = BeautifulSoup(book_resp.text, "lxml")

                genre_container = book_soup.find("div", attrs={"data-testid": "genresList"})
                if genre_container:
                    first_genre_span = genre_container.find("span", class_="Button__labelItem")
                    if first_genre_span:
                        genre = first_genre_span.get_text(strip=True)

                # Polite pause so Goodreads doesn't block you
                time.sleep(random.uniform(1, 2))

            books_list.append({
                "Title": title,
                "Author": author,
                "Rating": rating,
                "Avg Rating": avg_rating,
                "Date Added": date_added,
                "Num Pages": num_pages,
                "Genre": genre
            })

        except AttributeError:
            continue  

    page_num += 1

df = pd.DataFrame(books_list)
df.to_csv("books_data.csv", index=False)
print(f"\n✅ Finished! Total books collected: {len(df)}")
