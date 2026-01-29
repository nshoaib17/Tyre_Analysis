import re
import pandas as pd

#Read the Excel file
df = pd.read_excel("sales.xls")

#Convert to CSV-like text so we can use our regex patterns
lines = df.to_csv(index=False).split('\n')

# Where we'll store our tyre size totals
size_totals = {}
size_names = {}
current_size = None

for line in lines:

    # Look for product lines like "2055516[ABC].."
    product_match = re.match(r'^,(\d{7})(\w*)\s*-\s*(\d{3}/\d{2}Z?R\d{1,2}C?(?:LT)?)', line, re.IGNORECASE)

    if product_match:
        current_size = product_match.group(1)
        readable_size = product_match.group(3).replace("ZR", "R")

        if current_size not in size_names:
            size_names[current_size] = readable_size
            size_totals[current_size] = 0
        continue

    # Look for transaction lines (invoices or credit notes (exclusive to business))
    if current_size:
        transaction_match = re.match(r'^,TR(?:INV|CRE)-\d+,,.*?,,,,.*?,,,,(-?[\d.]+),,', line)

        if transaction_match:
            qty = float(transaction_match.group(1))
            size_totals[current_size] += qty

# Export results to CSV
with open("results.csv", "w") as output:
    output.write("Size,Units Sold\n")

    for size_code in sorted(size_totals.keys()):
        qty = int(size_totals[size_code])
        name = size_names.get(size_code, size_code)
        output.write(f"{name},{qty}\n")

