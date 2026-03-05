import pandas as pd
import re
from datetime import datetime

IN = "cnbc_headlines.csv"
OUT = "cnbc_news_from_headlines.csv"

def is_ticker(s):
    if not isinstance(s, str): return False
    s = s.strip()
    # common ticker pattern: 1-5 uppercase letters, sometimes with . or - for indexes
    return bool(re.fullmatch(r"[A-Z]{1,5}(\.[A-Z0-9]+)?", s))

def normalize_date(d):
    try:
        return pd.to_datetime(d).strftime("%Y-%m-%d")
    except Exception:
        return datetime.utcnow().strftime("%Y-%m-%d")

df = pd.read_csv(IN)
rows = []
for _, r in df.iterrows():
    date = normalize_date(r.get("Date",""))
    raw = str(r.get("Headline/Symbol","")).strip()
    author = str(r.get("Author/Detail","")).strip()
    value = str(r.get("Value/Timestamp","")).strip()

    # Decide ticker vs headline
    ticker = raw if is_ticker(raw) else ""
    headline = raw if not is_ticker(raw) else f"{raw} update"
    # Build summary/content
    parts = [p for p in [author, value] if p and p.lower() not in ("nan","")]
    summary = "; ".join(parts) if parts else ""
    content = " ".join([headline, summary]).strip()

    # If ticker empty but Category indicates Market Index, use raw as ticker-like label
    cat = str(r.get("Category","")).strip().lower()
    if not ticker and "market index" in cat:
        ticker = raw

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


