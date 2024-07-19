import logging
from flask import Flask, jsonify
from pymongo import MongoClient
from routes.book_routes import book_routes
from routes.rating_routes import rating_routes

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

client = MongoClient('mongodb://mongo:27017/')
app.config['db'] = client['booksdb']

app.register_blueprint(book_routes)
app.register_blueprint(rating_routes)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify(status='ok'), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
