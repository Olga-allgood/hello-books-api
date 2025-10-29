from flask import Blueprint, Response, abort, make_response, request  # additional imports
from app import db
from app.models.book import Book

book_bp = Blueprint("book_bp", __name__, url_prefix="/books")

@book_bp.post("")
def create_book():
    request_body = request.get_json()
    title = request_body["title"]
    description = request_body["description"]

    new_book = Book(title=title, description=description)
    db.session.add(new_book)
    db.session.commit()

    response = {
        "id": new_book.id,
        "title": new_book.title,
        "description": new_book.description,
    }

    return make_response(response, 201)
@book_bp.get("")
def get_all_books():
    query = db.select(Book).order_by(Book.id)
    # scalers are getting the model objects from the query 
    # and get them stored in books as a list of model objects
    books = db.session.scalars(query)
    books_response = []
    # data base has models with attributes, but for flask we need 
    # JSON files, so we create dictionaries from the model objects
    for book in books:
        books_response.append(
            {
            "id": book.id,
            "title": book.title,
            "description": book.description
        })
    return books_response

@book_bp.get("/<book_id>")
def get_single_book(book_id):
    book = validate_book(book_id)
    return {
        "id": book.id,
        "title": book.title,
        "description": book.description
    }
@book_bp.put("/<book_id>")
def update_book(book_id):
    book = validate_book(book_id)
    request_body = request.get_json()

    book.title = request_body["title"]
    book.description = request_body["description"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")
# with empty body- status 204 - specify json for the system!
def validate_book(book_id):
    try:
        book_id = int(book_id)
    except ValueError:
        invalid_input = {"message": f"Book id {book_id} invalid."}
        abort(make_response(invalid_input, 400))
    query = db.select(Book).where(Book.id == book_id)
    book = db.session.scalar(query)
    if not book: 
        not_found_input = {"message": f"book {book_id} not found"}
        abort(make_response(not_found_input, 404))  
    return book          
        
@book_bp.delete("/<book_id>")
def delete_book(book_id):
    book = validate_book(book_id) 
    db.session.delete(book)     
    db.session.commit()
    return Response(status=204, mimetype="application/json")

    

# # @book_bp.get("/<book_id>")
# # def get_one_book(book_id):
# #     try:
# #         book_id = int(book_id)
# #     except:
# #         return {"message": f"book {book_id} invalid"}, 400

# #     for book in books:
# #         if book.id == book_id:
# #             return {
# #                 "id": book.id,
# #                 "title": book.title,
# #                 "description": book.description,
# #             }

# #     return {"message": f"book {book_id} not found"}, 404

# def validate_book(book_id):
#     try:
#         book_id = int(book_id)
#     except:
#         response = {"message": f"book {book_id} invalid"}
#         abort(make_response(response, 400))

#     for book in books:
#         if book.id == book_id:
#             return book

#     response = {"message": f"book {book_id} not found"}
#     abort(make_response(response, 404))

# @book_bp.get("/<book_id>")
# def get_one_book(book_id):
#     book = validate_book(book_id)

#     return {
#         "id": book.id,
#         "title": book.title,
#         "description": book.description,
#     }