import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import io
import re
import numpy as np
import math
from functools import lru_cache

# Set page configuration
st.set_page_config(page_title="Global GDP Visualization", page_icon="📊", layout="wide")

# Custom CSS to improve the UI
st.markdown(
    """
<style>
    /* Overall app styling */
    .main {
        background-color: #f8f9fa;
        color: #212529;
    }
    
    /* Title styling */
    h1 {
        color: #0466c8;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.75rem !important;
        padding-bottom: 0.5rem !important;
    }
    
    /* Description text */
    .app-description {
        color: #495057;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
        max-width: 800px;
        line-height: 1.6;
    }
    
    /* Tabs styling - eliminate white space */
    .stTabs {
        background-color: transparent !important;
        padding: 0 !important;
        margin-top: 0 !important;
        margin-bottom: 0 !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-size: 1rem;
        font-weight: 600;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        margin-bottom: 0 !important;
        padding-bottom: 0 !important;
        background-color: transparent !important;
    }

    
    /* Fix for container background - remove nested white boxes */
    .stTabs [data-baseweb="tab-panel"] {
        padding: 0 !important;
        background-color: transparent !important;
        box-shadow: none !important;
        margin-top: 0 !important;
    }
    
    
    /* Year selector styling */
    .year-selector {
        margin-bottom: 0.125rem;
        margin-top: 0.125rem;
    }
    
    h3 {
        color: #0466c8;
        font-size: 1.25rem !important;
        font-weight: 600 !important;
        margin-top: 0.5rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    div[data-testid="stSelectbox"] {
        min-width: 200px;
        max-width: 300px;
        margin-bottom: 1.5rem;
    }
    
    div[data-testid="stSelectbox"] > div > div {
        background-color: white;
        border-radius: 8px;
        border: 1px solid #dee2e6;
    }
    
    /* Chart styling */
    .stPlotlyChart {
        overflow-y: auto;
        background-color: white;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    
    /* Dataframe styling */
    [data-testid="stDataFrame"] {
        background-color: white;
        border-radius: 8px;
        padding: 0.5rem;
        border: 1px solid #f8f9fa;
    }
    
    /* Improved pagination styling */
    .pagination {
        display: flex;
        justify-content: flex-start;
        align-items: center;
        margin: 1.5rem 0;
    }
    
    .pagination button, .pagination-disabled {
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        padding: 0.5rem 1rem !important;
        border-radius: 6px !important;
        transition: all 0.2s ease-in-out !important;
        width: 100% !important;
        text-align: center !important;
    }
    
    .pagination button {
        background-color: #0466c8 !important;
        color: white !important;
        border: none !important;
    }
    
    .pagination button:hover {
        background-color: #0353a4 !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1) !important;
    }
    
    /* Current page indicator */
    .current-page {
        font-weight: 600;
        color: #0466c8;
        font-size: 1rem;
        padding: 0.5rem 1rem;
        background-color: #f8f9fa;
        border-radius: 6px;
        display: inline-block;
    }
    
    /* Countries per page selector */
    .countries-selector {
        display: flex;
        justify-content: flex-end;
        align-items: center;
    }
    
    .countries-selector label {
        color: #495057;
        font-weight: 500;
        margin-right: 0.5rem;
    }
    
    .countries-selector [data-testid="stSelectbox"] {
        min-width: 120px;
    }
    
    /* Footer styling */
    .footer {
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid #e9ecef;
        color: #6c757d;
        font-size: 0.9rem;
    }
    
    /* App header container */
    .app-header {
        display: flex;
        align-items: center;
        margin-bottom: 0.5rem;
        margin-top: 1rem;
    }
    
    /* Globe icon styling */
    .globe-icon {
        font-size: 2.5rem;
        margin-right: 0.5rem;
        vertical-align: middle;
        display: inline-block;
    }
    
    /* For mobile responsiveness */
    @media (max-width: 768px) {
        h1 {
            font-size: 1.8rem !important;
        }
        .globe-icon {
            font-size: 2rem;
        }
    }
</style>
""",
    unsafe_allow_html=True,
)


