from modules.sheet import connect_sheet


def save_results(results):

    sheet = connect_sheet("Sheet1")

    data = sheet.get_all_values()

    # Simpan semua row berdasarkan AWB
    awb_rows = {}

    for row_no, row in enumerate(
        data[1:],
        start=2
    ):

        if len(row) == 0:
            continue

        awb = row[0].strip()

        if awb == "":
            continue

        if awb not in awb_rows:

            awb_rows[awb] = []

        awb_rows[awb].append(
            row_no
        )

    output = [

        ["", "", "", ""]

        for _ in range(
            len(data) - 1
        )

    ]

    total = 0

    for item in results:

        awb = str(

            item.get(
                "waybill_id",
                ""
            )

        ).strip()

        if awb == "":
            continue

        rows = awb_rows.get(
            awb,
            []
        )

        if len(rows) == 0:
            continue

        courier = item.get(
            "courier",
            {}
        )

        courier_name = ""

        if isinstance(
            courier,
            dict
        ):

            courier_name = courier.get(
                "company",
                ""
            )

        status = item.get(
            "status",
            ""
        )

        history = item.get(
            "history",
            []
        )

        last_update = ""

        note = ""

        if history:

            latest = history[-1]

            last_update = latest.get(
                "updated_at",
                ""
            )

            note = latest.get(
                "note",
                ""
            )

        # Baris pertama: hasil normal
        first_row = rows[0]

        output[first_row - 2] = [

            courier_name,

            status,

            last_update,

            note

        ]

        # Baris duplikat: kasih keterangan
        if len(rows) > 1:

            for duplicate_row in rows[1:]:

                output[duplicate_row - 2] = [

                    "",

                    "DOUBLE INPUT RESI",

                    "",

                    f"Resi sudah ada di baris {first_row}"

                ]

        total += 1

    sheet.batch_clear(

        [

            "B2:E1000"

        ]

    )

    sheet.update(

        range_name=f"B2:E{len(output)+1}",

        values=output

    )

    print(

        f"{total} resi unik berhasil ditulis"

    )