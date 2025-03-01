import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv("vehicles_us.csv")

# Fill missing values
df["model_year"] = df["model_year"].fillna(df["model_year"].median())
df["cylinders"] = df["cylinders"].fillna(df["cylinders"].median())
df["odometer"] = df["odometer"].fillna(df["odometer"].median())
df["paint_color"] = df["paint_color"].fillna(df["paint_color"].mode()[0])
df["is_4wd"] = df["is_4wd"].fillna(0)

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

# Price Range Filter
price_range = st.slider("Select Price Range", 
                        int(df["price"].min()), 
                        int(df["price"].max()), 
                        (int(df["price"].min()), int(df["price"].max())))

filtered_df = df[(df["price"] >= price_range[0]) & (df["price"] <= price_range[1])]
st.dataframe(filtered_df)

# Vehicle Type Filter
vehicle_types = st.multiselect("Select Vehicle Type(s)", df["type"].unique(), default=df["type"].unique())
filtered_df = filtered_df[filtered_df["type"].isin(vehicle_types)]
st.dataframe(filtered_df)

# Additional Data Visualizations
st.subheader("Additional Data Visualizations")

# Histograms for key numeric variables
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

sns.histplot(df["price"], bins=50, kde=True, ax=axes[0, 0])
axes[0, 0].set_title("Distribution of Vehicle Prices")

sns.histplot(df["odometer"], bins=50, kde=True, ax=axes[0, 1])
axes[0, 1].set_title("Distribution of Odometer Readings")

sns.histplot(df["model_year"], bins=50, kde=True, ax=axes[1, 0])
axes[1, 0].set_title("Distribution of Model Year")

sns.histplot(df["cylinders"], bins=20, kde=True, ax=axes[1, 1])
axes[1, 1].set_title("Distribution of Cylinders")

plt.tight_layout()
st.pyplot(fig)

# Box Plots for Outlier Detection
st.subheader("Box Plots for Key Variables")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

sns.boxplot(y=df["price"], ax=axes[0, 0])
axes[0, 0].set_title("Box Plot of Vehicle Prices")

sns.boxplot(y=df["odometer"], ax=axes[0, 1])
axes[0, 1].set_title("Box Plot of Odometer Readings")

sns.boxplot(y=df["model_year"], ax=axes[1, 0])
axes[1, 0].set_title("Box Plot of Model Year")

sns.boxplot(y=df["cylinders"], ax=axes[1, 1])
axes[1, 1].set_title("Box Plot of Cylinders")

plt.tight_layout()
st.pyplot(fig)

# Categorical Distributions
st.subheader("Categorical Distributions")

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

sns.countplot(y=df["type"], order=df["type"].value_counts().index, ax=axes[0])
axes[0].set_title("Distribution of Vehicle Types")
axes[0].set_ylabel("Vehicle Type")
axes[0].set_xlabel("Count")

sns.countplot(y=df["paint_color"], order=df["paint_color"].value_counts().index, ax=axes[1])
axes[1].set_title("Distribution of Paint Colors")
axes[1].set_ylabel("Paint Color")
axes[1].set_xlabel("Count")

plt.tight_layout()
st.pyplot(fig)