@lru_cache(maxsize=1)
def fetch_imf_gdp_data():
    """
    Fetch GDP data directly from the IMF's World Economic Outlook database
    Returns a pandas DataFrame with the data
    """
    # IMF data URL - World Economic Outlook database
    url = "https://www.imf.org/en/Publications/WEO/weo-database/2024/October/weo-report?c=512,914,612,171,614,311,213,911,314,193,122,912,313,419,513,316,913,124,339,638,514,218,963,616,223,516,918,748,618,624,522,622,156,626,628,228,924,233,632,636,634,238,662,960,423,935,128,611,321,243,248,469,253,642,643,939,734,644,819,172,132,646,648,915,134,652,174,328,258,656,654,336,263,268,532,944,176,534,536,429,433,178,436,136,343,158,439,916,664,826,542,967,443,917,544,941,446,666,668,672,946,137,546,674,676,548,556,678,181,867,682,684,273,868,921,948,943,686,688,518,728,836,558,138,196,278,692,694,962,142,449,564,565,283,853,288,293,566,964,182,359,453,968,922,714,862,135,716,456,722,942,718,724,576,936,961,813,726,199,733,184,524,361,362,364,732,366,144,146,463,528,923,738,578,537,742,866,369,744,186,925,869,746,926,466,112,111,298,927,846,299,582,487,474,754,698,&s=NGDPD,&sy=2022&ey=2029&ssm=0&scsm=1&scc=0&ssd=1&ssc=0&sic=0&sort=country&ds=.&br=1"

    try:
        # Use pandas to read the HTML table directly
        tables = pd.read_html(url)

        # Find the GDP data table - typically the largest table
        gdp_df = None
        max_rows = 0
        selected_table_idx = -1

        for i, table in enumerate(tables):
            if len(table) > max_rows:
                max_rows = len(table)
                gdp_df = table
                selected_table_idx = i

        if gdp_df is None or max_rows < 10:  # Ensure we have a substantial table
            st.error("Couldn't find GDP data table on the IMF website")
            return None

        # Get all column names
        col_names = list(gdp_df.columns)

        # Find the column containing country names
        country_col = None
        for col in col_names:
            if "country" in str(col).lower():
                country_col = col
                break

        if country_col is None:
            # If we can't find a column with 'country' in the name, assume it's the first column
            country_col = col_names[0]

        # Find year columns (columns with 4-digit numbers)
        year_cols = []
        for col in col_names:
            if re.search(r"\b20\d\d\b", str(col)):
                year_cols.append(col)

        if not year_cols:
            # If we can't find year columns, look for numeric columns or columns with year-like names
            for col in col_names:
                # Check if column name itself contains a 4-digit year
                if isinstance(col, tuple) and any(
                    re.search(r"\b20\d\d\b", str(part)) for part in col
                ):
                    year_cols.append(col)
                # Check if the column contains numeric data
                elif col != country_col and pd.api.types.is_numeric_dtype(gdp_df[col]):
                    year_cols.append(col)
                # Check if column name contains "year" or "unnamed"
                elif "year" in str(col).lower() or "unnamed" in str(col).lower():
                    year_cols.append(col)

        # Create a new dataframe with just the country and year columns
        clean_df = pd.DataFrame()
        clean_df["Country"] = gdp_df[country_col].astype(str)

        # Convert years to string format YYYY
        expected_years = [
            "2022",
            "2023",
            "2024",
            "2025",
            "2026",
            "2027",
            "2028",
            "2029",
        ]

        # If we found year columns, use them
        if year_cols:
            for i, year_col in enumerate(year_cols):
                if i < len(expected_years):
                    year = expected_years[i]
                    # Extract the values and convert to numeric
                    clean_df[year] = pd.to_numeric(gdp_df[year_col], errors="coerce")
        # If no year columns were found, try to use position-based approach
        else:
            # Assume years are in columns 1-8 (after country column)
            for i, year in enumerate(expected_years):
                col_idx = i + 1  # Skip the country column
                if col_idx < len(col_names):
                    col = col_names[col_idx]
                    clean_df[year] = pd.to_numeric(gdp_df[col], errors="coerce")

        # Remove rows with missing or invalid country names
        clean_df = clean_df[clean_df["Country"].str.len() > 2]

        # Remove rows that are not countries (headers, footers, etc.)
        clean_df = clean_df[
            ~clean_df["Country"].str.contains(
                "International Monetary Fund|Subject|Descriptor|Gross domestic product",
                regex=True,
                case=False,
            )
        ]

        return clean_df

    except Exception as e:
        st.error(f"Error processing IMF data: {e}")
        import traceback

        return None


