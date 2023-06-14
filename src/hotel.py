import tensorflow as tf
from sklearn.neighbors import NearestNeighbors
import pandas as pd
import numpy as np

# Function to recommend restaurants based on latitude and longitude
def recommend_hotels(latitude, longitude, quantity):

     # Calculate the distance between the user's location and the places' locations
     hotel["distance"] = tf.sqrt(
         tf.square(hotel["latitude"] - latitude) + tf.square(hotel["longitude"] - longitude)
     )

     # Takes latitude, longitude, rating, and distance columns as features
     X = hotel[['latitude', 'longitude', 'hotel_class', 'rating', 'distance']].values

     # Build the KNN model with the number of neighbors (k) = quantity
     knn = NearestNeighbors(n_neighbors=quantity)
     knn.fit(X)

     # Search for 5 nearest neighbors of given position
     distances, indices = knn.kneighbors([[latitude, longitude, 5, 5, 0]])

     # Displays recommended restaurants
     recommendations = []
     for index in indices[0]:
         recommendation = hotel.iloc[index].to_dict()
         recommendations. append(recommendation)
        
     # Checks if distance is a multiple of 20, then sorts by best rating
     if int(hotel.iloc[indices[0][0]]['distance']) % 20 == 0:
         recommendations = sorted(recommendations, key=lambda x: x['rating'], reverse=True)

     return {"hotel_recommendation": recommendations}