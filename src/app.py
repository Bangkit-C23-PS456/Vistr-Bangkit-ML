from flask import Flask
from place import recommend_places, recommend_places_with_traffic
from hotel import recommend_hotels
from restaurant import recommend_restaurants
from itinerary import itinerary_left, itinerary_with_traffic
from route_maps import create_route_description, get_traffic_condition

app = Flask(__name__)

@app.route('/place_recommendation', methods=['POST'])
def recommend_places(activity: str = "Outdoor", category: str = "Beach", latitude: float = -1.212555, longitude: float = 116.98106):
    return recommend_places(activity, category, latitude, longitude, 3)

@app.route('/place_recommendation_with_traffic', methods=['POST'])
def recommend_places(activity: str = "Outdoor", category: str = "Beach", latitude: float = -1.212555, longitude: float = 116.98106):
    return recommend_places_with_traffic(activity, category, latitude, longitude, 3)

@app.route('/hotel_recommendation', methods=['POST'])
def recommend_hotels(latitude: float = -1.212555, longitude: float = 116.98106, quantity: int = 3):
    return recommend_hotels(latitude, longitude, quantity)

@app.route('/restaurant_recommendation', methods=['POST'])
def recommend_restaurants(latitude: float = -1.212555, longitude: float = 116.98106, quantity: int = 3):
    return recommend_restaurants(latitude, longitude, quantity)

@app.route('/itinerary_recommendation', methods=['POST'])
def itinerary(activity: str = "Outdoor", category: str = "Beach", latitude: float = -1.212555, longitude: float = 116.98106):
    return itinerary_left(activity, category, latitude, longitude)

@app.route('/itinerary_recommendation_with_traffic', methods=['POST'])
def itinerary_with_traffic(activity: str = "Outdoor", category: str = "Beach", latitude: float = -1.212555, longitude: float = 116.98106):
    return itinerary_with_traffic(activity, category, latitude, longitude)

@app.route('/traffic_condition', methods=['POST'])
def traffic_condition(latitude_origin: float = -1.212555, longitude_origin: float = 116.98106, latitude_destination: float = -1.212555, longitude_destination: float = 116.98106):
    return get_traffic_condition(latitude_origin, longitude_origin, latitude_destination, longitude_destination)

@app.route('/route_map', methods=['POST'])
def route_map(latitude_origin: float = -1.212555, longitude_origin: float = 116.98106, latitude_destination: float = -1.212555, longitude_destination: float = 116.98106):
    return create_route_description(latitude_origin, longitude_origin, latitude_destination, longitude_destination)


if __name__ == '__main__':
    app.run()
