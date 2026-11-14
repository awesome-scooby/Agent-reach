"""Parse the structured market JSON REIWA embeds in each suburb profile page
(already fetched and cached by collect.reiwa). Keeps only market fields;
drops schools, map keys and marketing text.

Fields used (REIWA definitions, as stated on the page):
  * medians and quartiles: settled sales, 12 months to the latest completed month
  * bedroom medians: MedianHouseSalePriceThreeBed etc. (same 12-month window)
  * counts: CountOfHousesSold / CountOfUnitsSold (12 months)
  * BuyTrendData: calendar-year medians (current year = rolling 12 months)
  * DaysOnMarket: median selling days for settled sales
"""
import html
import json
import re
from pathlib import Path

CACHE = Path(__file__).resolve().parent.parent / ".cache"
KEEP_PRICE = ["MedianHouseSalePrice", "HouseSalePriceUpperQuartile", "HouseSalePriceLowerQuartile",
              "MedianHouseSalePriceTwoBed", "MedianHouseSalePriceThreeBed", "MedianHouseSalePriceFourBed",
              "CountOfHousesSold", "MedianHouseRentPrice", "MedianHouseRentPriceThreeBed", "CountOfHousesLeased",
              "MedianUnitSalePrice", "UnitSalePriceLowerQuartile", "UnitSalePriceUpperQuartile",
              "MedianUnitSalePriceTwoBed", "MedianUnitSalePriceThreeBed", "CountOfUnitsSold",
              "MedianUnitRentPrice", "MedianLandSalePrice", "CountOfLandSold"]


def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def parse(name):
    f = CACHE / f"reiwa_{slug(name)}.html"
    if not f.exists():
        return None
    s = f.read_text(encoding="utf-8", errors="ignore")
    for m in re.finditer(r"data-props='(.*?)'", s, flags=re.S):
        raw = html.unescape(m.group(1))
        if "SuburbPriceData" not in raw:
            continue
        try:
            d = json.loads(raw)["data"]
        except (json.JSONDecodeError, KeyError):
            continue
        p = d.get("SuburbPriceData") or {}
        g = d.get("GrowthRateChartData") or {}
        out = {k: p.get(k) for k in KEEP_PRICE}
        out.update({
            "trend": [[t["CalendarYear"], t.get("MedianHousePrice"), t.get("HouseCount"), t.get("MedianUnitPrice"), t.get("UnitCount")]
                      for t in p.get("BuyTrendData") or []],
            "rent_trend": [[t["CalendarYear"], t.get("MedianHousePrice"), t.get("HouseCount")] for t in p.get("RentTrendData") or []],
            "dom_house": d.get("HouseSalesDaysOnMarket"), "dom_unit": d.get("UnitSalesDaysOnMarket"),
            "dom_rent_house": d.get("HouseRentalDaysOnMarket"),
            "g1": g.get("HouseActualGrowthRateOneYear"), "g5": g.get("HouseActualGrowthRateFiveYears"),
            "g10": g.get("HouseActualGrowthRateTenYears"), "g10_pa": g.get("HouseGrowthRateTenYears"),
            "region_g10_pa": g.get("RegionHouseGrowthRateTenYears"),
            "trains": d.get("TrainStations"), "shops": d.get("Shops"), "km_reiwa": d.get("DistanceFromPerth"),
            "population": d.get("Population"), "interest": d.get("InterestLevel"),
            "tenure_rented_pct": (d.get("SuburbCensusData") or {}).get("OwnershipRentedNo"),
            "dwelling_house_pct": (d.get("SuburbCensusData") or {}).get("PropertyTypeHouseNo"),
            "dwelling_semi_pct": (d.get("SuburbCensusData") or {}).get("PropertyTypeDuplexNo"),
            "as_at": d.get("SettledSalesDescription"), "period": d.get("PriceDataDescription"),
            "url": f"https://reiwa.com.au/suburb/{slug(name)}/",
        })
        return out
    return None
