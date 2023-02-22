import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy  # , or_
from flask_cors import CORS
import random

BOOKS_PER_SHELF = 8

# @TODO: General Instructions
#   - As you're creating endpoints, define them and then search for 'TODO' within the frontend to update the endpoints there.
#     If you do not update the endpoints, the lab will not work - of no fault of your API code!
#   - Make sure for each route that you're thinking through when to abort and with which kind of error
#   - If you change any of the response body keys, make sure you update the frontend to correspond.


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    with app.app_context():
        from models import setup_db, Book

        setup_db(app)

        def paginate_books(request, selection):
            page = request.args.get("page", 1, type=int)
            start = (page - 1) * BOOKS_PER_SHELF
            end = start + BOOKS_PER_SHELF

            books = [book.format() for book in selection]
            current_books = books[start:end]

            return current_books

        @app.route("/books")
        def retrieve_books():
            selection = Book.query.order_by(Book.id).all()
            current_books = paginate_books(request, selection)

            if len(current_books) == 0:
                abort(404)

            return jsonify(
                {
                    "success": True,
                    "books": current_books,
                    "total_books": len(selection),
                }
            )

        @app.route("/books/<int:book_id>", methods=["PATCH"])
        def update_book_rating(book_id):
            body = request.get_json()

            try:
                book = Book.query.filter(Book.id == book_id).one_or_none()

                if book is None:
                    abort(404)

                if "rating" in body:
                    book.rating = int(body.get("rating"))

                book.update()

                return jsonify(
                    {
                        "success": True,
                        "id": book.id,
                    }
                )

            except:
                abort(422)

        @app.route("/books/<int:book_id>", methods=["DELETE"])
        def delete_book(book_id):
            try:
                book = Book.query.filter(Book.id == book_id).one_or_none()

                if book is None:
                    abort(404)

                book.delete()
                selection = Book.query.order_by(Book.id).all()
                current_books = paginate_books(request, selection)

                return jsonify(
                    {
                        "success": True,
                        "deleted": book_id,
                        "books": current_books,
                        "total_books": len(selection),
                    }
                )

            except:
                abort(422)

        @app.route("/books", methods=["POST"])
        def create_book():
            body = request.get_json()

            new_title = body.get("title", None)
            new_author = body.get("author", None)
            new_rating = body.get("rating", None)

            try:
                book = Book(
                    title=new_title, author=new_author, rating=new_rating
                )
                book.insert()

                selection = Book.query.order_by(Book.id).all()
                current_books = paginate_books(request, selection)

                return jsonify(
                    {
                        "success": True,
                        "created": book.id,
                        "books": current_books,
                        "total_books": len(selection),
                    }
                )

            except:
                abort(422)

    return app
