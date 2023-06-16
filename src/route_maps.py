import googlemaps
import requests
import json

# Replace 'YOUR_API_KEY' with your actual API key
api_key = 'AIzaSyAuEU_3xLOkirCxYw9Thz2Lq2C4AWHm7TE'

# Create a client instance
gmaps = googlemaps.Client(api_key)

def get_traffic_condition(latitude_origin, longitude_origin, latitude_destination, longitude_destination):
  # Request traffic information
  traffic_result = gmaps.directions((latitude_origin, longitude_origin), (latitude_destination, longitude_destination), mode="driving", departure_time="now", traffic_model="best_guess")

  if traffic_result == []:
    return {}
  # Extract the traffic information
  duration_without_traffic = traffic_result[0]['legs'][0]['duration']['value']
  duration_in_traffic = traffic_result[0]['legs'][0]['duration_in_traffic']['value']
  traffic_ratio = duration_in_traffic / duration_without_traffic
  if traffic_ratio <= 0.7:  # Current if the ratio of travel time to traffic <= 0.7
    traffic_status = "Lancar"
  elif traffic_ratio <= 1.3:  # Crowded if the ratio of travel time to traffic is between 0.7 and 1.3
    traffic_status = "Ramai"
  elif traffic_ratio <= 2.0:  # Solid if the ratio of travel time to traffic is between 1.3 and 2.0
    traffic_status = "Padat"
  else:  # Jam if the ratio of travel time to traffic > 2.0
    traffic_status = "Macet"

  return {
      "duration_without_traffic":duration_without_traffic,
      "duration_with_traffic":duration_in_traffic, 
      "traffic_ratio":traffic_ratio,
      "traffic_status":traffic_status
  }
  
def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def capitalize_first_letter(sentence):
    words = sentence.split()
    capitalized_words = [word.capitalize() for word in words]
    return ' '.join(capitalized_words)

def create_route_description(latitude_origin, longitude_origin, latitude_destination, longitude_destination):
  # Request traffic information
  traffic_result = gmaps.directions((latitude_origin, longitude_origin), (latitude_destination, longitude_destination), mode="driving", departure_time="now", traffic_model="best_guess")
  steps = traffic_result[0]['legs'][0]['steps']

  translator = Translator()
  
  description = ''
    
  for i, step in enumerate(steps):
    instruction = remove_html_tags(step['html_instructions'])
    distance = step['distance']['text']
    duration = step['duration']['text']
        
    if i == 0:
      description += f"Mulailah dengan {instruction.lower()} sejauh {distance} selama {duration}.\n"
    elif i == len(steps) - 1:
      description += f"Beloklah ke {instruction.lower()}.\nTujuan akhir akan berada di sebelah kiri."
    else:
      description += f"{capitalize_first_letter(instruction)}. Jarak yang ditempuh sejauh {distance} selama {duration}.\n"
  
  description = translator.translate(description, dest='id', src='en').text

  return description