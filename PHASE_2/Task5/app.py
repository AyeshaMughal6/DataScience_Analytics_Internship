import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(page_title="Global Superstore Analytics", layout="wide")

# 1. Load Data
@st.cache_data # This keeps the app fast by caching the data
def load_data():
    # Note: Ensure the dataset is in the same folder
    df = pd.read_excel("Global_Superstore.xls")
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    return df

df = load_data()

# 2. Sidebar Filters
st.sidebar.header("Filter the Data")
region = st.sidebar.multiselect("Select Region", options=df["Region"].unique(), default=df["Region"].unique())
category = st.sidebar.multiselect("Select Category", options=df["Category"].unique(), default=df["Category"].unique())

# Filter the dataframe based on selection
df_selection = df.query("Region == @region & Category == @category")

# 3. Main Page - Key Performance Indicators (KPIs)
st.title("Business Performance Dashboard")
st.markdown("##")

total_sales = int(df_selection["Sales"].sum())
total_profit = int(df_selection["Profit"].sum())
avg_shipping = round(df_selection["Shipping Cost"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales:,}")
with middle_column:
    st.subheader("Total Profit:")
    st.subheader(f"US $ {total_profit:,}")
with right_column:
    st.subheader("Avg Shipping Cost:")
    st.subheader(f"US $ {avg_shipping}")

st.markdown("---")

# 4. Sales by Segment (Bar Chart)
sales_by_segment = df_selection.groupby(by=["Segment"]).sum(numeric_only=True)[["Sales"]].sort_values(by="Sales")
fig_sales = px.bar(
    sales_by_segment,
    x="Sales",
    y=sales_by_segment.index,
    orientation="h",
    title="<b>Sales by Segment</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_segment),
    template="plotly_white",
)

# 5. Profit by Month (Line Chart)
df_selection['Month'] = df_selection['Order Date'].dt.to_period('M').astype(str)
line_chart_data = df_selection.groupby("Month").sum(numeric_only=True)[["Profit"]].reset_index()
fig_profit = px.line(line_chart_data, x="Month", y="Profit", title="<b>Profit Trend Over Time</b>")

left_chart, right_chart = st.columns(2)
left_chart.plotly_chart(fig_sales, use_container_width=True)
right_chart.plotly_chart(fig_profit, use_container_width=True)

# 6. Top 5 Customers
st.markdown("---")
st.subheader("Top 5 Customers by Sales")
top_customers = df_selection.groupby("Customer Name").sum(numeric_only=True)[["Sales"]].sort_values(by="Sales", ascending=False).head(5)
st.table(top_customers)