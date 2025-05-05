from flask import Blueprint, request, jsonify
from app.models import Book
from app.extensions import db
from http import HTTPStatus

main_bp = Blueprint('main', __name__)

@main_bp.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    
    if not data or 'title' not in data or 'author' not in data:
        return jsonify({"message": "Missing required fields"}), HTTPStatus.BAD_REQUEST
    
    try:
        new_book = Book(
            title=data['title'],
            author=data['author'],
            published_year=data.get('published_year')
        )
        db.session.add(new_book)
        db.session.commit()
        
        return jsonify({
            "data": new_book.to_dict(),
            "message": "Book created successfully",
            "status": HTTPStatus.CREATED
        }), HTTPStatus.CREATED
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@main_bp.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({"message": "Book not found"}), HTTPStatus.NOT_FOUND
    
    data = request.get_json()
    try:
        book.title = data.get('title', book.title)
        book.author = data.get('author', book.author)
        book.published_year = data.get('published_year', book.published_year)
        
        db.session.commit()
        return jsonify({
            "data": book.to_dict(),
            "message": "Book updated successfully",
            "status": HTTPStatus.OK
        }), HTTPStatus.OK
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@main_bp.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({"message": "Book not found"}), HTTPStatus.NOT_FOUND
    
    return jsonify({
        "data": book.to_dict(),
        "message": "Book retrieved successfully",
        "status": HTTPStatus.OK
    }), HTTPStatus.OK

@main_bp.route('/books', methods=['GET'])
def get_books():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    books = Book.query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        "data": [book.to_dict() for book in books.items],
        "total": books.total,
        "page": books.page,
        "per_page": books.per_page,
        "message": "Books retrieved successfully",
        "status": HTTPStatus.OK
    }), HTTPStatus.OK

@main_bp.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({"message": "Book not found"}), HTTPStatus.NOT_FOUND
    
    try:
        db.session.delete(book)
        db.session.commit()
        return jsonify({
            "message": "Book deleted successfully",
            "status": HTTPStatus.OK
        }), HTTPStatus.OK
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR