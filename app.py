import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv("world_population_worldbank.csv")

# Get latest year in dataset
latest_year = 2023

# Sidebar for user selection
st.sidebar.title("Global Population Insights")
page = st.sidebar.selectbox("Select a visualization:", [
    f"Top 10 Most Populous Countries in {latest_year}",
    "Population Growth of Selected Countries",
    "Total Global Population",
    "Top 10 Fastest Growing Countries (1960-2023)",
    "Population Trends by Region (1960-2023)",
    "Global Average Population Growth Per Decade",
    "Top 10 Fastest Growing Small States (1960-2023)",
    "Population Trends: Small States vs. Other Groups (1960-2023)",
    "Which Income Group Is Growing the Fastest? (1960-2023)",
    "Population Trends: High-Income vs. Low-Income Countries (1960-2023)",
    "Are Middle-Income Countries Experiencing Rapid Urbanization? (1960-2023)"
])

# Function to create a bar chart
def plot_bar_chart(data, x, y, title, xlabel, ylabel):
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=x, y=y, data=data, palette="viridis", ax=ax)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    st.pyplot(fig)

# Function to create a line chart
def plot_line_chart(data, title, xlabel, ylabel):
    fig, ax = plt.subplots(figsize=(12, 6))
    for column in data.columns:
        ax.plot(data.index, data[column], marker="o", label=column)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend()
    st.pyplot(fig)

# ...existing code...
# Top 10 Most Populous Countries
if page == f"Top 10 Most Populous Countries in {latest_year}":
    # Load a list of official country codes (ISO 3166)
    official_countries = set(pd.read_csv("https://raw.githubusercontent.com/datasets/country-codes/main/data/country-codes.csv")["ISO3166-1-Alpha-3"].dropna())
    
    # Filter only actual countries based on Country Code
    df_filtered = df[df["Country Code"].isin(official_countries)]
    
    # Convert latest_year to string
    latest_year_str = str(latest_year)
    
    if latest_year_str in df_filtered.columns:
        top_countries = df_filtered[["Country Name", latest_year_str]].sort_values(by=latest_year_str, ascending=False).head(10)
        plot_bar_chart(top_countries, latest_year_str, "Country Name", f"Top 10 Most Populous Countries in {latest_year}", "Population", "Country")
    else:
        st.error(f"Data for the year {latest_year} is not available.")

# Population Growth of Selected Countries
elif page == "Population Growth of Selected Countries":
    selected_countries = st.multiselect("Select countries:", df["Country Name"].unique(), default=["India", "China", "United States"])
    pop_trends = df[df["Country Name"].isin(selected_countries)].set_index("Country Name").T.iloc[1:]
    pop_trends.index = pop_trends.index.astype(int)
    plot_line_chart(pop_trends, "Population Growth of Selected Countries", "Year", "Population")

# Total Global Population
elif page == "Total Global Population":
    world_population = df[df["Country Name"] == "World"].set_index("Country Name").T.iloc[1:]
    world_population.index = world_population.index.astype(int)
    plot_line_chart(world_population, "Total Global Population (1960-2023)", "Year", "Population")

# Top 10 Fastest Growing Countries
elif page == "Top 10 Fastest Growing Countries (1960-2023)":
    df["Growth Rate"] = ((df[str(latest_year)] - df["1960"]) / df["1960"]) * 100
    fastest_growing = df[['Country Name', "Growth Rate"]].nlargest(10, "Growth Rate")
    plot_bar_chart(fastest_growing, "Growth Rate", "Country Name", "Top 10 Fastest Growing Countries (1960-2023)", "Growth Rate (%)", "Country")

# Population Trends by Region
elif page == "Population Trends by Region (1960-2023)":
    regions = ["East Asia & Pacific", "Europe & Central Asia", "Latin America & Caribbean", "Middle East & North Africa", "North America", "South Asia", "Sub-Saharan Africa"]
    regional_trends = df[df["Country Name"].isin(regions)].set_index("Country Name").T.iloc[1:]
    regional_trends.index = regional_trends.index.astype(int)
    plot_line_chart(regional_trends, "Population Trends by Region (1960-2023)", "Year", "Population")

# Which Income Group Is Growing the Fastest?
elif page == "Which Income Group Is Growing the Fastest? (1960-2023)":
    income_groups = ["High income", "Upper middle income", "Lower middle income", "Low income"]
    income_df = df[df["Country Name"].isin(income_groups)].copy()
    income_df["Growth Rate"] = ((income_df[str(latest_year)] - income_df["1960"]) / income_df["1960"]) * 100
    fastest_income_growth = income_df[["Country Name", "Growth Rate"]].sort_values("Growth Rate", ascending=False)
    plot_bar_chart(fastest_income_growth, "Growth Rate", "Country Name", "Which Income Group Is Growing the Fastest?", "Growth Rate (%)", "Income Group")

# Population Trends: High-Income vs. Low-Income Countries
elif page == "Population Trends: High-Income vs. Low-Income Countries (1960-2023)":
    income_trends = df[df["Country Name"].isin(["High income", "Low income"])].set_index("Country Name").T.iloc[1:]
    income_trends.index = income_trends.index.astype(int)
    plot_line_chart(income_trends, "Population Trends: High-Income vs. Low-Income Countries (1960-2023)", "Year", "Population")

# Are Middle-Income Countries Experiencing Rapid Urbanization?
elif page == "Are Middle-Income Countries Experiencing Rapid Urbanization? (1960-2023)":
    mid_income_trends = df[df["Country Name"].isin(["Upper middle income", "Lower middle income"])].set_index("Country Name").T.iloc[1:]
    mid_income_trends.index = mid_income_trends.index.astype(int)
    plot_line_chart(mid_income_trends, "Are Middle-Income Countries Experiencing Rapid Urbanization? (1960-2023)", "Year", "Population")

st.sidebar.markdown("### Data Source: World Bank")
