import streamlit as st
import pandas as pd
import requests

# Base URL of the Flask backend
BACKEND_URL = "http://backend:7860"

# Set the title of the Streamlit app
st.title("Super Kart Price Prediction")

# Section for online prediction
st.subheader("Online Prediction")

# Collect user input for property features
product_weight = st.number_input("Product Weight (in kg)", min_value=0.0, step=0.1, value=1.0)
product_sugar_content = st.number_input("Product Sugar Content (in grams)", min_value=0.0, step=0.1, value=1.0)
product_allocated_area = st.number_input("Product Allocated Area (ratio)", min_value=0.0, max_value=1.0, step=0.1, value=1.0)
product_type = st.selectbox("Product Type",sorted_product_types)
product_mrp = st.number_input("Product MRP (in dollars)", min_value=0.0, step=0.1, value=1.0)

# limited to only existing stores
store_establishment_year = st.selectbox("Store Establishment Year", [1987, 1998, 1999, 2009])

store_size = st.selectbox("Store Size", ["Small", "Medium", "Large"])
store_location_city_type = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
store_location_type = st.selectbox("Store Location Type", ["Supermarket", "Grocery Store"])
store_type = st.selectbox("Store Type", [
  "Supermarket Type2", "Supermarket Type1", "Department Store", "Food Mart"
])

# Convert user input into a DataFrame
input_data = pd.DataFrame([{
    'product_weight': product_weight,
    'product_sugar_content': product_sugar_content,
    'product_allocated_area': product_allocated_area,
    'product_type': product_type,
    'product_mrp': product_mrp,
    'store_establishment_year': store_establishment_year,
    'store_size': store_size,
    'store_location_city_type': store_location_city_type,
    'store_location_type': store_location_type,
    'store_type': store_type
}])

# Make prediction when the "Predict" button is clicked
if st.button("Predict", type="primary"):
    response = requests.post(f"{BACKEND_URL}/v1/prediction", json=input_data.to_dict(orient='records')[0])  # Send data to Flask API
    if response.status_code == 200:
        prediction = response.json()['Predicted Price (in dollars)']
        st.success(f"Predicted  Price (in dollars): {prediction}")
    else:
        st.error("Unable to connect to the prediction API.")

# Section for batch prediction
st.subheader("Batch Prediction")

# Allow users to upload a CSV file for batch prediction
uploaded_file = st.file_uploader("Upload CSV file for batch prediction", type=["csv"])

# Make batch prediction when the "Predict Batch" button is clicked
if uploaded_file is not None:
    if st.button("Predict Batch", type="primary"):
        response = requests.post(f"{BACKEND_URL}/v1/batch_prediction", files={"file": uploaded_file})  # Send file to Flask API
        if response.status_code == 200:
            predictions = response.json()
            st.success("Batch predictions completed!")
            st.write(predictions)  # Display the predictions
        else:
            st.error("Unable to connect to the prediction API.")
