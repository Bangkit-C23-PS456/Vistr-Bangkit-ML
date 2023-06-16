from place import recommend_places, recommend_places_with_traffic
from hotel import recommend_hotels
from restaurant import recommend_restaurants

def itinerary_left(activity, category, latitude, longitude):
  todo_recommendation = recommend_places(activity, category, latitude, longitude, 1)

  if len(todo_recommendation) > 0:
      todo_latitude = todo_recommendation['place_recommendation'][0]['latitude']
      todo_longitude = todo_recommendation['place_recommendation'][0]['longitude']

      hotel_recommendation = recommend_hotels(todo_latitude, todo_longitude, 3)
      restaurant_recommendation = recommend_restaurants(todo_latitude, todo_longitude, 3)

      return {
          'todo_recommendation': todo_recommendation,
          'hotel_recommendation': hotel_recommendation,
          'restaurant_recommendation': restaurant_recommendation
      }
      
  else:
      return {
          'todo_recommendation':[],
          'hotel_recommendation':[],
          'restaurant_recommendation':[]
      }

def itinerary_with_traffic(activity, category, latitude, longitude):
  todo_recommendation = recommend_places_with_traffic(activity, category, latitude, longitude, 1)

  if len(todo_recommendation) > 0:
      todo_latitude = todo_recommendation['place_recommendation'][0]['latitude']
      todo_longitude = todo_recommendation['place_recommendation'][0]['longitude']

      hotel_recommendation = recommend_hotels(todo_latitude, todo_longitude, 3)
      restaurant_recommendation = recommend_restaurants(todo_latitude, todo_longitude, 3)

      return {
          'todo_recommendation': todo_recommendation,
          'hotel_recommendation': hotel_recommendation,
          'restaurant_recommendation': restaurant_recommendation
      }

  else:
      return {
          'todo_recommendation':[],
          'hotel_recommendation':[],
          'restaurant_recommendation':[]
      }

