from collections import defaultdict
from flask import jsonify, current_app
from bson import ObjectId, errors
from util.jsonify_tools import convert_objectid

def get_ratings(query_id=None):
    db = current_app.config['db']
    filtered_ratings = list(db.ratings.find({"_id": ObjectId(query_id)}) if query_id else db.ratings.find())
    filtered_ratings = [convert_objectid(rating) for rating in filtered_ratings]
    return jsonify(filtered_ratings), 200

def get_book_ratings(book_id):
    db = current_app.config['db']
    try:
        rating_entry = db.ratings.find_one({"_id": ObjectId(book_id)})
    except errors.InvalidId:
        return jsonify({"message": "Ratings not found for the given book ID"}), 404

    if rating_entry:
        return jsonify(convert_objectid(rating_entry)), 200
    else:
        return jsonify({"message": "Ratings not found for the given book ID"}), 404

def add_rating(book_id, value):
    db = current_app.config['db']
    try:
        rating_entry = db.ratings.find_one({"_id": ObjectId(book_id)})
    except errors.InvalidId:
        return jsonify({"error": "Book not found"}), 404

    if not rating_entry:
        return jsonify({"error": "Book not found"}), 404

    if value not in {1, 2, 3, 4, 5}:
        return jsonify({"error": "Invalid rating value. Must be an integer between 1 and 5"}), 422

    rating_entry["values"].append(value)
    rating_entry["average"] = sum(rating_entry["values"]) / len(rating_entry["values"]) if rating_entry["values"] else 0

    db.ratings.update_one({"_id": ObjectId(book_id)}, {"$set": rating_entry})
    return jsonify({"new_average_rating": rating_entry["average"]}), 201

def get_top_books():
    db = current_app.config['db']
    try:
        eligible_books = list(db.ratings.find({"values": {"$gte": 3}}))

        if not eligible_books:
            return jsonify([])

        rating_groups = defaultdict(list)
        for book in eligible_books:
            rating_groups[book["average"]].append(book)

        top_ratings = sorted(rating_groups.keys(), reverse=True)[:3]

        top_books = []
        for rating in top_ratings:
            top_books.extend(rating_groups[rating])

        sorted_books_dicts = [convert_objectid(book) for book in top_books]
        return jsonify(sorted_books_dicts), 200

    except Exception as e:
        return jsonify({"error": "Failed to retrieve top books"}), 500