import requests
import json


def main():
    parameters = ["united", "states", "constitution"]
    headers = {"Content-Type": "application/json"}
    url = "http://127.0.0.1:5000/webapp/search/"

    for x in parameters:
        url += f"{x}+"

    url = url[: len(url) - 1]

    response = requests.get(url, headers).json()

    # formatted_response = json.dumps(response, indent=2)
    # print(formatted_response)

    return 0


if __name__ == "__main__":
    main()
