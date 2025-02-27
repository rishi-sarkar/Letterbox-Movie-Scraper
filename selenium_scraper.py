from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time


def scrape_letterboxd_movies_and_ratings(username_to_scrape):
    """
    Scrape all films and ratings from a Letterboxd user's profile,
    with extra debugging to help diagnose issues.
    """

    # Set up headless Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=chrome_options)

    page = 1
    results = []

    while True:
        # Replace with your target URL
        url = f"https://letterboxd.com/{username_to_scrape}/films/page/{page}/"
        driver.get(url)

        print(f"\n--- Scraping page {page} ---")
        print(f"Request URL: {url}")
        # Wait for the JavaScript to load the content (adjust timing as needed)
        time.sleep(1)

        # Get the rendered HTML and parse it with BeautifulSoup
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # Find all film containers on this page
        film_containers = soup.find_all("li", class_="poster-container")
        print(f"Found {len(film_containers)} film containers on this page.")

        # If there are no films, we've likely reached the end
        if not film_containers:
            print("No film containers found; assuming end of results.")
            break

        for container in film_containers:
            title_text = None
            user_rating = None
            # Extract the data-film-name attribute
            frame_title = container.find("span", class_="frame-title")
            if frame_title:
                title_text = frame_title.text.strip()

            rating = container.find(
                "span", class_="rating")
            if rating:
                rating = rating.get_text()
                user_rating = rating.count('★') + float(rating.count('½'))/2

            results.append({
                "film_name": title_text,
                "rating": user_rating
            })
        page += 1

    driver.quit()

    return results


if __name__ == "__main__":
    # Replace with any Letterboxd username you want to debug
    username_to_scrape = "shreysinha"
    data = scrape_letterboxd_movies_and_ratings(username_to_scrape)

    print("\n--- FINAL RESULTS ---")
    for entry in data:
        print(f"Movie: {entry['film_name']} | Rating: {entry['rating']}")

    """Save the scraped movie data to a text file."""
    with open("letterboxd_movies.txt", "w", encoding="utf-8") as file:
        for entry in data:
            file.write(
                f"{entry['film_name']},{entry['rating']}\n")
            # f"Movie: {entry['film_name']} | Rating: {entry['rating']}\n")
    print(f"Results saved to letterboxd_movies.txt")
