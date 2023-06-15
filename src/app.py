from flask import Flask
from place import recommend_places
from hotel import recommend_hotels
from restaurant import recommend_restaurants
from itinerary import itinerary_left, itinerary_with_traffic

app = Flask(__name__)

@app.route('/place_recommendation', methods=['POST'])
def recommend_places(activity: str = "Outdoor", category: str = "Beach", latitude: float = -1.212555, longitude: float = 116.98106):
    return recommend_places(activity, category, latitude, longitude, 3)

@app.route('/hotel_recommendation', methods=['POST'])
def recommend_hotels(activity: str = "Outdoor", category: str = "Beach", latitude: float = -1.212555, longitude: float = 116.98106):
    return recommend_hotels(latitude, longitude)

@app.route('/restaurant_recommendation', methods=['POST'])
def recommend_restaurants(activity: str = "Outdoor", category: str = "Beach", latitude: float = -1.212555, longitude: float = 116.98106):
    return recommend_restaurants(latitude, longitude)

@app.route('/itinerary_recommendation', methods=['POST'])
def itinerary(activity: str = "Outdoor", category: str = "Beach", latitude: float = -1.212555, longitude: float = 116.98106):
    return itinerary_left(activity, category, latitude, longitude)

app.route('/itinerary_recommendation_with_traffic', methods=['POST'])
def itinerary_with_traffic(activity: str = "Outdoor", category: str = "Beach", latitude: float = -1.212555, longitude: float = 116.98106):
    return itinerary_with_traffic(activity, category, latitude, longitude)

if __name__ == '__main__':
    app.run()
