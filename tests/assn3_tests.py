import requests

def delete_book_by_isbn(isbn):
    url = "http://localhost:5001/books"
    response = requests.get(url, params={"ISBN": isbn})
    books = response.json()
    print(f"Books found with ISBN {isbn}: {books}")
    for book in books:
        if book["ISBN"] == isbn:
            print(f"Book details: {book}")
            book_id = book.get("ID") or book.get("id")
            if book_id:
                requests.delete(f"{url}/{book_id}")

def test_post_books():
    books = [
        {"title": "Adventures of Huckleberry Finn", "authors": "Mark Twain", "ISBN": "9780520343641", "genre": "Fiction"},
        {"title": "The Best of Isaac Asimov", "authors": "Isaac Asimov", "ISBN": "9780385050784", "genre": "Science Fiction"},
        {"title": "Fear No Evil", "authors": "Natan Sharansky", "ISBN": "9780394558783", "genre": "Biography"}
    ]
    for book in books:
        delete_book_by_isbn(book["ISBN"])

    url = "http://localhost:5001/books"
    ids = set()
    for book in books:
        response = requests.post(url, json=book)
        assert response.status_code == 201
        book_id = response.json().get("ID")
        assert book_id not in ids
        ids.add(book_id)

def test_get_book_by_id():
    delete_book_by_isbn("9780520343641")

    url = "http://localhost:5001/books"
    response = requests.post(url, json={"title": "Adventures of Huckleberry Finn", "authors": "Mark Twain", "ISBN": "9780520343641", "genre": "Fiction"})
    print(f"Response JSON: {response.json()}")
    book_id = response.json().get("ID") or response.json().get("id")
    response = requests.get(f"{url}/{book_id}")
    assert response.status_code == 200
    assert response.json()["authors"] == "Mark Twain"

def test_get_books():
    delete_book_by_isbn("9780520343641")
    delete_book_by_isbn("9780385050784")
    delete_book_by_isbn("9780394558783")

    url = "http://localhost:5001/books"
    response = requests.post(url, json={"title": "Adventures of Huckleberry Finn", "authors": "Mark Twain", "ISBN": "9780520343641", "genre": "Fiction"})
    response = requests.post(url, json={"title": "The Best of Isaac Asimov", "authors": "Isaac Asimov", "ISBN": "9780385050784", "genre": "Science Fiction"})
    response = requests.post(url, json={"title": "Fear No Evil", "authors": "Natan Sharansky", "ISBN": "9780394558783", "genre": "Biography"})
    response = requests.get(url)
    assert response.status_code == 404
    assert len(response.json()) == 3

def test_post_invalid_isbn():
    url = "http://localhost:5001/books"
    book4 = {"title": "Invalid ISBN Book", "authors": "Unknown", "ISBN": "123", "genre": "Fiction"}
    response = requests.post(url, json=book4)
    assert response.status_code == 500

def test_delete_book():
    delete_book_by_isbn("9780385050784")

    url = "http://localhost:5001/books"
    response = requests.post(url, json={"title": "The Best of Isaac Asimov", "authors": "Isaac Asimov", "ISBN": "9780385050784", "genre": "Science Fiction"})
    print(f"Response JSON: {response.json()}")
    book_id = response.json().get("ID") or response.json().get("id")
    response = requests.delete(f"{url}/{book_id}")
    assert response.status_code == 200

def test_get_deleted_book():
    delete_book_by_isbn("9780385050784")

    url = "http://localhost:5001/books"
    response = requests.post(url, json={"title": "The Best of Isaac Asimov", "authors": "Isaac Asimov", "ISBN": "9780385050784", "genre": "Science Fiction"})
    print(f"Response JSON: {response.json()}")
    book_id = response.json().get("ID") or response.json().get("id")
    requests.delete(f"{url}/{book_id}")
    response = requests.get(f"{url}/{book_id}")
    assert response.status_code == 404

def test_post_invalid_genre():
    url = "http://localhost:5001/books"
    book5 = {"title": "Book with Invalid Genre", "authors": "Unknown", "ISBN": "9781234567890", "genre": "Unknown Genre"}
    response = requests.post(url, json=book5)
    assert response.status_code == 422
