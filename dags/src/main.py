import math
import mysql_utils
import scraper_utils


if __name__ == "__main__":
    exit_program = False
    selection_mapping = {1: "NES", 2: "SNES", 3: "N64", 4: "GCN", 5: "Wii",
                         6: "Wii U", 7: "Switch", 8: "Switch 2", 9: "GameBoy",
                         10: "GBA", 11: "DS", 12: "3DS", 13: "Virtual Boy",
                         14: "GBC", 15: "G&W", 16: "PS1", 17: "PS2", 18: "PS3",
                         19: "PS4", 20: "PS5", 21: "PSP", 22: "PSVita",
                         23: "Master System", 24: "Genesis", 25: "Sega CD",
                         26: "Sega 32X", 27: "Saturn", 28: "Dreamcast",
                         29: "Game Gear", 30: "Sega Pico", 31: "Xbox",
                         32: "Xbox 360", 33: "Xbox One", 34: "XSX"}
    selection_mapping = {str(key): val for key, val in selection_mapping.items()}
    print("""
            ***Welcome to the Video Game Price Guide Tool!***

            You can update the value of any items in your collection.""")
    page_no = 1
    page_size_limit = 6
    number_of_pages = math.ceil(len(selection_mapping) / page_size_limit)
    start_of_page = 1
    end_of_page = page_size_limit
    while not exit_program:
        try:
            print("""
            Which console would you like to have updated prices?""")
            valid_selections = list(range(start_of_page, end_of_page + 4))
            offset = int(valid_selections[0]) - 1
            for num, option in selection_mapping.items():
                if int(num) in valid_selections[:-3]:
                    print(f"\t\t{int(num) - offset} : {option}")

            prev_page, next_page, quit = 0, 0, 0
            if page_no == 1:
                next_page = end_of_page + 1
                quit = end_of_page + 2
                print(f"\t\t{next_page - offset} : Next Page")
                valid_selections.pop()
            elif page_no != page_size_limit:
                prev_page = end_of_page + 1
                next_page = end_of_page + 2
                quit = end_of_page + 3
                print(f"\t\t{prev_page - offset} : Previous Page")
                print(f"\t\t{next_page - offset} : Next Page")
            else:
                prev_page = end_of_page + 1
                quit = end_of_page + 2
                valid_selections.pop()
                print(f"\t\t{prev_page - offset} : Previous Page")
            print(f"\t\t{quit - offset} : Quit")

            selection = int(input("Selection: ")) + offset
            if selection not in valid_selections:
                print("Selection was invalid, please make a selection.")
            elif selection == next_page:
                start_of_page += page_size_limit
                end_of_page += page_size_limit
                page_no += 1
            elif selection == prev_page:
                start_of_page -= page_size_limit
                end_of_page -= page_size_limit
                page_no -= 1
            elif selection == quit:
                print("""
                        Thank you for using this service.
                                ***Good-bye!***""")
                exit_program = True
            else:
                print(f"Updating prices for {selection_mapping[str(selection)]}...")

                # Query table for game data (tags for URL and game condition)
                table = f"""vg_price join console_mapping on game_system = console_name
                    where console_name = '{selection_mapping[str(selection)]}'"""
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
                        if not price_guide:
                            invalid_urls.append({"title": title, "url": url})

                    except Exception as e:
                        print(f"Ran into a problem with url {url} - {e}")
                        invalid_urls.append({"title": title, "url": url})

                if invalid_urls:
                    mysql_utils.report_failures(invalid_urls)
                    print("Invalid URL table has been updated.")
        except Exception:
            print("""
                Sorry, we ran into an issue with that selection.
                Please select a different option.""")
