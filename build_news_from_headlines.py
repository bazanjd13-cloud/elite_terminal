import pandas as pd
from datetime import datetime
import re

IN_FILE = "cnbc_headlines.csv"
OUT_FILE = "cnbc_news_from_headlines.csv"

def find_col(df, possible_names):
    for col in df.columns:
        clean = col.strip().lower().replace(" ", "").replace("_", "")
        for name in possible_names:
            if clean == name:
                return col
    return None

def extract_url(text):
    if not isinstance(text, str):
        return ""
    m = re.search(r"https?://\S+", text)
    return m.group(0) if m else ""

def main():
    df = pd.read_csv(IN_FILE)

    # Try to detect columns automatically
    headline_col = find_col(df, ["asset/headline", "assetheadline", "headline"])
    ticker_col   = find_col(df, ["symbol/source", "symbolsource", "symbol"])
    notes_col    = find_col(df, ["notes", "note"])

    print("Detected columns:")
    print("Headline:", headline_col)
    print("Ticker:", ticker_col)
    print("Notes:", notes_col)

    if not headline_col or not ticker_col or not notes_col:
        raise SystemExit("Could not detect required columns. Check CSV headers.")

    rows = []
    today = datetime.utcnow().strftime("%Y-%m-%d")

    for _, r in df.iterrows():
        ticker = str(r[ticker_col]).strip().upper()
        headline = str(r[headline_col]).strip()
        notes = str(r[notes_col]).strip()
        content = f"{headline}. {notes}"

        rows.append({
            "date": today,
            "ticker": ticker,
            "headline": headline,
            "summary": notes,
            "content": content,
            "source": "CNBC Headlines"
        })

    out_df = pd.DataFrame(rows)
    out_df.to_csv(OUT_FILE, index=False, encoding="utf-8")
    print(f"\nSaved {len(out_df)} rows to {OUT_FILE}")

if __name__ == "__main__":
    main()

import pandas as pd
from datetime import datetime
import re

IN_FILE = "cnbc_headlines.csv"
OUT_FILE = "cnbc_news_from_headlines.csv"

def find_col(df, possible_names):
    for col in df.columns:
        clean = col.strip().lower().replace(" ", "").replace("_", "")
        for name in possible_names:
            if clean == name:
                return col
    return None

def extract_url(text):
    if not isinstance(text, str):
        return ""
    m = re.search(r"https?://\S+", text)
    return m.group(0) if m else ""

def main():
    df = pd.read_csv(IN_FILE)

    # Try to detect columns automatically
    headline_col = find_col(df, ["asset/headline", "assetheadline", "headline"])
    ticker_col   = find_col(df, ["symbol/source", "symbolsource", "symbol"])
    notes_col    = find_col(df, ["notes", "note"])

    print("Detected columns:")
    print("Headline:", headline_col)
    print("Ticker:", ticker_col)
    print("Notes:", notes_col)

    if not headline_col or not ticker_col or not notes_col:
        raise SystemExit("Could not detect required columns. Check CSV headers.")

    rows = []
    today = datetime.utcnow().strftime("%Y-%m-%d")

    for _, r in df.iterrows():
        ticker = str(r[ticker_col]).strip().upper()
        headline = str(r[headline_col]).strip()
        notes = str(r[notes_col]).strip()
        content = f"{headline}. {notes}"

        rows.append({
            "date": today,
            "ticker": ticker,
            "headline": headline,
            "summary": notes,
            "content": content,
            "source": "CNBC Headlines"
        })

    out_df = pd.DataFrame(rows)
    out_df.to_csv(OUT_FILE, index=False, encoding="utf-8")
    print(f"\nSaved {len(out_df)} rows to {OUT_FILE}")

if __name__ == "__main__":
    main()

import pandas as pd
from datetime import datetime
import re

IN_FILE = "cnbc_headlines.csv"
OUT_FILE = "cnbc_news_from_headlines.csv"

def extract_url(text):
    if not isinstance(text, str):
        return ""
    m = re.search(r"https?://\S+", text)
    return m.group(0) if m else ""

def main():
    df = pd.read_csv(IN_FILE)
    required = ["Asset/Headline","Symbol/Source","Notes"]
    for c in required:
        if c not in df.columns:
            raise SystemExit(f"Missing column: {c}")

    rows = []
    today = datetime.utcnow().strftime("%Y-%m-%d")

    for _, r in df.iterrows():
        ticker = str(r["Symbol/Source"]).strip().upper()
        headline = str(r["Asset/Headline"]).strip()
        notes = str(r["Notes"]).strip()
        content = f"{headline}. {notes}"

        rows.append({
            "date": today,
            "ticker": ticker,
            "headline": headline,
            "summary": notes,
            "content": content,
            "source": "CNBC Headlines"
        })

    out_df = pd.DataFrame(rows)
    out_df.to_csv(OUT_FILE, index=False, encoding="utf-8")
    print(f"Saved {len(out_df)} rows to {OUT_FILE}")

if __name__ == "__main__":
    main()