def process_data(df, selected_year):
    """
    Process the GDP data for visualization

    Args:
        df: DataFrame with GDP data
        selected_year: Year to filter the data by

    Returns:
        Processed DataFrame sorted by GDP
    """
    if df is None:
        return None

    # Select data for the chosen year
    if selected_year not in df.columns:
        st.warning(
            f"Data for {selected_year} not available. Defaulting to the most recent year."
        )
        # Get the most recent year from the numeric columns
        year_columns = [col for col in df.columns if col != "Country"]
        selected_year = year_columns[-1]

    # Filter and sort the data
    filtered_df = df[["Country", selected_year]].copy()
    filtered_df = filtered_df.dropna(subset=[selected_year])
    filtered_df = filtered_df.sort_values(by=selected_year, ascending=False)

    # Format GDP values in billions with no decimals
    filtered_df["GDP (Billions USD)"] = filtered_df[selected_year]
    filtered_df["GDP_formatted"] = filtered_df["GDP (Billions USD)"].apply(
        lambda x: f"{int(x)}" if not pd.isna(x) else ""
    )

    return filtered_df


def create_gdp_chart(df, selected_year, countries_per_page=25, page=0):
    """
    Create a bar chart visualization of GDP data

    Args:
        df: Processed DataFrame with GDP data
        selected_year: Selected year for the data
        countries_per_page: Number of countries to display per page
        page: Current page number (0-indexed)

    Returns:
        Plotly figure object
    """
    if df is None or df.empty:
        return None

    # Calculate pagination
    start_idx = page * countries_per_page
    end_idx = start_idx + countries_per_page

    # Get the subset of data for the current page
    page_df = df.iloc[start_idx:end_idx].copy()

    # Calculate dynamic height based on number of countries (minimum 600px)
    # Each country bar needs about 30px of height
    height = max(600, countries_per_page * 30)

    # Create bar chart using Plotly
    fig = px.bar(
        page_df,
        y="Country",
        x="GDP (Billions USD)",
        text="GDP_formatted",
        orientation="h",
        title=f"GDP in {selected_year} (USD Billions)",
        labels={"GDP (Billions USD)": "GDP (Billions USD)", "Country": ""},
        height=height,
        # Use a single color instead of a color scale
        color_discrete_sequence=["#0466c8"],  # Updated to match theme
    )

    # Customize the appearance
    fig.update_layout(
        xaxis_title="GDP (Billions USD)",
        yaxis={
            "categoryorder": "total ascending",
            "automargin": True,  # Give more space for country names
            "title": None,
            "tickfont": {"size": 12, "color": "#495057"},
        },
        font=dict(size=12),
        margin=dict(l=20, r=20, t=50, b=20),
        # Remove color axis/colorbar
        coloraxis_showscale=False,
        # Improve the appearance of the plot with better styling
        plot_bgcolor="white",
        paper_bgcolor="white",
        title={
            "font": {"size": 18, "color": "#212529", "family": "Arial, sans-serif"},
            "x": 0.5,
            "xanchor": "center",
        },
        xaxis={
            "showgrid": True,
            "gridwidth": 1,
            "gridcolor": "#f1f3f5",
            "title": {"font": {"size": 14, "color": "#495057"}},
        },
    )

    fig.update_traces(
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>GDP: %{text}<extra></extra>",
        marker_line_width=0,
        # Adding a slight gradient effect to bars
        marker_color="#0466c8",
        opacity=0.9,
    )

    return fig


def create_gdp_map(df, selected_year):
    """
    Create a choropleth map visualization of GDP data

    Args:
        df: Processed DataFrame with GDP data
        selected_year: Selected year for the data

    Returns:
        Plotly figure object
    """
    if df is None or df.empty:
        return None

    # Create choropleth map using Plotly
    fig = px.choropleth(
        df,
        locations="Country",  # Use country names
        locationmode="country names",  # Match names to country boundaries
        color="GDP (Billions USD)",
        hover_name="Country",
        color_continuous_scale="YlGnBu",  # Yellow-Green-Blue colorscale with 100 increments
        range_color=[0, df["GDP (Billions USD)"].max()],  # Full range of values
        title=f"Global GDP Distribution {selected_year} (USD Billions)",
        labels={"GDP (Billions USD)": "GDP (Billions USD)"},
        projection="natural earth",  # Use a more natural looking projection
    )

    # Customize the appearance
    fig.update_layout(
        coloraxis_colorbar=dict(
            title="GDP (Billions USD)",
            tickfont={"size": 12, "color": "#495057"},
            titlefont={"size": 14, "color": "#495057"},
            len=0.5,  # Make the colorbar shorter
            # Use a logarithmic scale to better show the range of values
            tickvals=[100, 1000, 5000, 10000, 20000, 30000],
            ticktext=["100", "1.000", "5.000", "10.000", "20.000", "30.000"],
            # Increase number of color segments for more granularity
            nticks=100,
        ),
        margin=dict(l=0, r=0, t=50, b=0),
        geo=dict(
            showframe=False,
            showcountries=True,
            showcoastlines=True,
            projection_type="equirectangular",
            landcolor="rgb(240, 240, 240)",
            oceancolor="rgb(220, 240, 255)",
            coastlinecolor="rgb(150, 150, 150)",
            countrycolor="rgb(150, 150, 150)",
        ),
        height=600,
        # Improve the appearance of the plot with better styling
        plot_bgcolor="white",
        paper_bgcolor="white",
        title={
            "font": {"size": 18, "color": "#212529", "family": "Arial, sans-serif"},
            "x": 0.5,
            "xanchor": "center",
        },
    )

    return fig


