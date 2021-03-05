import requests as r
import json


HYPIXEL_API = "https://api.hypixel.net/"


def get_key():
    with open("key.json", "r") as key:
        return json.load(key)["key"]

def get_auctions(key):
    response = r.get(HYPIXEL_API + "skyblock/auctions" + f"?key={key}").json()

    if "error" in response:
        raise MemoryError(response['error'], response['cause'])

    auctions = response['auctions']
    page_count = response['totalPages']

    print('Total Pages:', page_count)
    print('Total Auctions:', response['totalAuctions'])
    print('Getting Pages...')
    for i in range(1, page_count):
        print('.', end="", flush=True)
        page = r.get(HYPIXEL_API + "skyblock/auctions" + f"?key={key}&page={i}")

        try:
            page = page.json()
        except json.decoder.JSONDecodeError:
            print(page.content[:500])

        if "error" in page:
            raise MemoryError(page['error'], page['cause'])
        try:
            auctions += page['auctions']
        except KeyError:
            print(page.keys())

    print('\nFinished Getting Pages.')

    return auctions

