from flask import Flask
from place import get_recommendation_place_nn

app = Flask(__name__)

@app.route('/recommendations', methods=['POST'])
def recommendations():
    return get_recommendation_place_nn()

if __name__ == '__main__':
    app.run()
