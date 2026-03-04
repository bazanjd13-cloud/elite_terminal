import pandas as pd
import re
from datetime import datetime

IN = "cnbc_headlines.csv"
OUT = "cnbc_news_from_headlines.csv"

def is_ticker(s):
    if not isinstance(s, str): 
        return False
    s = s.strip()
    return bool(re.fullmatch(r"[A-Z0-9\.\-]{1,6}", s))

def normalize_date(d):
    try:
        return pd.to_datetime(d).strftime("%Y-%m-%d")
    except Exception:
        return datetime.utcnow().strftime("%Y-%m-%d")

df = pd.read_csv(IN, dtype=str)
rows = []
for _, r in df.iterrows():
    date = normalize_date(r.get("Date",""))
    raw = str(r.get("Headline","")).strip()
    category = str(r.get("Category","")).strip()
    author = str(r.get("Author","")).strip()
    ts = str(r.get("Timestamp","")).strip()

    # If the Headline field is a short uppercase token, treat as ticker
    ticker = raw if is_ticker(raw) else ""
    # For normal headlines use the headline text
    headline = raw if not ticker else f"{raw} update"

    # Build summary/content from author, timestamp and category
    parts = [p for p in [category, author, ts] if p and p.lower() not in ("nan","none","n/a","")]
    summary = "; ".join(parts)
    content = " ".join([headline, summary]).strip()

    # Map common index names to market symbols
    idx = raw.lower()
    if not ticker:
        if "s&p" in raw or "s&p 500" in raw:
            ticker = ".SPX"
        elif "djia" in raw or "dow" in raw or "dow jones" in raw:
            ticker = ".DJI"
        elif "nasdaq" in raw:
            ticker = ".IXIC"

    rows.append({
        "date": date,
        "ticker": ticker,
        "headline": headline,
        "summary": summary,
        "content": content,
        "source": "CNBC Headlines (converted)"
    })

out = pd.DataFrame(rows)
out.to_csv(OUT, index=False, encoding="utf-8")
print(f"Saved {len(out)} rows to {OUT}")


