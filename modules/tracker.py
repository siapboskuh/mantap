from modules.sheet import connect_sheet


def get_batch(batch_size=50):

    sheet = connect_sheet("Sheet1")

    data = sheet.get_all_values()

    requests = []

    seen = {}

    duplicate_updates = []

    format_requests = []

    for row_no, row in enumerate(
        data[1:],
        start=2
    ):

        if len(row) == 0:
            continue

        awb = row[0].strip()

        if awb == "":
            continue

        if awb in seen:

            original_row = seen[awb]

            duplicate_updates.append({

                "range": f"B{row_no}:E{row_no}",

                "values": [[

                    "",

                    "DOUBLE INPUT RESI",

                    "",

                    f"Resi sudah ada di baris {original_row}"

                ]]

            })

            format_requests.append({

                "repeatCell": {

                    "range": {

                        "sheetId": sheet.id,

                        "startRowIndex": row_no - 1,

                        "endRowIndex": row_no,

                        "startColumnIndex": 0,

                        "endColumnIndex": 1

                    },

                    "cell": {

                        "userEnteredFormat": {

                            "backgroundColor": {

                                "red": 1,

                                "green": 0.7,

                                "blue": 0.7

                            }

                        }

                    },

                    "fields": "userEnteredFormat.backgroundColor"

                }

            })

            continue

        seen[awb] = row_no

        requests.append({

            "row": row_no,

            "awb": awb

        })

    if duplicate_updates:

        sheet.batch_update(

            duplicate_updates,

            value_input_option="RAW"

        )

    if format_requests:

        sheet.spreadsheet.batch_update({

            "requests": format_requests

        })

        print(

            f"{len(duplicate_updates)} resi duplikat ditemukan"

        )

    batches = []

    for i in range(

        0,

        len(requests),

        batch_size

    ):

        batches.append(

            requests[
                i:i + batch_size
            ]

        )

    print(

        f"{len(requests)} resi unik akan diproses"

    )

    return batches