# BIN auction flipper for Hypixel Skyblock

## Usage

To use the auction flipper you must add your API key by createing a file called "key.json" with the following text:

```json
{
  "key": "<Your API Key>"
}
```

Then run `main.py`

## Config

Config variables are stored in config.json.

```
{
    "min-type-ahs": int | Minimum amount of auctions for item in order to be shown (to prevent obscure items)
    "max-request-workers": int | Amount of concurrent workers for requesting pages
}
```
