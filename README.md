# GDP Visualization App

Interactive visualization of global GDP data sourced from Wikipedia.

## Features

- Scrapes GDP data from Wikipedia's "List of countries by GDP (nominal)" page
- Displays interactive bar charts of countries' GDP data
- Allows users to select different years to view data
- Option to filter top N countries or view all data
- Interactive table with the underlying data

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

The application scrapes data from Wikipedia's [List of countries by GDP (nominal)](<https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)>) page, specifically using the IMF estimates table.

## Technologies Used

- **Beautiful Soup**: Web scraping library for parsing HTML content
- **Pandas**: Data manipulation and analysis
- **Streamlit**: Web application framework
- **Plotly**: Interactive visualization library
