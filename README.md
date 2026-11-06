# Task 3 — Real-World Dataset Analysis

**Prepared by Nazmus Sakib**

In this project, I analyze annual World Bank indicators for Bangladesh, India, Nepal, Pakistan, and Sri Lanka from 2000 through 2024. The panel combines GDP per capita in constant 2015 US dollars with life expectancy at birth in years. It contains 125 country-year rows and has complete observations for both indicators over the selected period.

## Project contents

- `Task_3_Real_World_Dataset_Analysis_Report.docx` — report with method, findings, charts, limitations, and references.
- `Task3_WorldBank_Analysis.ipynb` — executable notebook for inspection and analysis.
- `analyze_world_bank.py` — script that validates the included dataset, calculates summary statistics, and regenerates the four charts.
- `data/south_asia_wdi_2000_2024.csv` — tidy country-year data used in the analysis.
- `data/*_api.json` and `data/api_metadata.json` — retained World Bank API responses and update metadata.
- `figures/` — exported charts.
- `outputs/country_2000_2024_summary.csv` — endpoint changes and summary metrics.

## Reproduce

Requires Python 3.10 or later. From this folder:

```bash
python -m venv .venv
# Activate .venv for your operating system
pip install -r requirements.txt
python analyze_world_bank.py
jupyter lab
```

Open `Task3_WorldBank_Analysis.ipynb` in Jupyter to review the steps. The analysis uses the saved dataset so it can run without a network connection; the retained API JSON shows the source response. To refresh the raw data, use the World Bank Indicators API V2, documented at the URL below.

## Indicators and sources

- GDP per capita (constant 2015 US$), World Bank indicator `NY.GDP.PCAP.KD`: https://data.worldbank.org/indicator/NY.GDP.PCAP.KD
- Life expectancy at birth, total (years), indicator `SP.DYN.LE00.IN`: https://data.worldbank.org/indicator/SP.DYN.LE00.IN
- World Bank Indicators API documentation: https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api-documentation

The indicator pages identify source agencies and show a CC BY 4.0 license. Preserve attribution when reusing data. The report treats correlations as descriptive; they do not establish causation. The analysis is limited to these five economies and the 2000–2024 period.
