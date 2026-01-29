import sqlite3
import pandas as pd
import re

# Load and parse the data in Python first
df = pd.read_csv('results.csv')

# Parse tyre size into columns
def parse_size(size):
    match = re.match(r'(\d+)/(\d+)R(\d+)(C?)', size)
    if match:
        return {
            'width': int(match.group(1)),
            'aspect_ratio': int(match.group(2)),
            'rim': int(match.group(3)),
            'commercial': 'Yes' if match.group(4) == 'C' else 'No'
        }
    return {'width': None, 'aspect_ratio': None, 'rim': None, 'commercial': 'No'}

parsed = df['Size'].apply(parse_size).apply(pd.Series)
df = pd.concat([df, parsed], axis=1)
df = df.rename(columns={'Units Sold': 'sold'})

conn = sqlite3.connect(':memory:')
df.to_sql('tyres', conn, index=False, if_exists='replace')

def run_query(title, query):
    print(title)
    print('='*50)
    result = pd.read_sql_query(query, conn)
    print('='*50)
    print(result.to_string(index=False))
    return result


# 1. Show the parsed data
run_query("1. Tyre Size Breakdown", """
SELECT *
FROM tyres
LIMIT 15
""")


# 2. Sales by rim size
run_query("2. Sales by Rim Size", """
SELECT
  rim,
  SUM(sold) AS total_sold,
  COUNT(*) AS num_sizes,
  ROUND(AVG(sold), 2) AS avg_sold
FROM tyres
GROUP BY rim
ORDER BY total_sold DESC
""")


# 3. Sales by width category
run_query("3. Sales by Tyre Width Category", """
WITH Width_Categories AS (
  SELECT
    CASE
      WHEN width < 185 THEN 'Compact'
      WHEN width BETWEEN 185 AND 215 THEN 'Standard'
      WHEN width BETWEEN 216 AND 255 THEN 'Performance'
      ELSE 'Wide/Sport'
    END AS category,
    sold
  FROM tyres)

SELECT
  category,
  SUM(sold) AS total,
  COUNT(*) AS varieties
FROM Width_Categories
GROUP BY category
ORDER BY total DESC
""")


# 4. Top 3 best sellers per rim size
run_query("4. Best Sellers per Rim Size", """
WITH Ranked_Tyres AS (
  SELECT
    Size,
    sold,
    rim,
    RANK() OVER (PARTITION BY rim
                     ORDER BY sold DESC) AS rank
  FROM tyres)

SELECT
  Size, sold, rim, rank
FROM Ranked_Tyres
WHERE rank <= 3
ORDER BY rim, rank
""")


# 5. Cumulative sales
run_query("5. Cumulative Sales", """
SELECT
  Size,
  sold,
  SUM(sold) OVER (ORDER BY sold DESC) AS running_total,
  ROUND(
    SUM(sold) OVER (ORDER BY sold DESC) * 100.0 /
    SUM(sold) OVER (), 2
  ) AS cumulative_pct
FROM tyres
ORDER BY sold DESC
LIMIT 20
""")


# 6. Top performers
run_query("6. Top Performers", """
WITH Stats AS (
  SELECT AVG(sold) AS avg_sold
  FROM tyres)

SELECT
  t.Size,
  t.sold,
  ROUND(s.avg_sold, 2) AS average
FROM tyres t, Stats s
WHERE t.sold > s.avg_sold * 3
ORDER BY t.sold DESC
""")


# 7. Commercial vs regular
run_query("7. Commercial vs Regular Tyres", """
SELECT
  commercial AS type,
  COUNT(*) AS varieties,
  SUM(sold) AS total,
  ROUND(AVG(sold), 2) AS avg,
  MAX(sold) AS best,
  MIN(sold) AS worst
FROM tyres
GROUP BY commercial
""")


# 8. Market share by rim
run_query("8. Market Share by Rim", """
WITH Rim_Totals AS (
  SELECT
    rim,
    SUM(sold) AS total
  FROM tyres
  GROUP BY rim)

SELECT
  rim,
  total,
  ROUND(total * 100.0 / SUM(total) OVER (), 2) AS market_share
FROM Rim_Totals
ORDER BY total DESC
""")


# 9. Sales by aspect ratio
run_query("9. Sales by Aspect Ratio", """
SELECT
  aspect_ratio,
  SUM(sold) AS total,
  COUNT(*) AS varieties,
  ROUND(AVG(sold), 2) AS avg
FROM tyres
GROUP BY aspect_ratio
ORDER BY total DESC
""")


# 10. Width vs rim grid
run_query("10. Width vs Rim Size Grid", """
WITH Grouped AS (
  SELECT
    CASE
      WHEN width < 185 THEN '<185'
      WHEN width < 215 THEN '185-214'
      WHEN width < 255 THEN '215-254'
      ELSE '255+'
    END AS width_grp,
    CASE
      WHEN rim <= 15 THEN 'R12-15'
      WHEN rim <= 17 THEN 'R16-17'
      WHEN rim <= 19 THEN 'R18-19'
      ELSE 'R20+'
    END AS rim_grp,
    sold
  FROM tyres)

SELECT
  width_grp,
  SUM(CASE WHEN rim_grp = 'R12-15' THEN sold ELSE 0 END) AS [R12-15],
  SUM(CASE WHEN rim_grp = 'R16-17' THEN sold ELSE 0 END) AS [R16-17],
  SUM(CASE WHEN rim_grp = 'R18-19' THEN sold ELSE 0 END) AS [R18-19],
  SUM(CASE WHEN rim_grp = 'R20+' THEN sold ELSE 0 END) AS [R20+],
  SUM(sold) AS total
FROM Grouped
GROUP BY width_grp
ORDER BY width_grp
""")
conn.close()
