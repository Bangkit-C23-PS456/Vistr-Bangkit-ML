import tensorflow as tf
import os
import pandas as pd
import numpy as np
import json
import math

places_df = pd.read_json("https://storage.googleapis.com/vistr/afterFiltered.json")

def get_recommendations_tf(user_activity, user_category, user_latitude, user_longitude):
    # Define the user's preferences
    user_activity = tf.constant(user_activity, dtype=tf.string)
    user_category = tf.constant(user_category, dtype=tf.string)
    user_latitude = user_latitude
    user_longitude = user_longitude

    # Calculate the distance between the user's location and the places' locations
    places_df["distance"] = np.sqrt(
        np.square(places_df["latitude"] - user_latitude) + np.square(places_df["longitude"] - user_longitude)
    )

    # Filter the places based on the user's preferences
    filtered_places = places_df[
        (places_df["activity"] == user_activity) & (places_df["category"] == user_category)
    ]

    # Sort the filtered places by distance
    sorted_places = filtered_places.sort_values(by="distance")

    # Find the indices of the top k recommendations
    k = 3
    top_indices = sorted_places.index[:k]

    # Gather the top k recommendations from the sorted places DataFrame
    top_recommendations = sorted_places.loc[top_indices]
    recommendations_json = top_recommendations.to_json(orient="records")


    return json.loads(recommendations_json)
# Example usage

