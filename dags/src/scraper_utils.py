import json
import requests
from bs4 import BeautifulSoup

urls = [
        "https://www.pricecharting.com/game/playstation-2/xenosaga-episode-iii",
        "https://www.pricecharting.com/game/playstation-2/xenosaga-3",
        "https://www.pricecharting.com/game/xbox-360/need-for-speed-carbon"
        ]

conditions = ["Complete"]


def get_request(url):
    """
    Makes a request to the given URL. Assumes no authorization is needed.

    Args
    - url: The URL from which information is being requested.

    Returns
    The response text.
    """
    response = requests.get(url=url)

    if response.status_code != 200:
        print("Could not receive response, request may be invalid.")
        return None

    return response.text


def extract_prices(text, url):
    """
    Extracts and cleans up price table data from response.

    Args
    - text: The response text.
    - url: The request URL.

    Returns
    A dictionary containing the pricing info.
    """
    price_guide = None
    try:
        if "Your search for" in text:
            raise ValueError(f"Landed on search page, URL invalid: {url}.")

        soup = BeautifulSoup(text, "html.parser")
        price_table = soup.find_all(id="full-prices")

        if not price_table:
            raise ValueError(f"No prices table could be found for game: {url[url.rindex("/") + 1:]}.")

        price_guide = {"Game": price_table[0].h2.get_text().replace("Full Price Guide: ", "")}

        table_rows = price_table[0].find_all("tr")

        for row in table_rows:
            condition, price = row.get_text().strip().split("\n")
            price_guide[condition] = price

        price_guide = {condition: price for condition, price in price_guide.items() if price != "-"}

    except ValueError as e:
        print(e)

    return price_guide


if __name__ == "__main__":
    invalid_urls = []
    for url in urls:
        resp = get_request(url)
        price_guide = extract_prices(resp, url, invalid_urls)
        print(json.dumps(price_guide, indent=4))

    print(f"Invalid URLs: {invalid_urls}")
