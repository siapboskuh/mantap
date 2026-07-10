import os
import json
import glob
import gspread

from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

SPREADSHEET_ID = "1vt2JnG-ipB-AHP62ej3ItoAUgt192-qqNQMRKVDGN18"


def get_credential():

    current = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(current)

    json_files = (
        glob.glob(os.path.join(root, "credentials", "*.json"))
        + glob.glob(os.path.join(root, "*.json"))
    )

    for file in json_files:

        try:

            with open(file, encoding="utf8") as f:

                data = json.load(f)

                if "private_key" in data and "project_id" in data:

                    return file

        except Exception:
            pass

    raise Exception("service_account.json tidak ditemukan")


def get_client():

    creds = Credentials.from_service_account_file(
        get_credential(),
        scopes=SCOPES
    )

    return gspread.authorize(creds)


client = get_client()

spreadsheet = client.open_by_key(SPREADSHEET_ID)


def connect_sheet(name="Sheet1"):

    return spreadsheet.worksheet(name)


def get_awb(limit=None):

    sheet = connect_sheet("Sheet1")

    data = sheet.get_all_values()

    hasil = []

    for i, row in enumerate(data[1:], start=2):

        if len(row) == 0:
            continue

        awb = row[0].strip()

        if awb == "":
            continue

        hasil.append({
            "row": i,
            "awb": awb
        })

        if limit and len(hasil) >= limit:
            break

    return hasil