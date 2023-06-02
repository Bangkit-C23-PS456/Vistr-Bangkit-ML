from flask import Flask,request,jsonify
from flask_cors import CORS
from flask_restful import Resource, Api

app = Flask(__name__)
CORS(app) 
api = Api(app)
        
        
@app.route('/')
def hello():
    return "Hello World"
        
        
incomes = [
    { 'description': 'salary', 'amount': 5000 }
]


@app.route('/incomes')
def get_incomes():
    return jsonify(incomes)

if __name__=='__main__':
    app.run(port = 5000, debug = True)