from app.models.book import Book
import pytest

def test_from_dict_returns_book():
    # Arrange
    book_data = {
        "title": "New Book",
        "description": "The Best!"
    }

    # Act
    new_book = Book.from_dict(book_data)

    # Assert
    assert new_book.title == "New Book"
    assert new_book.description == "The Best!"

def test_from_dict_with_no_title():
    # Arrange
    book_data = {
        "description": "The Best!"
    }

    # Act & Assert
    with pytest.raises(KeyError, match = 'title'):
        new_book = Book.from_dict(book_data)

def test_from_dict_with_no_description():
    # Arrange
    book_data = {
        "title": "New Book"
    }

    # Act & Assert
    with pytest.raises(KeyError, match = 'description'):
        new_book = Book.from_dict(book_data)

def test_from_dict_with_extra_keys():
    # Arrange
    book_data = {
        "extra": "some stuff",
        "title": "New Book",
        "description": "The Best!",
        "another": "last value"
    }

    # Act
    new_book = Book.from_dict(book_data)

    # Assert
    assert new_book.title == "New Book"
    assert new_book.description == "The Best!"

    # When we have records, `get_all_books` returns a list containing a dictionary representing each `Book`
def test_get_all_books_with_two_records(client, two_saved_books):
    # Act
    response = client.get("/books")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0] == {
        "id": 1,
        "title": "Ocean Book",
        "description": "watr 4evr"
    }
    assert response_body[1] == {
        "id": 2,
        "title": "Mountain Book",
        "description": "i luv 2 climb rocks"
    }

# When we have records and a `title` query in the request arguments, `get_all_books` returns a list containing only the `Book`s that match the query
def test_get_all_books_with_title_query_matching_none(client, two_saved_books):
    # Act
    data = {'title': 'Desert Book'}
    response = client.get("/books", query_string = data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

# When we have records and a `title` query in the request arguments, `get_all_books` returns a list containing only the `Book`s that match the query
def test_get_all_books_with_title_query_matching_one(client, two_saved_books):
    # Act
    data = {'title': 'Ocean Book'}
    response = client.get("/books", query_string = data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0] == {
        "id": 1,
        "title": "Ocean Book",
        "description": "watr 4evr"
    }

# When we call `get_one_book` with a numeric ID that doesn't have a record, we get the expected error message
def test_get_one_book_missing_record(client, two_saved_books):
    # Act
    response = client.get("/books/3")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Book 3 not found"}

# When we call `get_one_book` with a non-numeric ID, we get the expected error message
def test_get_one_book_invalid_id(client, two_saved_books):
    # Act
    response = client.get("/books/cat")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "Book cat invalid"}


def test_to_dict_no_missing_data():
    # Arrange
    test_data = Book(id = 1,
                    title="Ocean Book",
                    description="watr 4evr")

    # Act
    result = test_data.to_dict()

    # Assert
    assert len(result) == 3
    assert result["id"] == 1
    assert result["title"] == "Ocean Book"
    assert result["description"] == "watr 4evr"

def test_to_dict_missing_id():
    # Arrange
    test_data = Book(title="Ocean Book",
                    description="watr 4evr")

    # Act
    result = test_data.to_dict()

    # Assert
    assert len(result) == 3
    assert result["id"] is None
    assert result["title"] == "Ocean Book"
    assert result["description"] == "watr 4evr"

def test_to_dict_missing_title():
    # Arrange
    test_data = Book(id=1,
                    description="watr 4evr")

    # Act
    result = test_data.to_dict()

    # Assert
    assert len(result) == 3
    assert result["id"] == 1
    assert result["title"] is None
    assert result["description"] == "watr 4evr"

def test_to_dict_missing_description():
    # Arrange
    test_data = Book(id = 1,
                    title="Ocean Book")

    # Act
    result = test_data.to_dict()

    # Assert
    assert len(result) == 3
    assert result["id"] == 1
    assert result["title"] == "Ocean Book"
    assert result["description"] is None