import streamlit as st
import pandas as pd
import plotly.express as px
st.title("Test App")


df = pd.read_csv("vehicles_us.csv")

# Streamlit Header
st.header("Vehicle Sales Data Dashboard")

# Histogram: Distribution of vehicle prices
st.subheader("Price Distribution of Vehicles")
fig_hist = px.histogram(df, x="price", nbins=50, title="Histogram of Vehicle Prices")

# Checkbox to show/hide histogram
if st.checkbox("Show Histogram"):
    st.plotly_chart(fig_hist)

# Scatter Plot: Relationship between mileage and price
st.subheader("Mileage vs. Price Scatter Plot")
fig_scatter = px.scatter(df, x="odometer", y="price", color="type", 
                         title="Mileage vs Price", 
                         labels={"odometer": "Mileage", "price": "Price"})
st.plotly_chart(fig_scatter)


