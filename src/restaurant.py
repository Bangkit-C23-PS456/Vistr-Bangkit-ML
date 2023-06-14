import tensorflow as tf
from sklearn.neighbors import NearestNeighbors
import pandas as pd
import numpy as np

# Function to recommend restaurants based on latitude and longitude
def recommend_restaurants(latitude, longitude, quantity):

     # Calculate the distance between the user's location and the places' locations
     restaurant["distance"] = tf.sqrt(
         tf.square(restaurant["latitude"] - latitude) + tf.square(restaurant["longitude"] - longitude)
     )

     # Takes latitude, longitude, rating, and distance columns as features
     X = restaurant[['latitude', 'longitude', 'rating', 'distance']].values

     # Build the KNN model with the number of neighbors (k) = quantity
     knn = NearestNeighbors(n_neighbors=quantity)
     knn.fit(X)

     # Search for 5 nearest neighbors of given position
     distances, indices = knn.kneighbors([[latitude, longitude, 5, 0]])

     # Displays recommended restaurants
     restaurant_recommendations = []
     for index in indices[0]:
         recommendation = restaurant.iloc[index].to_dict()
         restaurant_recommendations. append(recommendation)
        
     # Checks if distance is a multiple of 20, then sorts by best rating
     if int(restaurant.iloc[indices[0][0]]['distance']) % 20 == 0:
         restaurant_recommendations = sorted(restaurant_recommendations, key=lambda x: x['rating'], reverse=True)

     return {"restaurant_recommendation": restaurant_recommendations}