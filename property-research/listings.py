#!/usr/bin/env python3
"""Current for-sale listings from the Domain developer API (free tier).

The API key is never stored here. In this cloud environment the network
proxy injects the saved credential into requests to api.domain.com.au, so
the script sends a placeholder header that the proxy replaces. Running
elsewhere, set DOMAIN_API_KEY in your shell.

Search: 3+ bedroom houses and townhouses, for sale, up to MAX_PRICE, in the
shortlist suburbs with the highest match score. Writes data/listings.json.
If no key is configured, writes {"status": "no_key"} and exits cleanly.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "data" / "listings.json"
API = "https://api.domain.com.au/v1/listings/residential/_search"
MAX_PRICE = 620_000          # a little over budget: medians are beatable in a falling market
TOP_N = 16                   # suburbs searched per day (free tier ~500 calls/day; we use 1 call per suburb)


def search(suburb, state, postcode):
    body = {"listingType": "Sale", "propertyTypes": ["House", "Townhouse", "Villa", "SemiDetached"],
            "minBedrooms": 3, "maxPrice": MAX_PRICE, "pageSize": 50,
            "locations": [{"state": state, "suburb": suburb, "postCode": postcode, "includeSurroundingSuburbs": False}]}
    req = urllib.request.Request(API, data=json.dumps(body).encode(), method="POST", headers={
        "Content-Type": "application/json", "Accept": "application/json",
        "X-Api-Key": os.environ.get("DOMAIN_API_KEY", "placeholder-replaced-by-proxy")})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.loads(r.read().decode())


def flatten(item, suburb, city):
    lst = item.get("listing") or {}
    pd = lst.get("propertyDetails") or {}
    price = (lst.get("priceDetails") or {}).get("displayPrice")
    return {"id": lst.get("id"), "suburb": suburb, "city": city,
            "address": pd.get("displayableAddress"), "type": pd.get("propertyType"),
            "beds": pd.get("bedrooms"), "baths": pd.get("bathrooms"), "cars": pd.get("carspaces"),
            "land": pd.get("landArea"), "price": price, "headline": lst.get("headline"),
            "listed": lst.get("dateListed"),
            "url": f"https://www.domain.com.au/{lst.get('listingSlug')}" if lst.get("listingSlug") else None}


def main():
    model = json.loads((ROOT / "data" / "model.json").read_text())
    subs = sorted(model["suburbs"], key=lambda s: -s["match"])[:TOP_N]
    found, errors = [], []
    for s in subs:
        state = "VIC" if s["city"] == "Melbourne" else "WA"
        try:
            res = search(s["suburb"], state, s["postcode"])
            for it in res if isinstance(res, list) else []:
                if it.get("type") == "PropertyListing":
                    found.append(flatten(it, s["suburb"], s["city"]))
        except urllib.error.HTTPError as e:
            if e.code in (401, 403):
                OUT.write_text(json.dumps({"status": "no_key", "message": f"Domain API returned {e.code}. Add the key via the environment's credential form."}))
                print("no key / not authorised", file=sys.stderr)
                return
            errors.append(f"{s['suburb']}: HTTP {e.code}")
        except Exception as e:  # noqa: BLE001
            errors.append(f"{s['suburb']}: {e}")
        time.sleep(0.5)
    OUT.write_text(json.dumps({"status": "ok", "fetched": time.strftime("%Y-%m-%d %H:%M"), "max_price": MAX_PRICE,
                               "suburbs_searched": [s["suburb"] for s in subs], "errors": errors,
                               "listings": found}, indent=1))
    print(f"{len(found)} listings, {len(errors)} errors", file=sys.stderr)


if __name__ == "__main__":
    main()
