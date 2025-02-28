import requests
from bs4 import BeautifulSoup


def getTitle(film_url):
    base_url = "https://letterboxd.com"
    json_url = base_url + film_url + "json/"

    response = requests.get(json_url)
    data = response.json()

    # Navigate to the "film" key, then the "name" key
    film_name = data["name"]
    return film_name


def scrape_letterboxd_movies_and_ratings(username):
    """
    Scrape all films and ratings from a Letterboxd user's profile,
    with extra debugging to help diagnose issues.
    """

    page = 1
    results = []

    while True:
        url = f"https://letterboxd.com/{username}/films/page/{page}/"

        print(f"\n--- Scraping page {page} ---")
        print(f"Request URL: {url}")

        # Make the GET request with a custom user-agent
        response = requests.get(url)

        # If we don’t get 200, we stop
        if response.status_code != 200:
            print("Non-200 status code encountered. Stopping.")
            break

        # Parse the HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all film containers on this page
        film_containers = soup.find_all("li", class_="poster-container")
        print(f"Found {len(film_containers)} film containers on this page.")

        # If there are no films, we've likely reached the end
        if not film_containers:
            print("No film containers found; assuming end of results.")
            break

        for container in film_containers:
            film_div = container.find("div")
            if film_div:
                target_link = film_div.get("data-target-link")
                film_name = getTitle(target_link)
            else:
                print("Film div not found")
            rating = container.find(
                "span", class_="rating")
            user_rating = None
            if rating:
                rating = rating.get_text()
                user_rating = rating.count('★') + float(rating.count('½'))/2

            results.append({
                "film_name": film_name,
                "rating": user_rating
            })

        # Move on to the next page
        page += 1

    return results


if __name__ == "__main__":
    # Replace with Letterboxd username
    username_to_scrape = "username"
    data = scrape_letterboxd_movies_and_ratings(username_to_scrape)

    print("\n--- FINAL RESULTS ---")
    for entry in data:
        print(f"Movie: {entry['film_name']} | Rating: {entry['rating']}")