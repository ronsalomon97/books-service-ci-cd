from pymongo import MongoClient
import os
from bson.objectid import ObjectId
from dotenv import load_dotenv

load_dotenv()

class Database:
    _instance = None

    def _new_(cls, *args, **kwargs):
        if not cls._instance:
            cls.instance = super(Database, cls).new_(cls, *args, **kwargs)
            mongo_uri = os.getenv("MONGO_URI", "mongodb://mongo_books:27017/booksdb")
            cls._instance.client = MongoClient(mongo_uri)
            cls._instance.db = cls._instance.client["booksdb"]
            cls._instance.books = cls._instance.db["books"]
            cls._instance.ratings = cls._instance.db["ratings"]
        return cls._instance

    def insert_book(self, book):
        result = self.books.insert_one(book)
        return str(result.inserted_id)

    def find_book(self, book_id):
        return self.books.find_one({"_id": ObjectId(book_id)})

    def update_book(self, book_id, updates):
        self.books.update_one({"_id": ObjectId(book_id)}, {"$set": updates})

    def delete_book(self, book_id):
        self.books.delete_one({"_id": ObjectId(book_id)})

    def insert_rating(self, rating):
        result = self.ratings.insert_one(rating)
        return str(result.inserted_id)

    def find_rating(self, rating_id):
        return self.ratings.find_one({"_id": ObjectId(rating_id)})

    def update_rating(self, rating_id, updates):
        self.ratings.update_one({"_id": ObjectId(rating_id)}, {"$set": updates})

    def delete_rating(self, rating_id):
        self.ratings.delete_one({"_id": ObjectId(rating_id)})