import re
import requests
from flask import jsonify, current_app
from bson import ObjectId, errors
from util.jsonify_tools import custom_jsonify, convert_objectid
from dotenv import load_dotenv

load_dotenv()

def add_book(data):
    db = current_app.config['db']
    expected_fields = {"ISBN", "title", "genre"}
    received_fields = set(data.keys())

    if received_fields != expected_fields:
        return (
            jsonify(
                {
                    "error": "ISBN, title, and genre fields (and only them) must be provided"
                }
            ),
            422,
        )

    isbn = data["ISBN"]
    title = data["title"]
    genre = data["genre"]

    valid_genres = [
        "Fiction",
        "Children",
        "Biography",
        "Science",
        "Science Fiction",
        "Fantasy",
        "Other",
    ]
    if genre not in valid_genres:
        return (
            jsonify(
                {
                    "error": "Invalid genre; acceptable genres are Fiction, Children, Biography, Science, Science Fiction, Fantasy, Other"
                }
            ),
            422,
        )

    existing_book = db.books.find_one({"ISBN": isbn})
    if existing_book:
        return jsonify({"error": "A book with this ISBN already exists"}), 422

    # fetch data from Google Books API
    google_books_url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
    try:
        response = requests.get(google_books_url)
        response.raise_for_status()
        google_books_data = response.json()["items"][0]["volumeInfo"]
    except requests.exceptions.HTTPError:
        return jsonify({"error": f"Unable to connect to Google Books API"}), 500
    except (IndexError, KeyError):
        return (
            jsonify({"error": "Invalid ISBN number; not found in Google Books API"}),
            422,
        )

    authors_list = google_books_data.get("authors", ["missing"])
    authors = " and ".join(authors_list)

    publisher = google_books_data.get("publisher", "missing")

    published_date = google_books_data.get("publishedDate", "missing")
    if published_date != "missing":
        valid_date_formats = [
            r"^\d{4}$",  # YYYY
            r"^\d{4}-\d{2}-\d{2}$",  # YYYY-MM-DD
        ]

    if not any(re.match(pattern, published_date) for pattern in valid_date_formats):
        published_date = "missing"

    book = {
        "ISBN": isbn,
        "title": title,
        "genre": genre,
        "authors": authors,
        "publisher": publisher,
        "publishedDate": published_date
    }
    book_id = db.books.insert_one(book).inserted_id

    rating = {"_id": book_id, "title": title, "values": [], "average": 0}
    db.ratings.insert_one(rating)

    return jsonify({"message": f"Book created successfully with ID {book_id}"}), 201

def get_book(book_id):
    db = current_app.config['db']
    try:
        book = db.books.find_one({"_id": ObjectId(book_id)})
    except errors.InvalidId:
        return custom_jsonify({"message": "Book not found"}), 404

    if book:
        book['id'] = str(book.pop('_id'))
        return custom_jsonify(convert_objectid(book)), 200
    else:
        return custom_jsonify({"message": "Book not found"}), 404


def get_books(query_params):
    db = current_app.config['db']

    query_params = {k: v.strip('"') for k, v in query_params.items()}

    mongo_query = {}
    for key, value in query_params.items():
        if key == "id":
            try:
                mongo_query["_id"] = ObjectId(value)
            except errors.InvalidId:
                return jsonify({"error": "Invalid ID format"}), 422
        elif key in ["genre", "authors", "publisher", "title", "ISBN", "publishedDate"]:
            mongo_query[key] = value

    filtered_books = list(db.books.find(mongo_query))
    filtered_books = [mongo_document_to_dict(book) for book in filtered_books]

    return jsonify(filtered_books), 200

def mongo_document_to_dict(document):
    if document:
        document = dict(document)
        document['id'] = str(document.pop('_id'))
    return document


def update_book(book_id, updated_data):
    db = current_app.config['db']
    book = db.books.find_one({"_id": ObjectId(book_id)})

    if not book:
        return jsonify({"error": "Book not found"}), 404

    required_fields = [
        "ISBN",
        "title",
        "genre",
        "authors",
        "publisher",
        "publishedDate",
    ]
    if not all(field in updated_data for field in required_fields):
        return jsonify({"error": "All fields must be provided"}), 422

    valid_genres = [
        "Fiction",
        "Children",
        "Biography",
        "Science",
        "Science Fiction",
        "Fantasy",
        "Other",
    ]
    if updated_data["genre"] not in valid_genres:
        return (
            jsonify(
                {
                    "error": "Invalid genre; acceptable genres are Fiction, Children, Biography, Science, Science Fiction, Fantasy, Other"
                }
            ),
            422,
        )

    published_date = updated_data.get("publishedDate", "missing")

    if published_date != "missing":
        valid_date_formats = [
            r"^\d{4}$",  # YYYY
            r"^\d{4}-\d{2}-\d{2}$",  # YYYY-MM-DD
        ]

        if not any(re.match(pattern, published_date) for pattern in valid_date_formats):
            published_date = "missing"

    updated_data["publishedDate"] = published_date

    if db.books.find_one({"ISBN": updated_data["ISBN"], "_id": {"$ne": ObjectId(book_id)}}):
        return jsonify({"error": "A book with this ISBN already exists"}), 422

    db.books.update_one({"_id": ObjectId(book_id)}, {"$set": updated_data})
    return jsonify({"message": f"Book with ID {book_id} updated successfully"}), 200

def delete_book(book_id):
    db = current_app.config['db']
    try:
        book = db.books.find_one({"_id": ObjectId(book_id)})
    except errors.InvalidId:
        return custom_jsonify({"message": "Book not found"}), 404

    if not book:
        return custom_jsonify({"message": "Book not found"}), 404

    db.books.delete_one({"_id": ObjectId(book_id)})
    db.ratings.delete_one({"_id": ObjectId(book_id)})

    return custom_jsonify({"id": str(book_id)}), 200
