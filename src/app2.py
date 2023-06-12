from flask import Flask, request
import tensorflow as tf
import pandas as pd
import psycopg2

app = Flask(__name__)

# Connect to the database
connection = psycopg2.connect(
    host="your_host",
    database="your_database",
    user="your_username",
    password="your_password"
)

# Define a function to fetch data from the database and return it as a DataFrame
def fetch_places_from_db():
    query = "SELECT * FROM places"
    places_df = pd.read_sql_query(query, connection)
    return places_df

@app.route('/recommendations', methods=['POST'])
def get_recommendations():
    # Get the user's preferences from the request
    user_activity = request.json['activity']
    user_category = request.json['category']
    user_latitude = request.json['latitude']
    user_longitude = request.json['longitude']

    # Define the user's preferences
    user_activity = tf.constant(user_activity, dtype=tf.string)
    user_category = tf.constant(user_category, dtype=tf.string)
    user_latitude = tf.constant(user_latitude, dtype=tf.float32)
    user_longitude = tf.constant(user_longitude, dtype=tf.float32)

    # Fetch the places data from the database
    places_df = fetch_places_from_db()

    # Calculate the distance between the user's location and the places' locations
    places_df["distance"] = tf.sqrt(
        tf.square(places_df["latitude"] - user_latitude) + tf.square(places_df["longitude"] - user_longitude)
    )

    # Filter the places based on the user's preferences
    filtered_places = places_df[
        (places_df["activity"] == user_activity) & (places_df["category"] == user_category)
    ]

    # Sort the filtered places by distance
    sorted_places = filtered_places.sort_values(by="distance")

    # Find the indices of the top k recommendations
    k = 3
    top_indices = tf.argsort(sorted_places["distance"])[:k]

    # Gather the top k recommendations from the sorted places dataframe
    top_recommendations = sorted_places.iloc[top_indices]

    # Create a response dictionary with the recommendations
    recommendations = []
    for _, row in top_recommendations.iterrows():
        recommendation = {
            "place_name": row["place_name"],
            "city": row["city"],
            "rating": row["rating"],
            # Add other relevant fields as needed
        }
        recommendations.append(recommendation)

    return {"recommendations": recommendations}

if __name__ == '__main__':
    app.run()
