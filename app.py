from modules.tracker import get_batch
from modules.biteship import Biteship
from modules.writer import save_results


def main():

    batches = get_batch(50)

    total = len(batches)

    print(
        f"Total batch: {total}"
    )

    bs = Biteship()

    semua_hasil = []

    for nomor, batch in enumerate(
        batches,
        start=1
    ):

        print(
            f"\nBatch {nomor}/{total}"
        )

        awbs = [

            item["awb"]

            for item in batch

        ]

        bs.track(
            awbs
        )

        semua_hasil.extend(

            bs.get_results()

        )

    bs.close()

    save_results(

        semua_hasil

    )

    print(

        "\nSelesai"

    )


if __name__ == "__main__":

    main()