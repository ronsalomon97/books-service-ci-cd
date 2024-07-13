import requests

def test_post_books():
    url = "http://localhost:5001/books"
    books = [
        {"title": "Adventures of Huckleberry Finn", "ISBN": "9780520343641", "genre": "Fiction"},
        {"title": "The Best of Isaac Asimov", "ISBN": "9780385050784", "genre": "Science Fiction"},
        {"title": "Fear No Evil", "ISBN": "9780394558783", "genre": "Biography"}
    ]
    for book in books:
        response = requests.post(url, json=book)
        assert response.status_code == 201
        assert "ID" in response.json()

def test_get_book_by_id():
    url = "http://localhost:5001/books"
    response = requests.post(url, json={"title": "Adventures of Huckleberry Finn", "ISBN": "9780520343641", "genre": "Fiction"})
    book_id = response.json()["ID"]
    response = requests.get(f"{url}/{book_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Adventures of Huckleberry Finn"

def test_get_books():
    url = "http://localhost:5001/books"
    response = requests.get(url)
    assert response.status_code == 200
    assert len(response.json()) >= 1

def test_update_book():
    url = "http://localhost:5001/books"
    response = requests.post(url, json={"title": "Test Book", "ISBN": "1234567890", "genre": "Test"})
    book_id = response.json()["ID"]
    update_url = f"{url}/{book_id}"
    response = requests.put(update_url, json={"title": "Updated Test Book"})
    assert response.status_code == 200
    response = requests.get(update_url)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Test Book"

def test_delete_book():
    url = "http://localhost:5001/books"
    response = requests.post(url, json={"title": "Delete Test Book", "ISBN": "0987654321", "genre": "Test"})
    book_id = response.json()["ID"]
    delete_url = f"{url}/{book_id}"
    response = requests.delete(delete_url)
    assert response.status_code == 204
    response = requests.get(delete_url)
    assert response.status_code == 404
