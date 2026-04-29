import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title="Sales Dashboard", layout="wide")

st.title("📊 Sales Performance Dashboard")

# Upload file
uploaded_file = st.file_uploader("Upload your sales data (CSV)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("Raw Data")
    st.write(df.head())

    # Convert Date column
    df['Date'] = pd.to_datetime(df['Date'])

    # Sidebar filters
    st.sidebar.header("Filters")
    region = st.sidebar.multiselect("Select Region", df['Region'].unique(), default=df['Region'].unique())
    product = st.sidebar.multiselect("Select Product", df['Product'].unique(), default=df['Product'].unique())

    filtered_df = df[(df['Region'].isin(region)) & (df['Product'].isin(product))]

    # KPIs
    total_sales = filtered_df['Sales'].sum()
    total_profit = filtered_df['Profit'].sum()

    col1, col2 = st.columns(2)
    col1.metric("Total Sales", f"${total_sales}")
    col2.metric("Total Profit", f"${total_profit}")

    # Sales over time
    sales_trend = filtered_df.groupby('Date')['Sales'].sum().reset_index()
    fig1 = px.line(sales_trend, x='Date', y='Sales', title="Sales Over Time")
    st.plotly_chart(fig1, use_container_width=True)

    # Sales by region
    fig2 = px.bar(filtered_df, x='Region', y='Sales', color='Region', title="Sales by Region")
    st.plotly_chart(fig2, use_container_width=True)

    # Top products
    top_products = filtered_df.groupby('Product')['Sales'].sum().sort_values(ascending=False).reset_index()
    fig3 = px.bar(top_products, x='Product', y='Sales', title="Top Products")
    st.plotly_chart(fig3, use_container_width=True)

else:
    st.info("Please upload a CSV file to continue.")