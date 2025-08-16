import mysql_utils
import scraper_utils


if __name__ == "__main__":
    quit = False
    selection_mapping = {1: "NES", 2: "SNES", 3: "N64", 4: "GCN", 5: "Wii",
                         6: "Wii U", 7: "Switch", 8: "Switch 2", 9: "GameBoy",
                         10: "GBA", 11: "DS", 12: "3DS", 13: "Virtual Boy",
                         14: "GBC", 15: "G&W", 16: "PS1", 17: "PS2", 18: "PS3",
                         19: "PS4", 20: "PS5", 21: "PSP", 22: "PSVita",
                         23: "Master System", 24: "Genesis", 25: "Sega CD",
                         26: "Sega 32X", 27: "Saturn", 28: "Dreamcast",
                         29: "Game Gear", 30: "Sega Pico", 31: "Xbox",
                         32: "Xbox 360", 33: "Xbox One", 34: "XSX",
                         35: "Exit"}
    selection_mapping = {str(key): val for key, val in selection_mapping.items()}
    selection_string = ""
    for num, option in selection_mapping.items():
        selection_string += f"\t\t{num} : {option}\n"

    print("""
        ***Welcome to the Video Game Price Guide Tool!***

            You can update the value of any items in your collection.""")

    while not quit:
        print(f"""
            Which console would you like to have updated prices?\n{selection_string}
        """)
        selection = input("Selection: ")
        if selection not in selection_mapping.keys():
            print("Selection was invalid, please make a selection.")

        elif selection == list(selection_mapping.keys())[-1]:
            print("""
                    Thank you for using this service.
                            ***Good-bye!***""")
            quit = True

        else:
            print(f"Updating prices for {selection_mapping[selection]}...")

            # Query table for game data (tags for URL and game condition)
            table = f"""vg_price join console_mapping on game_system = console_name
                where console_name = '{selection_mapping[selection]}'"""
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
