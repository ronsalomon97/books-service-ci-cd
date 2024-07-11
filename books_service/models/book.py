class Book:
    def __init__(self, id, ISBN, title, genre, authors, publisher, publishedDate):
        self.id = id
        self.ISBN = ISBN
        self.title = title
        self.genre = genre
        self.authors = authors
        self.publisher = publisher
        self.publishedDate = publishedDate

    def to_dict(self):
        return {
            "id": self.id,
            "ISBN": self.ISBN,
            "title": self.title,
            "genre": self.genre,
            "authors": self.authors,
            "publisher": self.publisher,
            "publishedDate": self.publishedDate,
        }