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

### 1. Tyre Size Breakdown
```
      Size  sold  width  aspect_ratio  rim commercial
 145/65R15     1    145            65   15         No
 155/65R13     2    155            65   13         No
 155/65R14    33    155            65   14         No
155/70R12C     4    155            70   12        Yes
 155/70R13     2    155            70   13         No
 ...
```

### 2. Sales by Rim Size
```
 rim  total_sold  num_sizes  avg_sold
  17        1194         25     47.76
  16        1036         28     37.00
  18         937         31     30.23
  15         540         20     27.00
  19         497         27     18.41
  20         238         28      8.50
  14         142         10     14.20
  21          70         19      3.68
  22          28         11      2.55
  13          13          4      3.25
  23           6          2      3.00
  12           6          2      3.00
```

### 3. Sales by Tyre Width Category
```
   category  total  varieties
   Standard   2196         63
Performance   2021         82
 Wide/Sport    250         46
    Compact    240         16
```

### 4. Best Sellers per Rim Size
```
      Size  sold  rim  rank
155/70R12C     4   12     1
195/60R12C     2   12     2
 175/65R13     7   13     1
 175/65R14    46   14     1
 195/65R15    87   15     1
 205/55R16   262   16     1
 225/45R17   202   17     1
 225/40R18   198   18     1
 225/45R19    62   19     1
 255/35R20    27   20     1
 275/35R21     9   21     1
 325/35R22     5   22     1
 285/40R23     4   23     1
```

### 5. Cumulative Sales
```
      Size  sold  running_total  cumulative_pct
 205/55R16   262            262            5.57
 225/45R17   202            464            9.86
 225/40R18   198            662           14.06
 215/45R17   125            787           16.72
 205/45R17   115            902           19.16
 215/50R17   107           1116           23.71
 225/50R17   107           1116           23.71
 225/45R18    93           1209           25.69
 195/65R15    87           1296           27.53
 205/60R16    84           1380           29.32
```

### 6. Top Performers
```
      Size  sold
 205/55R16   262    
 225/45R17   202    
 225/40R18   198    
 215/45R17   125    
 205/45R17   115    
 215/50R17   107    
 225/50R17   107    
 225/45R18    93    
 195/65R15    87    
 205/60R16    84    
```

### 7. Commercial vs Regular Tyres
```
type  varieties  total   avg  best  worst
  No        187   4223 22.58   262      1
 Yes         20    484 24.20    75      2
```

### 8. Market Share by Rim
```
 rim  total  market_share
  17   1194         25.37
  16   1036         22.01
  18    937         19.91
  15    540         11.47
  19    497         10.56
  20    238          5.06
  14    142          3.02
  21     70          1.49
  22     28          0.59
  13     13          0.28
  12      6          0.13
  23      6          0.13
```

### 9. Sales by Aspect Ratio
```
 aspect_ratio  total  varieties   avg
           45   1017         32 31.78
           55    925         24 38.54
           40    646         34 19.00
           65    602         23 26.17
           50    520         19 27.37
           60    436         20 21.80
           35    347         30 11.57
           70     88          9  9.78
           75     84          5 16.80
           30     42         11  3.82
```

### 10. Width vs Rim Size Grid
```
width_grp  R12-15  R16-17  R18-19  R20+  total
  185-214     420     954      20     6   1400
  215-254      41    1276    1190    92   2599
     255+       0       0     224   244    468
     <185     240       0       0     0    240
```

## Usage

```bash
pip install pandas
python sql_analysis.py
```

## Requirements

- Python 3.x
- pandas
