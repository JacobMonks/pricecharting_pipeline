import requests
from bs4 import BeautifulSoup

urls = ["https://www.pricecharting.com/game/playstation-2/xenosaga-3",
        # "https://www.pricecharting.com/game/xbox-360/need-for-speed-carbon"
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


def extract_prices(text):
    """
    Extracts and cleans up price table data from response.

    Args
    - text: The response text.

    Returns
    A dictionary containing the pricing info.
    """
    price_guide = None
    try:
        soup = BeautifulSoup(text, "html.parser")
        price_table = soup.find_all(id="full-prices")

        if not price_table:
            raise ValueError("No prices table could be found.")

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
    for url in urls:
        resp = get_request(url)
        price_guide = extract_prices(resp)

        print(price_guide)