def pagination_controls(total_items, items_per_page, current_page, location="top"):
    """Create pagination controls

    Args:
        total_items: Total number of items to paginate
        items_per_page: Number of items per page
        current_page: Current page number (0-indexed)
        location: Identifier for the control location (top or bottom)
    """
    total_pages = math.ceil(total_items / items_per_page)

    if total_pages <= 1 and items_per_page < total_items:
        return

    # Create a more balanced layout: left for pagination, center for page info, right for dropdown
    cols = st.columns([2, 3, 2])

    # Column for page navigation
    with cols[0]:
        st.markdown('<div class="pagination">', unsafe_allow_html=True)

        # Use a simpler 2-column layout for Previous/Next buttons
        nav_cols = st.columns([1, 1])

        # Previous button
        with nav_cols[0]:
            if current_page > 0:
                if st.button(
                    "← Previous", key=f"prev_{location}", use_container_width=True
                ):
                    st.session_state.current_page = current_page - 1
                    st.rerun()
            else:
                # Disabled previous button (grayed out)
                st.markdown(
                    """<div style="width:100%; text-align:center; padding: 0.5em; 
                    background-color:#e9ecef; color:#adb5bd; border-radius:6px; 
                    border:1px solid #ced4da;">← Previous</div>""",
                    unsafe_allow_html=True,
                )

        # Next button
        with nav_cols[1]:
            if current_page < total_pages - 1:
                if st.button(
                    "Next →", key=f"next_{location}", use_container_width=True
                ):
                    st.session_state.current_page = current_page + 1
                    st.rerun()
            else:
                # Disabled next button (grayed out)
                st.markdown(
                    """<div style="width:100%; text-align:center; padding: 0.5em; 
                    background-color:#e9ecef; color:#adb5bd; border-radius:6px; 
                    border:1px solid #ced4da;">Next →</div>""",
                    unsafe_allow_html=True,
                )

        st.markdown("</div>", unsafe_allow_html=True)

    # Center column for page information
    with cols[1]:
        st.markdown(
            f'<div class="current-page" style="text-align:center; margin-top:8px;">Page {current_page + 1} of {total_pages}</div>',
            unsafe_allow_html=True,
        )

    # Column for countries per page selector (only show on the top controls)
    if location == "chart" or location == "table_top":
        with cols[2]:
            st.markdown(
                '<div class="countries-selector" style="float:right;">',
                unsafe_allow_html=True,
            )

            # Use a unique key for each location - both will update the same session state variable
            selector_key = f"countries_per_page_{location}"

            # Initialize the selector key if it doesn't exist
            if selector_key not in st.session_state:
                st.session_state[selector_key] = st.session_state.countries_per_page

            # Create the countries per page selector
            st.selectbox(
                "Show",
                ["25", "50", "100", "All"],
                key=selector_key,
                label_visibility="collapsed",
                on_change=reset_pagination_with_value,
                args=(selector_key,),
            )

            # Update the global session state
            if st.session_state.get(selector_key) != st.session_state.get(
                "countries_per_page"
            ):
                st.session_state.countries_per_page = st.session_state[selector_key]

            st.markdown("</div>", unsafe_allow_html=True)


def reset_pagination():
    """Reset pagination to first page when changing items per page"""
    st.session_state.current_page = 0


def reset_pagination_with_value(value):
    """
    Reset pagination to first page and sync selection value

    Args:
        value: Key of the selectbox that changed
    """
    st.session_state.current_page = 0

    # Update the main countries_per_page value
    if value in st.session_state:
        st.session_state.countries_per_page = st.session_state[value]


