# Import necessary libraries
import numpy as np
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation
from flask import Flask, request, jsonify  # For creating the Flask API

# Initialize the Flask application
kart_price_predictor_api = Flask("Super Kart Price Predictor")
app = kart_price_predictor_api

# Load the trained machine learning model
model = joblib.load("super_kart_prediction_model_v1_0.joblib")

# Define a route for the home page (GET request)
@kart_price_predictor_api.get('/')
def home():
    """
    This function handles GET requests to the root URL ('/') of the API.
    It returns a simple welcome message.
    """
    return "Welcome to the Super Kart Price Prediction API!"

# Define an endpoint for single property prediction (POST request)
@kart_price_predictor_api.post('/v1/prediction')
def predict_kart_price():
    """
    This function handles POST requests to the '/v1/prediction' endpoint.
    It expects a JSON payload containing property details and returns
    the predicted rental price as a JSON response.
    """
    # Get the JSON data from the request body
    kart_data = request.get_json()

    # Extract relevant features from the JSON data  
    sample = {
        'Product_Weight': kart_data['product_weight'],
        'Product_Sugar_Content': kart_data['product_sugar_content'],
        'Product_Allocated_Area': kart_data['product_allocated_area'],
        'Product_Type': kart_data['product_type'],
        'Product_MRP': kart_data['product_mrp'],
        'Store_Establishment_Year': str(kart_data['store_establishment_year']),
        'Store_Size': kart_data['store_size'],
        'Store_Location_City_Type': kart_data['store_location_city_type'],
        'Store_Location_Type': kart_data['store_location_type'],
        'Store_Type': kart_data['store_type']
    }

    # Convert the extracted data into a Pandas DataFrame
    input_data = pd.DataFrame([sample])

    # Make prediction (get log_price)
    predicted_price = model.predict(input_data)[0]

    # Convert predicted_price to Python float
    predicted_price = round(float(predicted_price), 2)

    # When we send this value directly within a JSON response, 
    # Flask's jsonify function encounters a datatype error
    # Return the actual price
    return jsonify({'Predicted Price (in dollars)': predicted_price})


# Define an endpoint for batch prediction (POST request)
@kart_price_predictor_api.post('/v1/batch_prediction')
def predict_kart_price_batch():
    """
    This function handles POST requests to the '/v1/batch_prediction' endpoint.
    It expects a CSV file containing property details for multiple properties
    and returns the predicted  prices as a dictionary in the JSON response.
    """
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the CSV file into a Pandas DataFrame
    input_data = pd.read_csv(file)

    # Make predictions for all properties in the DataFrame (get log_prices)
    predicted_log_prices = model.predict(input_data).tolist()

    # Calculate actual prices
    predicted_prices = [round(float(np.exp(log_price)), 2) for log_price in predicted_log_prices]

    # Create a dictionary of predictions with property IDs as keys
    property_ids = input_data['id'].tolist()  # Assuming 'id' is the property ID column
    output_dict = dict(zip(property_ids, predicted_prices))  # Use actual prices

    # Return the predictions dictionary as a JSON response
    return output_dict

# Run the Flask application in debug mode if this script is executed directly
if __name__ == '__main__':
    kart_price_predictor_api.run(debug=True)
