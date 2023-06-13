from flask import Flask
from place import get_recommendation_place_nn

app = Flask(__name__)

@app.route('/recommendations', methods=['POST'])
def recommendations(activity: str = "Outdoor", category: str = "Beach", latitude: float = -1.212555, longitude: float = 116.98106):
    return get_recommendation_place_nn(activity, category, latitude, longitude)

if __name__ == '__main__':
    app.run()