def main():
    """Main function to run the Streamlit app"""
    # Custom header with styled title and globe icon
    st.markdown(
        """<div class="app-header">
        <span class="globe-icon">🌍</span><h1 style="display: inline-block; margin-top: 0;">Global GDP Visualization</h1>
        </div>""",
        unsafe_allow_html=True,
    )

    # App description with improved styling
    st.markdown(
        """<div class="app-description">
        This application visualizes GDP data from the International Monetary Fund (IMF),
        sourced directly from the IMF's World Economic Outlook database.
        </div>""",
        unsafe_allow_html=True,
    )

    # Initialize pagination state
    if "current_page" not in st.session_state:
        st.session_state.current_page = 0

    # Initialize countries per page state
    if "countries_per_page" not in st.session_state:
        st.session_state.countries_per_page = "25"

    # Initialize active tab state
    if "active_tab" not in st.session_state:
        st.session_state.active_tab = "Chart"

    # Initialize GDP data state - only fetch once on app startup
    if "gdp_data" not in st.session_state:
        # Show loading spinner while fetching data
        with st.spinner("Fetching GDP data from IMF..."):
            st.session_state.gdp_data = fetch_imf_gdp_data()

    # Use the stored GDP data
    gdp_data = st.session_state.gdp_data

    if gdp_data is None:
        st.error("Failed to retrieve GDP data. Please try again later.")
        return

    # Year selection - ensure we display years from 2022 to 2029
    expected_years = [str(year) for year in range(2022, 2030)]
    year_columns = [col for col in gdp_data.columns if col in expected_years]

    if not year_columns:
        st.error("No year data available for 2022-2029 in the dataset")
        return

    # Year selector without label (dropdown is self-explanatory)
    st.markdown('<div class="year-selector">', unsafe_allow_html=True)
    selected_year = st.selectbox(
        "",  # Empty label - dropdown is self-explanatory
        year_columns,
        index=3,  # Default to 2025 (index 3)
        key="year_selector",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # Process the data - store processed data in session state for the selected year
    if f"processed_data_{selected_year}" not in st.session_state:
        st.session_state[f"processed_data_{selected_year}"] = process_data(
            gdp_data, selected_year
        )

    processed_data = st.session_state[f"processed_data_{selected_year}"]

    if processed_data is None or processed_data.empty:
        st.warning("No data available for the selected year.")
        return

    # Determine how many countries to display per page
    countries_per_page_str = st.session_state.countries_per_page
    total_countries = len(processed_data)

    if countries_per_page_str == "All":
        countries_per_page = total_countries
    else:
        countries_per_page = int(countries_per_page_str)

    # Calculate total number of pages
    total_pages = math.ceil(total_countries / countries_per_page)

    # Ensure current page is valid
    if st.session_state.current_page >= total_pages:
        st.session_state.current_page = 0

    # Create tabs for chart, map, and table with custom styling
    tab1, tab2, tab3 = st.tabs(["📊 Chart", "🗺️ Map", "📋 Table"])

    with tab1:  # Chart tab
        st.markdown('<div class="content-container">', unsafe_allow_html=True)

        # Display the chart for the current page
        fig = create_gdp_chart(
            processed_data,
            selected_year,
            countries_per_page=countries_per_page,
            page=st.session_state.current_page,
        )

        if fig:
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # Display pagination controls below the chart
        pagination_controls(
            total_countries,
            countries_per_page,
            st.session_state.current_page,
            location="chart",
        )

    with tab2:  # Map tab
        st.markdown('<div class="content-container">', unsafe_allow_html=True)

        # Display the map visualization
        map_fig = create_gdp_map(processed_data, selected_year)

        if map_fig:
            st.plotly_chart(map_fig, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with tab3:  # Table tab
        st.markdown('<div class="content-container">', unsafe_allow_html=True)

        # Show the data table for the current page
        start_idx = st.session_state.current_page * countries_per_page
        end_idx = min(
            start_idx + countries_per_page, total_countries
        )  # Make sure we don't go past the end
        page_data = processed_data.iloc[start_idx:end_idx].copy()

        st.dataframe(
            page_data[["Country", "GDP (Billions USD)"]].reset_index(drop=True),
            column_config={
                "Country": st.column_config.TextColumn(
                    "Country/Territory", width="medium"
                ),
                "GDP (Billions USD)": st.column_config.NumberColumn(
                    "GDP (Billions USD)", format="%d", width="small"
                ),
            },
            hide_index=True,
            use_container_width=True,
        )

        st.markdown("</div>", unsafe_allow_html=True)

        # Display pagination controls for the table
        pagination_controls(
            total_countries,
            countries_per_page,
            st.session_state.current_page,
            location="table_top",
        )

    # Add footnote with improved styling
    st.markdown(
        """<div class="footer">
        Data source: <a href="https://www.imf.org/en/Publications/WEO/weo-database/2024/October" target="_blank" style="color: #0466c8; text-decoration: none;">
        International Monetary Fund (IMF) - World Economic Outlook Database</a>
        </div>""",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
