import streamlit as st
import pandas as pd
import plotly.express as px


df = pd.read_csv("vehicles_us.csv")

df["model_year"] = df["model_year"].fillna(df["model_year"].median())
df["cylinders"] = df["cylinders"].fillna(df["cylinders"].median())
df["odometer"] = df["odometer"].fillna(df["odometer"].median())

df["paint_color"] = df["paint_color"].fillna(df["paint_color"].mode()[0])
df["is_4wd"] = df["is_4wd"].fillna(0)

df.to_csv("cleaned_vehicles_us.csv", index=False)
print(df.isnull().sum())

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

# Title
st.title("Vehicle Listings")

# Checkbox to toggle data display
show_full_data = st.checkbox("Show Full Dataset")

# Display data based on checkbox selection
if show_full_data:
    st.write("Displaying full dataset:")
    st.dataframe(df)
else:
    st.write("Displaying first 5 rows:")
    st.dataframe(df.head())

# Additional Information
st.write(f"Total Rows: {df.shape[0]}, Total Columns: {df.shape[1]}")
st.write("Checkbox Loaded")
price_range = st.slider("Select Price Range", int(df["price"].min()), int(df["price"].max()), (int(df["price"].min()), int(df["price"].max())))
filtered_df = df[(df["price"] >= price_range[0]) & (df["price"] <= price_range[1])]
st.dataframe(filtered_df)
