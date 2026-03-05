import csv

IN = "cnbc_headlines.csv"
OUT = "cnbc_headlines_clean.csv"

with open(IN, "r", encoding="utf-8", newline="") as f:
    # read raw lines to preserve quoting issues
    lines = f.read().splitlines()

# get header and expected column count
if not lines:
    raise SystemExit("Input file is empty.")
header = lines[0]
expected = len(next(csv.reader([header])))

clean_rows = []
for i, line in enumerate(lines):
    try:
        row = next(csv.reader([line]))
    except Exception:
        # fallback: naive split
        row = line.split(",")
    if len(row) == expected:
        clean_rows.append(row)
    elif len(row) > expected:
        # merge extra fields into the last column
        merged = row[:expected-1] + [",".join(row[expected-1:])]
        clean_rows.append(merged)
    else:
        # pad missing fields with empty strings
        padded = row + [""] * (expected - len(row))
        clean_rows.append(padded)

# write cleaned CSV
with open(OUT, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    for r in clean_rows:
        writer.writerow(r)

print(f"Saved cleaned file: {OUT} (expected columns = {expected}, rows = {len(clean_rows)})")


