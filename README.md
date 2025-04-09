# GDP Visualization App

Interactive visualization of global GDP data sourced directly from the International Monetary Fund (IMF).

## Features

- Fetches GDP data directly from the IMF's World Economic Outlook database
- Displays bar chart, map and table of countries' GDP data
- Allows users to select different years (2022-2029) to view data
- Pagination with adjustable countries per page (25, 50, 100, or All)

## Installation

1. Clone this repository:

   ```
   git clone https://github.com/yourusername/gdp-overview.git
   cd gdp-overview
   ```

2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the Streamlit app:

```
streamlit run app.py
```

This will start a local web server and open the application in your default web browser.

## Data Source

The application fetches data directly from the IMF's [World Economic Outlook Database](https://www.imf.org/en/Publications/WEO/weo-database/2024/October), which includes GDP projections from 2022 to 2029.

## Technologies Used

- **Pandas**: Data manipulation and analysis
- **Streamlit**: Web application framework
- **Plotly**: Interactive visualization library
- **Requests/Pandas**: Data fetching from IMF website
