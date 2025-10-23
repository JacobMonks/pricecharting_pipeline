import os.path
import pandas as pd
from dags.src.private_constants import Constants
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from mysql import connector

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]


def get_google_sheet_data(range: str):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    raw_data_df = pd.DataFrame()

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=Constants.google_sheet_id, range=range)
            .execute()
        )
        values = result.get("values", [])

        if not values:
            print("No data found.")
            return None

        raw_data_df = pd.DataFrame(values)
        raw_data_df = raw_data_df.rename(columns={0: "Game Title", 5: "Price"})

    except HttpError as err:
        print(err)

    return raw_data_df


def process_data_into_rows(raw_data):

    processed_data = []
    try:
        if raw_data.empty:
            raise ValueError("No data was found.")

        print("Converting raw data into rows...")

        for index, row in raw_data.iterrows():
            new_row = []

            new_row.extend([row["Game Title"], row["Price"]])
            if new_row:
                processed_data.append(new_row)

    except ValueError as e:
        print(e)

    return processed_data


def mysql_google_sheet_migration(data: list):
    try:
        if not data:
            raise ValueError("No data was found.")

        conn = connector.connect(
            host="127.0.0.1",
            port=3306,
            database="pricecharting",
            user="root",
            password=""  # Insert password when connecting locally.
        )
        cursor = conn.cursor()

        header_row = data[0]

        game_system = header_row[0][:header_row[0].index(":")]
        condition = header_row[1]
        if condition == "Game Only":
            condition = "Loose"
        elif condition == "CIB":
            condition = "Complete"

        query = "INSERT INTO vg_price (game_title, game_system, game_condition, price, title_tag) VALUES "
        row = """("{game_title}", "{game_system}", "{game_condition}", {price}, NULL), """

        for item in data[1:]:
            new_row = ""
            if item[1] is not None and '$' in item[1]:
                new_row = row.format(game_title=item[0],
                                     game_system=game_system,
                                     game_condition=condition,
                                     price=float(item[1].strip("$").replace(',', ''))
                                     )
            else:
                new_row = row.format(game_title=item[0],
                                     game_system=game_system,
                                     game_condition=condition,
                                     price="NULL"
                                     )
            query += new_row

        query = query[:query.rindex(")") + 1]
        cursor.execute(query)

        conn.commit()
        print(f"Row(s) were updated for {game_system}: {str(cursor.rowcount)}")

        cursor.close()
        conn.close()

    except connector.Error as e:
        print("ERROR - ", e)

    except ValueError as e:
        print(e)


if __name__ == "__main__":
    data = get_google_sheet_data("Sheet1!A851:F881")
    processed_data = process_data_into_rows(data)
    mysql_google_sheet_migration(processed_data)
