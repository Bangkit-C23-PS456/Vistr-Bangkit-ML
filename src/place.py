from flask import request
import tensorflow as tf
from sklearn.neighbors import NearestNeighbors
import pandas as pd
import numpy as np

# Define a function to fetch data from the database and return it as a DataFrame
def place_df():
    places_df = places_df = pd.read_json('./data/todo.json')
    return places_df

def get_recommendation_place_nn(user_activity, user_category, user_latitude, user_longitude):
    # Get the user's preferences from the request

    # Define the user's preferences
    user_activity = str(user_activity)
    user_category = str(user_category)
    user_latitude = user_latitude
    user_longitude = user_longitude

    # Fetch the places data from the database
    places_df = place_df()

    # Calculate the distance between the user's location and the places' locations
    places_df["distance"] = tf.sqrt(
        tf.square(places_df["latitude"] - user_latitude) + tf.square(places_df["longitude"] - user_longitude)
    )

    # Filter the places based on the user's preferences
    filtered_places = places_df[
        (places_df["activity"] == user_activity) & (places_df["category"] == user_category)
    ]
    
    # Check if there are any matching places
    if filtered_places.empty:
        return {"recommendations": []}

    # Perform collaborative filtering using k-nearest neighbors
    X = filtered_places[["latitude", "longitude"]].values
    nbrs = NearestNeighbors(n_neighbors=3).fit(X)
    distances, indices = nbrs.kneighbors([[user_latitude, user_longitude]])

    # Get the top recommendations based on nearest neighbors
    top_indices = indices[0]
    top_recommendations = filtered_places.iloc[top_indices]

    # Create a response dictionary with the recommendations
    recommendations = []
    for _, row in top_recommendations.iterrows():
        recommendation = row.to_dict()
        recommendations.append(recommendation)

    return {"recommendations": recommendations}