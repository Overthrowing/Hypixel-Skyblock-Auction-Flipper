import json
import requests as r
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from requests_futures.sessions import FuturesSession

HYPIXEL_API = "https://api.hypixel.net/"
CONFIG = json.load(open("config.json", "r"))


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
    print('Getting Pages.')

    session = FuturesSession(executor=ThreadPoolExecutor(max_workers=CONFIG["max-request-workers"]))
    urls = [
        HYPIXEL_API + "skyblock/auctions" + f"?key={key}&page={i}" for i in range(1, page_count)
    ]
    responses = [session.get(u) for u in urls]

    for res in as_completed(responses):
        resp = res.result()
        print('.', end="", flush=True)

        try:
            page = resp.json()
        except json.decoder.JSONDecodeError:
            print(resp.content[:500])

        if "error" in page:
            raise MemoryError(page['error'], page['cause'])
        try:
            auctions += page['auctions']
        except KeyError:
            print(page.keys())

    print('\nFinished Getting Pages.')

    return auctions
