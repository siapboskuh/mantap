from playwright.sync_api import sync_playwright
import json


class Biteship:

    def __init__(self):

        self.responses = []

        self.saved_awb = set()

        self.p = sync_playwright().start()

        self.browser = self.p.chromium.launch(
            headless=False
        )

        self.page = self.browser.new_page()

    def track(self, awbs):

        print("\nMembuka Biteship...")

        def handle_response(response):

            try:

                if "/v1/public/trackings/" not in response.url:

                    return

                data = response.json()

                awb = data.get(
                    "waybill_id",
                    ""
                )

                if awb == "":

                    return

                if awb in self.saved_awb:

                    return

                self.saved_awb.add(
                    awb
                )

                self.responses.append(
                    data
                )

                print(
                    "[TRACKING]",
                    awb
                )

            except Exception:

                pass

        self.page.on(
            "response",
            handle_response
        )

        self.page.goto(
            "https://biteship.com/id/cek-resi",
            wait_until="networkidle"
        )

        textarea = self.page.locator(
            "textarea"
        )

        textarea.wait_for(
            timeout=30000
        )

        textarea.fill(
            "\n".join(awbs)
        )

        print(
            f"{len(awbs)} resi berhasil diinput"
        )

        self.page.get_by_role(
            "button",
            name="Cek Resi"
        ).click()

        print(
            "\nMenunggu hasil..."
        )

        self.page.wait_for_timeout(
            20000
        )

        print(
            f"{len(self.responses)} tracking tersimpan"
        )

        with open(
            "responses.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.responses,
                f,
                ensure_ascii=False,
                indent=2
            )

    def get_results(self):

        return self.responses

    def close(self):

        self.browser.close()

        self.p.stop()