import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv("vehicles_us.csv")

df["cylinders"] = df.groupby(["model", "model_year"])["cylinders"].transform(lambda x: x.fillna(x.median()))

# Fill other missing values
df["model_year"] = df["model_year"].fillna(df["model_year"].median())
df["odometer"] = df["odometer"].fillna(df["odometer"].median())
df["paint_color"] = df["paint_color"].fillna(df["paint_color"].mode()[0])
df["is_4wd"] = df["is_4wd"].fillna(0)

# Streamlit Header
st.header("Vehicle Sales Data Dashboard")

# Filters
st.sidebar.header("Filters")
price_range = st.sidebar.slider("Select Price Range", 
                                int(df["price"].min()), 
                                int(df["price"].max()), 
                                (int(df["price"].min()), int(df["price"].max())))

vehicle_types = st.sidebar.multiselect("Select Vehicle Type(s)", df["type"].unique(), default=df["type"].unique())

# Apply Filters
filtered_df = df[(df["price"] >= price_range[0]) & (df["price"] <= price_range[1])]
filtered_df = filtered_df[filtered_df["type"].isin(vehicle_types)]

# Data Display Toggle
show_full_data = st.sidebar.checkbox("Show Full Dataset")
if show_full_data:
    st.write("Displaying full dataset:")
    st.dataframe(filtered_df)
else:
    st.write("Displaying first 5 rows:")
    st.dataframe(filtered_df.head())

st.write(f"Total Rows: {filtered_df.shape[0]}, Total Columns: {filtered_df.shape[1]}")

# Price Distribution
st.subheader("Price Distribution of Vehicles")
fig_hist = px.histogram(filtered_df, x="price", nbins=50, title="Histogram of Vehicle Prices")
st.plotly_chart(fig_hist)

# Scatter Plot: Mileage vs. Price
st.subheader("Mileage vs. Price Scatter Plot")
fig_scatter = px.scatter(filtered_df, x="odometer", y="price", color="type", 
                         title="Mileage vs Price", 
                         labels={"odometer": "Mileage", "price": "Price"})
st.plotly_chart(fig_scatter)

# Data Visualizations with Filters Applied
st.subheader("Data Distributions")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

sns.histplot(filtered_df["price"], bins=50, kde=True, ax=axes[0, 0])
axes[0, 0].set_title("Filtered Distribution of Vehicle Prices")

sns.histplot(filtered_df["odometer"], bins=50, kde=True, ax=axes[0, 1])
axes[0, 1].set_title("Filtered Distribution of Odometer Readings")

sns.histplot(filtered_df["model_year"], bins=50, kde=True, ax=axes[1, 0])
axes[1, 0].set_title("Filtered Distribution of Model Year")

sns.histplot(filtered_df["cylinders"], bins=20, kde=True, ax=axes[1, 1])
axes[1, 1].set_title("Filtered Distribution of Cylinders")

plt.tight_layout()
st.pyplot(fig)

# Box Plots
st.subheader("Box Plots for Key Variables")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

sns.boxplot(y=filtered_df["price"], ax=axes[0, 0])
axes[0, 0].set_title("Box Plot of Vehicle Prices")

sns.boxplot(y=filtered_df["odometer"], ax=axes[0, 1])
axes[0, 1].set_title("Box Plot of Odometer Readings")

sns.boxplot(y=filtered_df["model_year"], ax=axes[1, 0])
axes[1, 0].set_title("Box Plot of Model Year")

sns.boxplot(y=filtered_df["cylinders"], ax=axes[1, 1])
axes[1, 1].set_title("Box Plot of Cylinders")

plt.tight_layout()
st.pyplot(fig)

# Categorical Distributions
st.subheader("Categorical Distributions")

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

sns.countplot(y=filtered_df["type"], order=filtered_df["type"].value_counts().index, ax=axes[0])
axes[0].set_title("Filtered Distribution of Vehicle Types")
axes[0].set_ylabel("Vehicle Type")
axes[0].set_xlabel("Count")

sns.countplot(y=filtered_df["paint_color"], order=filtered_df["paint_color"].value_counts().index, ax=axes[1])
axes[1].set_title("Filtered Distribution of Paint Colors")
axes[1].set_ylabel("Paint Color")
axes[1].set_xlabel("Count")

plt.tight_layout()
st.pyplot(fig)

