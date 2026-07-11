from flask import Flask
import subprocess
import os
import sys

app = Flask(__name__)


@app.route("/")
def home():

    return {
        "status": "online",
        "message": "CEK RESI API is running"
    }


@app.route("/track")
def track():

    try:

        root = os.path.dirname(
            os.path.abspath(__file__)
        )

        result = subprocess.run(

            [
                sys.executable,
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

            "return_code": result.returncode,

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