import mysql_utils
import scraper_utils


if __name__ == "__main__":
    # Query table for game data (tags for URL and game condition)
    table = "vg_price join console_mapping on game_system = console_name where console_tag = 'super-nintendo'"
    games_list = mysql_utils.query_no_filter("pricecharting", table,
                                             ["game_title", "game_condition", "title_tag", "console_tag"])

    url_template = "https://www.pricecharting.com/game/{console}/{title}"
    invalid_urls = []

    for game in games_list:
        try:
            url = url_template.format(console=game["console_tag"], title=game["title_tag"])
            title = game["game_title"]

            resp = scraper_utils.get_request(url)
            if not resp:
                invalid_urls.append({"title": title, "url": url})

            price_guide = scraper_utils.extract_prices(resp, url)
            if price_guide:
                print(f"""
                    Game: {price_guide["Game"]}
                    Condition: {game["game_condition"]}
                    Price: {price_guide[game["game_condition"]]}
                """)
            else:
                invalid_urls.append({"title": title, "url": url})

        except Exception as e:
            print(f"Ran into a problem with url {url} - {e}")
            invalid_urls.append({"title": title, "url": url})

    print(f"Invalid URLs: {invalid_urls}")

    if invalid_urls:
        mysql_utils.report_failures(invalid_urls)
        print("Invalid URL table has been updated.")
