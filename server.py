from flask import Flask
import subprocess
import os

app = Flask(__name__)


@app.route("/track")
def track():

    try:

        root = os.path.dirname(
            os.path.abspath(__file__)
        )

        result = subprocess.run(

            [
                "python",
                os.path.join(
                    root,
                    "app.py"
                )
            ],

            cwd=root,

            capture_output=True,

            text=True

        )

        return {

            "status": "success",

            "stdout": result.stdout,

            "stderr": result.stderr

        }

    except Exception as e:

        return {

            "status": "error",

            "message": str(e)

        }


if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000

    )