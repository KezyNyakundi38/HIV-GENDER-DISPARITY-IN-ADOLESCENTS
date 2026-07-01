# Power BI — DAX Measures, M-Code \& Dashboard Layout

## Power Query (M) — clean column aliases at the ingestion layer

```m
let
    Source = Csv.Document(File.Contents("...\\\\jan\\\_2021\\\_data\\\_viz5\\\_gender\\\_inequality\\\_and\\\_hivaids1.csv"),
        \\\[Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Promoted = Table.PromoteHeaders(Source, \\\[PromoteAllScalars=true]),
    Typed = Table.TransformColumnTypes(Promoted, {
        {"year", Int64.Type},
        {"estimated\\\_number\\\_of\\\_annual\\\_new\\\_hiv\\\_infections", type number},
        {"estimated\\\_number\\\_of\\\_annual\\\_aids\\\_related\\\_deaths", type number},
        {"estimated\\\_incidence\\\_rate\\\_of\\\_new\\\_hiv\\\_infection\\\_per\\\_1\\\_000\\\_uninfected\\\_population", type number},
        {"estimated\\\_rate\\\_of\\\_annual\\\_aids\\\_related\\\_deaths\\\_per\\\_100\\\_000\\\_population", type number},
        {"estimated\\\_number\\\_of\\\_people\\\_living\\\_with\\\_hiv", Int64.Type}
    }),
    Renamed = Table.RenameColumns(Typed, {
        {"estimated\\\_number\\\_of\\\_annual\\\_new\\\_hiv\\\_infections", "New Infections"},
        {"estimated\\\_number\\\_of\\\_annual\\\_aids\\\_related\\\_deaths", "AIDS Deaths"}
    })
in
    Renamed
```

## DAX Measures

```dax
-- Total New Infections
Total New Infections =
SUM ( hiv\\\_data\\\[New Infections] )

-- Total AIDS Deaths (helper)
Total AIDS Deaths =
SUM ( hiv\\\_data\\\[AIDS Deaths] )

-- YoY Death Rate Change (%)
-- Uses a year-context-shifted measure; requires a Year dimension/sort.
YoY Death Change % =
VAR CurrentDeaths = \\\[Total AIDS Deaths]
VAR PriorDeaths =
    CALCULATE (
        \\\[Total AIDS Deaths],
        FILTER (
            ALL ( hiv\\\_data\\\[year] ),
            hiv\\\_data\\\[year] = MAX ( hiv\\\_data\\\[year] ) - 1
        )
    )
RETURN
    DIVIDE ( CurrentDeaths - PriorDeaths, PriorDeaths )

-- Gender Inequality Ratio (Female new infections / Male new infections)
Gender Inequality Ratio =
VAR FemaleInf =
    CALCULATE ( \\\[Total New Infections], hiv\\\_data\\\[sex] = "Female" )
VAR MaleInf =
    CALCULATE ( \\\[Total New Infections], hiv\\\_data\\\[sex] = "Male" )
RETURN
    DIVIDE ( FemaleInf, MaleInf )
```

## Recommended Dashboard Layout (single canvas, 16:9)

|Zone|Visual|Bound measure|
|-|-|-|
|**Top band — KPI cards**|3 cards|`Total New Infections`, `Gender Inequality Ratio`, `YoY Death Change %`|
|**Left slicer rail**|Vertical slicers|`unicef\\\_region`, `year` (range slider)|
|**Upper-left**|Line chart|New infections over time, legend = `sex`|
|**Upper-right**|Filled map / bar|Mean `incidence\\\_rate` by country (hotspot view)|
|**Lower-left**|Combo chart|PLHIV (column) vs. death rate (line) — the ART decoupling story|
|**Lower-right**|Clustered bar|Incidence rate by `sex` within region (risk stratification)|

**Slicer placement:** anchor `Region` and `Year` on the left rail so every visual responds to a single cross-filter context. Set the line chart's title to reflect the selected region dynamically. Apply a conditional-formatting rule on the hotspot map (red ≥ 15 per 1,000) to mirror the Python alert palette for visual consistency across the stack.

