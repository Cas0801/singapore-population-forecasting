# Data contract

The canonical processed table contains one row per calendar year:

| column | type | description |
| --- | --- | --- |
| `year` | integer | Calendar year, unique and ascending |
| `population` | numeric | Total resident population under the selected source definition |

Record source URLs, download dates, and definition changes here before analysis. Do not mix total population, resident population, and citizen population without explicitly modelling the break.
