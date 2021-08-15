import colorama as color
import json

from utils import get_key, get_auctions

CONFIG = json.load(open("config.json", "r"))
KEY = get_key()

auctions = get_auctions(KEY)
bin_auctions = []
reforges = [
    "Gentle ",
    "Odd ",
    "Fast ",
    "Fair ",
    "Epic ",
    "Heroic ",
    "Sharp ",
    "Spicy ",
    "Legendary ",
    "Dirty ",
    "Fabled ",
    "Suspicious ",
    "Withered ",
    "Salty ",
    "Treacherous ",
    "Deadly ",
    "Fine ",
    "Grand ",
    "Hasty ",
    "Neat ",
    "Rapid ",
    "Unreal ",
    "Awkward ",
    "Rich ",
    "Precise ",
    "Spiritual ",
    "Clean ",
    "Fierce ",
    "Heavy ",
    "Light ",
    "Mythic ",
    "Pure ",
    "Smart ",
    "Titanic ",
    "Ancient ",
    "Necrotic ",
    "Spiked ",
    "Renowned ",
    "Cubic ",
    "Warped ",
    "Reinforced ",
    "Loving ",
    "Ridiculous ",
    "Giant ",
    "Bizarre ",
    "Itchy ",
    "Ominous ",
    "Pleasant ",
    "Pretty ",
    "Shiny ",
    "Simple ",
    "Strange ",
    "Vivid ",
    "Godly ",
    "Demonic ",
    "Forceful ",
    "Hurtful ",
    "Keen ",
    "Strong ",
    "Superior ",
    "Unpleasant ",
    "Zealous ",
    "Silky ",
    "Bloody ",
    "Shaded ",
    "Sweet ",
    "Fruitful ",
    "Magnetic ",
    "Moil ",
    "Candied ",
    "Perfect ",
    "Wise "
]

for auction in auctions:
    # This removes pets as well
    if "bin" in auction and "[Lvl " not in auction["item_name"]:
        del (
            auction["uuid"],
            auction["auctioneer"],
            auction["profile_id"],
            auction["coop"],
            auction["start"],
            auction["end"],
            auction["item_lore"],
            auction["extra"],
            auction["bids"],
            auction["item_bytes"],
            auction["claimed_bidders"]
        )
        bin_auctions.append(auction)

del auctions
print("Removed non-BIN auctions.")

excepts = [
    "Wise Dragon",
    "Perfect Chestplate",
    "Perfect Helmet",
    "Perfect Leggings",
    "Perfect Boots",
    "Absolutely Perfect"
]

for auction in bin_auctions:
    if [1 if x in auction["item_name"] else 0 for x in excepts]:
        for reforge in reforges:
            if reforge in auction["item_name"]:
                auction["item_name"] = auction["item_name"].replace(reforge, "")

    elif "Wise Dragon" in auction["item_name"] or "Very Wise Dragon" in auction["item_name"]:
        auction["item_name"] = auction["item_name"].replace("Very ", "")
        for reforge in reforges[:-1]:
            auction["item_name"] = auction["item_name"].replace(reforge, "")

    elif "Perfect " in auction["item_name"]:
        auction["item_name"] = auction["item_name"].replace("Absolutely ", "")
        for reforge in reforges[:-2]:
            auction["item_name"] = auction["item_name"].replace(reforge, "")

items = {}
for auction in bin_auctions:
    if auction["item_name"] not in items:
        items[auction["item_name"]] = [auction]
    else:
        items[auction["item_name"]].append(auction)

flips = []
for key in items:
    if len(items[key]) >= CONFIG["min-type-ahs"]:
        cheapest = []

        for item in items[key]:
            cheapest.append(int(item["starting_bid"]))
        cheapest = sorted(cheapest)[:2]

        if len(cheapest) == 2:
            difference = cheapest[1] * 0.99 - cheapest[0]
            margin = round(difference / cheapest[0] * 100, 1)
            flips.append({
                "Item Name": key,
                "Buy Price": cheapest[0],
                "Sell Price": cheapest[1] * 0.99,
                "Difference": difference,
                "Profit Margin": margin
            })

flips = sorted(flips, key=lambda k: k["Difference"])

if __name__ == "__main__":
    max_price = int(input("Max price (in thousands of coins): ")) * 1000
    print()

    color.init()


    def colorizer(val, c):
        if CONFIG["use-colors"]:
            return getattr(color.Fore, c.upper()) + str(val) + color.Fore.RESET
        else:
            return str(val)


    for flip in flips:
        Name = flip["Item Name"]
        Buy = flip["Buy Price"]
        Sell = round(flip["Sell Price"])
        Difference = round(flip["Difference"])
        Profit = flip["Profit Margin"]

        if Buy < max_price and Profit > 100:
            print(f"""| Item Name: {colorizer(Name, 'blue')}
            Buy Price:       {colorizer(Buy, 'yellow')}
            Sell Price:      {colorizer(Sell, 'yellow')}
            Profit:          {colorizer('$' + str(Difference), 'green')}
            Profit Margin:   {colorizer(str(Profit) + '%', 'green')}\n""")
