
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="IBM E-Commerce Dashboard", layout="wide")

st.title("IBM Advanced E-Commerce Dashboard")

@st.cache_data
def load_data():
    amazon = pd.read_excel("Amazon_Products_2017_2026.xlsx")
    flipkart = pd.read_excel("Flipkart_Products_2017_2026.xlsx")
    meesho = pd.read_excel("Meesho_Products_2017_2026.xlsx")
    return amazon, flipkart, meesho

amazon, flipkart, meesho = load_data()

company_option = st.sidebar.selectbox(
    "Choose Company",
    ["Amazon", "Flipkart", "Meesho"]
)

if company_option == "Amazon":
    df = amazon
elif company_option == "Flipkart":
    df = flipkart
else:
    df = meesho

st.sidebar.header("Filters")

selected_year = st.sidebar.selectbox(
    "Select Year",
    sorted(df["Year"].unique())
)

search_product = st.sidebar.text_input(
    "Search Product"
)

filtered_df = df[df["Year"] == selected_year]

if search_product:
    filtered_df = filtered_df[
        filtered_df["Product Name"].str.contains(search_product, case=False)
    ]

st.subheader(f"{company_option} Dataset")
st.dataframe(filtered_df)

st.subheader("Revenue Analysis")

revenue_month = filtered_df.groupby("Month")["Revenue"].sum().reset_index()

fig1 = px.line(
    revenue_month,
    x="Month",
    y="Revenue",
    markers=True,
    title=f"{company_option} Monthly Revenue ({selected_year})"
)

st.plotly_chart(fig1, use_container_width=True)

st.subheader("Category Sales")

category_sales = filtered_df.groupby("Category")["Units Sold"].sum().reset_index()

fig2 = px.bar(
    category_sales,
    x="Category",
    y="Units Sold",
    color="Category",
    title="Category Wise Product Sales"
)

st.plotly_chart(fig2, use_container_width=True)

st.subheader("Top Selling Products")

top_products = filtered_df.groupby("Product Name")["Units Sold"].sum().reset_index()
top_products = top_products.sort_values(by="Units Sold", ascending=False)

fig3 = px.pie(
    top_products.head(10),
    values="Units Sold",
    names="Product Name",
    title="Top 10 Selling Products"
)

st.plotly_chart(fig3, use_container_width=True)

st.subheader("Growth vs Loss")

fig4 = px.scatter(
    filtered_df,
    x="Growth %",
    y="Loss %",
    color="Category",
    size="Units Sold",
    hover_data=["Product Name"],
    title="Growth vs Loss Analysis"
)

st.plotly_chart(fig4, use_container_width=True)

st.subheader("Highest Sold Month")

highest_month = revenue_month.sort_values(by="Revenue", ascending=False).iloc[0]

st.success(
    f"Highest Revenue Month in {selected_year}: "
    f"{highest_month['Month']} "
    f"(Revenue: {highest_month['Revenue']:.2f})"
)

st.subheader("Highest Price Product")

max_product = filtered_df.loc[filtered_df["High Price"].idxmax()]

st.write(max_product)

st.subheader("Lowest Price Product")

min_product = filtered_df.loc[filtered_df["High Price"].idxmin()]

st.write(min_product)

uploaded_file = st.file_uploader("Upload New Dataset", type=["xlsx"])

if uploaded_file:
    new_df = pd.read_excel(uploaded_file)
    st.success("Dataset Uploaded Successfully")
    st.dataframe(new_df.head(50))
