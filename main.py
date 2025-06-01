import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

headers = {"User-Agent": "Mozilla/5.0"}
base_url = "https://www.goodreads.com/review/list/40791379?page="
books_list = []
page_num = 1

def get_open_library_genres(title, author):
    """Fetch genres from Open Library API"""
    query = f"{title} {author}".replace(" ", "+")
    url = f"https://openlibrary.org/search.json?q={query}"
    
    try:
        response = requests.get(url)
        data = response.json()
        if "docs" in data and data["docs"]:
            subjects = data["docs"][0].get("subject", [])
            return ", ".join(subjects) if subjects else "Unknown"
        else:
            return "Unknown"
    except Exception as e:
        print(f"Error fetching genre for '{title}': {e}")
        return "Unknown"

while True:
    response = requests.get(base_url + str(page_num), headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    books = soup.find_all("tr", class_="bookalike review")

    if not books:
        break  # no more books, exit

    for book in books:
        try:
            title = book.find('td', class_='field title').find('div', class_='value').get_text(strip=True)
            author = book.find('td', class_='field author').find('div', class_='value').find('a').get_text(strip=True)
            rating = book.find('td', class_='field rating').find('div', class_='value').get_text(strip=True)
            avg_rating = book.find('td', class_='field avg_rating').find('div', class_='value').get_text(strip=True)
            date_added = book.find('td', class_='field date_added').find('div', class_='value').get_text(strip=True)
            num_pages = book.find('td', class_='field num_pages').find('div', class_='value').get_text(strip=True)
            
            # Fetch genre from Open Library API
            genre = get_open_library_genres(title, author)
            
            # Slow down requests to avoid rate limits
            time.sleep(random.uniform(0.5, 1.5))

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
            continue  # Skip books with missing data

    print(f"Scraped page {page_num} ✅")
    page_num += 1

# Save to a new CSV file
df = pd.DataFrame(books_list)
df.to_csv("books_data2.csv", index=False)
print(f"✅ Finished! Total books collected: {len(df)}")
