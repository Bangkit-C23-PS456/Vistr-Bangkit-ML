from flask import request
import tensorflow as tf
from sklearn.neighbors import NearestNeighbors
import pandas as pd
import numpy as np

# Define a function to fetch data from the database and return it as a DataFrame
todo = pd.read_json('./data/todo.json')

def recommend_places(activity, category, latitude, longitude, quantity):
    # Get the user's preferences from the request

    # Define the user's preferences
    activity = str(activity)
    category = str(category)
    latitude = latitude
    longitude = longitude

    # Calculate the distance between the user's location and the places' locations
    todo["distance"] = tf.sqrt(
        tf.square(todo["latitude"] - latitude) + tf.square(todo["longitude"] - longitude)
    )

    # Filter the places based on the user's preferences
    filtered_places = todo[
        (todo["activity"] == activity) & (todo["category"] == category)
    ]
    
    # Check if there are any matching places
    if filtered_places.empty:
        return {"recommendations": []}

    # Perform collaborative filtering using k-nearest neighbors
    X = filtered_places[["latitude", "longitude", "rating", "distance"]].values
    nbrs = NearestNeighbors(n_neighbors=quantity).fit(X)
    distances, indices = nbrs.kneighbors([[latitude, longitude, 5, 0]])

    # Get the top recommendations based on nearest neighbors
    top_indices = indices[0]
    top_recommendations = filtered_places.iloc[top_indices]

    # Create a response dictionary with the recommendations
    recommendations = []
    for _, row in top_recommendations.iterrows():
        recommendation = row.to_dict()
        recommendations.append(recommendation)

    return {"place_recommendation": recommendations}