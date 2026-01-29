# Tyre Sales Analysis

SQL analysis of tyre sales data, exploring patterns across different tyre dimensions.

## Data

The dataset (`results.csv`) contains tyre sales with two columns:
- **Size** - Tyre dimensions in standard format (e.g., `205/55R16`, `215/65R16C`)
- **Units Sold** - Number of units sold

### Tyre Size Format

| Part | Example | Meaning |
|------|---------|---------|
| Width | 205 | Tyre width in mm |
| Aspect Ratio | 55 | Sidewall height as % of width |
| Rim | 16 | Wheel diameter in inches |
| C suffix | C | Commercial vehicle tyre |

## Queries

The analysis includes:

1. **Tyre Size Breakdown** - Show the parsed data
2. **Sales by Rim Size** - Sales by rim size
3. **Sales by Tyre Width Category** - Compact, Standard, Performance, Wide/Sport
4. **Best Sellers per Rim Size** - Top 3 best sellers per rim size
5. **Cumulative Sales** - Cumulative sales
6. **Top Performers** - Top performers
7. **Commercial vs Regular Tyres** - Commercial vs regular
8. **Market Share by Rim** - Market share by rim
9. **Sales by Aspect Ratio** - Sales by aspect ratio
10. **Width vs Rim Size Grid** - Width vs rim grid

## Usage

```bash
pip install pandas
python sql_analysis.py
```

## Requirements

- Python 3.x
- pandas
