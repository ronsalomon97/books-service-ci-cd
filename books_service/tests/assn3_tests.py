import requests

def test_post_books():
    url = "http://localhost:5001/books"
    books = [
        {"title": "Adventures of Huckleberry Finn", "authors": "Mark Twain", "ISBN": "9780520343641", "genre": "Fiction"},
        {"title": "The Best of Isaac Asimov", "authors": "Isaac Asimov", "ISBN": "9780385050784", "genre": "Science Fiction"},
        {"title": "Fear No Evil", "authors": "Natan Sharansky", "ISBN": "9780394558783", "genre": "Biography"}
    ]
    ids = set()
    for book in books:
        response = requests.post(url, json=book)
        assert response.status_code == 201
        book_id = response.json().get("ID")
        assert book_id not in ids
        ids.add(book_id)

def test_get_book_by_id():
    url = "http://localhost:5001/books"
    response = requests.post(url, json={"title": "Adventures of Huckleberry Finn", "authors": "Mark Twain", "ISBN": "9780520343641", "genre": "Fiction"})
    book_id = response.json()["ID"]
    response = requests.get(f"{url}/{book_id}")
    assert response.status_code == 200
    assert response.json()["authors"] == "Mark Twain"

def test_get_books():
    url = "http://localhost:5001/books"
    response = requests.get(url)
    assert response.status_code == 200
    assert len(response.json()) == 3

def test_post_invalid_isbn():
    url = "http://localhost:5001/books"
    book4 = {"title": "Invalid ISBN Book", "authors": "Unknown", "ISBN": "123", "genre": "Fiction"}
    response = requests.post(url, json=book4)
    assert response.status_code == 500

def test_delete_book():
    url = "http://localhost:5001/books"
    response = requests.post(url, json={"title": "The Best of Isaac Asimov", "authors": "Isaac Asimov", "ISBN": "9780385050784", "genre": "Science Fiction"})
    book_id = response.json()["ID"]
    response = requests.delete(f"{url}/{book_id}")
    assert response.status_code == 200

def test_get_deleted_book():
    url = "http://localhost:5001/books"
    response = requests.post(url, json={"title": "The Best of Isaac Asimov", "authors": "Isaac Asimov", "ISBN": "9780385050784", "genre": "Science Fiction"})
    book_id = response.json()["ID"]
    requests.delete(f"{url}/{book_id}")
    response = requests.get(f"{url}/{book_id}")
    assert response.status_code == 404

def test_post_invalid_genre():
    url = "http://localhost:5001/books"
    book5 = {"title": "Book with Invalid Genre", "authors": "Unknown", "ISBN": "9781234567890", "genre": "Unknown Genre"}
    response = requests.post(url, json=book5)
    assert response.status_code == 422
