# Sales Dashboard

A modular, interactive sales analytics application built with Streamlit. Explore sales data at annual, monthly, and daily granularity, track KPI growth metrics, and generate time-series forecasts by store, product, or city — all from a single interface backed by SQLite.

[Streamlit APP](https://selldashboard-rnpp7zpkvfdrkslnagjymy.streamlit.app/)

---

## Features

- **Multi-granularity analysis** — Annual, monthly, and daily sales breakdowns with interactive filtering by city, store, and product family
- **Global overview** — Time evolution of total sales, aggregated views by store and product family
- **KPI tracking** — Month-over-month and year-over-year growth metrics
- **Time-series forecasting** — Hybrid Linear Regression + SARIMAX model with Fourier seasonality components, segmented by store, product, or city
- **Excel export** — Download any analysis view as a formatted `.xlsx` file directly from the dashboard

---

## Tech Stack

| Package | Role |
|---|---|
| `streamlit` | Web UI, navigation, and interactive widgets |
| `pandas` | Data loading, aggregation, and time series manipulation |
| `plotly` | Interactive charts (time series, bar charts) |
| `matplotlib` | Supplementary daily plots |
| `statsmodels` | SARIMAX modeling, DeterministicProcess, CalendarFourier |
| `scikit-learn` | Linear regression for deterministic trend/seasonality |
| `xlsxwriter` | In-memory Excel file generation |
| `sqlite3` | Pre-aggregated data backend (stdlib, no install needed) |

---

## Project Structure

```
.
├── dashboard_streamlit.py      # Main entrypoint: navigation, DB connection, routing
├── modules.py                  # Global overview page (total sales, by store, by family)
├── modules_anuales.py          # Annual sales analysis and export
├── modules_mensuales.py        # Monthly sales analysis and export
├── modules_diarias.py          # Daily sales analysis with averaging modes and export
├── KPIs.py                     # Monthly and yearly KPI growth computations
├── time_series.py              # Time series entry points (by store, product, city)
├── modules_time_series.py      # Shared forecasting pipeline: PredictAndGraph()
├── toExcel.py                  # Shared Excel export helper
├── db.db                       # SQLite database (development)
├── db_deployment.db            # SQLite database (deployment)
└── requirements.txt            # Python dependencies
```

---

## Architecture

The application follows a clear modular pattern. `dashboard_streamlit.py` handles the sidebar navigation and SQLite connection, then dispatches to specialized modules based on the user's selection.

```
App start
  └── Sidebar selection
        ├── Global information      → modules.first_page()
        ├── Annual sales            → modules_anuales.graph_years()
        ├── Monthly sales           → modules_mensuales.graph_monthly*()
        ├── Daily sales             → modules_diarias.graph_daily*()
        ├── KPIs                    → KPIs.KPIs()
        ├── Predictions by Store    → time_series.TimeSeriesTiendas()
        ├── Predictions by Product  → time_series.TimeSeriesProductos()
        └── Predictions by City     → time_series.TimeSeriesCiudades()
```

All modules share a single SQLite connection and read from pre-aggregated tables:

| Table | Used by |
|---|---|
| `sales_by_date` | Global overview |
| `sales_by_store` | Global overview |
| `sales_by_family` | Global overview |
| `df_by_year_and_store` | Annual analysis |
| `df_by_year_month_and_store` | Monthly analysis |
| `df_by_year_month_day_and_store` | Daily analysis |
| `sales_by_date_and_store_and_promotion` | Store forecasting |
| `sales_by_date_and_family_and_promotion` | Product forecasting |
| `sales_by_date_and_promotion` | Aggregated forecasting |
| `cities_store` | Store/city selection |
| `productos` | Product family selection |

---

## Forecasting Pipeline

The `PredictAndGraph()` function in `modules_time_series.py` implements a hybrid two-stage model:

1. **Deterministic component** — A `LinearRegression` is fit on the last 365 days of data using a `DeterministicProcess` with trend, constant, and `CalendarFourier(freq="M", order=4)` seasonal terms, plus a `onpromotion` feature
2. **Residual component** — A `SARIMAX(order=(7, 1, 4))` model is fit on the residuals from step 1
3. **Forecast** — Both components are combined to produce the final prediction over a user-selected future date range, displayed alongside historical data in an interactive Plotly chart

---

## Installation

**Requirements:** Python 3.8+

```bash
git clone https://github.com/mmatthieu1290/sales_dashboard.git
cd sales_dashboard
pip install -r requirements.txt
```

If deploying on Streamlit Cloud, ensure `packages.txt` is present for any system-level dependencies.

---

## Running the App

```bash
streamlit run dashboard_streamlit.py
```

The app will open in your browser at `http://localhost:8501`. Use the sidebar to navigate between views.

---

## Database

The app reads from `db.db` by default (development). For deployment, `db_deployment.db` is used. Both are SQLite files containing pre-aggregated sales tables — no additional database setup is required.

---

## License

This project is not currently under an open-source license. All rights reserved.
