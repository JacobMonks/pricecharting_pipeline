import mysql_utils
import scraper_utils


if __name__ == "__main__":
    # Query table for game data (tags for URL and game condition)
    table = "vg_price join console_mapping on game_system = console_name"
    games_list = mysql_utils.query_no_filter("pricecharting", table, ["game_condition", "title_tag", "console_tag"])

    url_template = "https://www.pricecharting.com/game/{console}/{title}"
    invalid_urls = []

    for game in games_list[:10]:
        url = url_template.format(console=game["console_tag"], title=game["title_tag"])

        resp = scraper_utils.get_request(url)
        price_guide = scraper_utils.extract_prices(resp, url, invalid_urls)
        print(f"""
            Game: {price_guide["Game"]}
            Condition: {game["game_condition"]}
            Price: {price_guide[game["game_condition"]]}
        """)

    print(f"Invalid URLs: {invalid_urls}")
