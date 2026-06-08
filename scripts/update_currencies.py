#!/usr/bin/env python3
"""Generate assets/currencies.json for the Sip app.

Port of Playgrounds/Currencies.playground. The playground made one apilayer call per base currency
(with a hardcoded API key); this fetches USD-based rates once from the free, keyless
exchangerate-api "open" endpoint and derives every SOURCE→TARGET cross rate via the USD pivot —
mathematically equivalent, no API key, one request.

Output matches the shape the app decodes (CurrencyCache.Currencies): {date, bases, rates}, with an
ISO-8601 `date` and `rates` keyed by concatenated pairs ("USDEUR", "EURUSD", …).
"""
from __future__ import annotations

import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# The currencies Sip offers (kept in sync with the old playground).
BASES = sorted([
    "CAD", "CHF", "CNY", "CZK", "DKK", "EUR", "GBP", "HKD", "HUF", "ILS", "ISK", "JPY",
    "MXN", "NOK", "NZD", "PLN", "RUB", "SAR", "SEK", "SGD", "THB", "TRY", "USD", "ZAR",
])

SOURCE_URL = "https://open.er-api.com/v6/latest/USD"
OUTPUT = Path(__file__).resolve().parent.parent / "assets" / "currencies.json"


def fetch_usd_rates() -> dict[str, float]:
    req = urllib.request.Request(SOURCE_URL, headers={"User-Agent": "sip-landing-page"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.load(resp)
    if payload.get("result") != "success":
        raise SystemExit(f"FX API error: {payload.get('error-type', 'unknown')}")
    rates = payload["rates"]
    missing = [c for c in BASES if c not in rates]
    if missing:
        raise SystemExit(f"FX API is missing currencies: {', '.join(missing)}")
    return rates


def build(usd: dict[str, float]) -> dict:
    pairs: dict[str, float] = {}
    for src in BASES:
        for dst in BASES:
            pairs[f"{src}{dst}"] = round(usd[dst] / usd[src], 6)
    return {
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "bases": BASES,
        "rates": pairs,
    }


def main() -> None:
    data = build(fetch_usd_rates())
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT} — {len(data['rates'])} pairs, dated {data['date']}")


if __name__ == "__main__":
    main()
