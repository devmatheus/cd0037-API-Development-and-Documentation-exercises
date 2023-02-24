# API Documentation Practice
In this exercise, your task is to practice writing documentation for the bookstore app we created earlier.

You'll soon be writing documentation for your final project (the Trivia API), after which you'll get feedback from a reviewer. You can think of this as some rudimentary practice to prepare for that.

At each step, you can compare what you've written with our own version. Of course, **there isn't a single correct way to write a piece of documentation**, so your version may look quite different. However, there are principles and practices you should follow in order to produce quality documentation, and we'll point this out so you can check whether you've incorporated them in what you wrote.

## Getting started
- Base URL: http://127.0.0.1:5000
- Authentication: This version of the application does not require authentication or API keys.

## Error Handling
- Response codes: 400, 404, 422;
- Messages:
  - 400: `bad request`;
  - 404: `resource not found`;
  - 422: `unprocessable`;
- Error types:
  - 400 `bad request`: The request was not formatted correctly;
  - 404: `resource not found`: The requested resource could not be found;
  - 422: `unprocessable`: The request was formatted correctly but the server could not process the instructions;
- Example:
```json
{
  "error": 404,
  "message": "resource not found",
  "success": false
}
```

## Endpoint Library
### GET /books
- General:
  - Returns a list of book objects, success value, and total number of books;
  - Results are paginated in groups of 8. Include a request argument to choose page number, starting from 1;
- Query parameters:
  - page: integer (optional);
- Example:
  - Request: `curl http://127.0.0.1:5000/books?page=2`;
  - Response [status code 200]:
  ```json
  {
      "success": True,
      "books": [
        {
            "id": 1,
            "title": "Harry Potter and the Sorcerer's Stone",
            "author": "J.K. Rowling",
            "rating": 5
        }
      ],
      "total_books": 1,
  }
  ```

### POST /books
- General:
  - Search for books by title or creates a new book using the submitted title, author and rating;
- Searching:
  - Returns a list of books matching the search term, success value, total books;
  - Results are paginated in groups of 8. Include a request argument to choose page number, starting from 1;
  - For searching you can use the `search` argument in the request body otherwise you can use the `title`, `author` and `rating` arguments to create a new book;
  - Query parameters:
    - page: integer (optional);
  - Request body:
    - search: string (optional);
  - Example:
    - Request: `curl http://127.0.0.1:5000/books?page=2 -X POST -H "Content-Type: application/json" -d '{"search": "Harry"}'`;
    - Response [status code 200]:
    ```json
    {
        "success": True,
        "books": [
            {
                "id": 1,
                "title": "Harry Potter and the Sorcerer's Stone",
                "author": "J.K. Rowling",
                "rating": 5
            }
        ],
        "total_books": 1,
    }
    ```
- Creating:
  - Returns the id of the created book, success value, total books, and book list based on current page number to update the frontend;
  - Request body:
    - title: string (required);
    - author: string (required);
    - rating: integer (required);
  - Example:
    - Request: `curl http://127.0.0.1:5000/books -X POST -H "Content-Type: application/json" -d '{"title": "Harry Potter and the Sorcerer's Stone", "author": "J.K. Rowling", "rating": 5}'`;
    - Response [status code 200]:
    ```json
    {
        "success": True,
        "id": 1,
        "total_books": 1,
        "books": [
            {
                "id": 1,
                "title": "Harry Potter and the Sorcerer's Stone",
                "author": "J.K. Rowling",
                "rating": 5
            }
        ]
    }
    ```

### PATCH /books/{book_id}
- General:
  - Update the rating of a book;
- Route parameters:
  - book_id: integer (required);
- Request body:
  - rating: integer (required);
- Example:
  - Request: `curl http://127.0.0.1:5000/books/1 -X PATCH -H "Content-Type: application/json" -d '{"rating": 5}'`;
  - Response [status code 200]:
```json
{
  "success": True,
  "id": 1
}
```

### DELETE /books/{book_id}
- General:
  - Deletes the book of the given ID if it exists and returns the id of the deleted book, success value, total books, and book list based on current page number to update the frontend;
- Route parameters:
  - book_id: integer (required);
- Example:
  - Request: `curl http://127.0.0.1:5000/books/1 -X DELETE`;
  - Response [status code 200]:
```json
{
  "success": True,
  "delete": 1,
  "total_books": 0,
  "books": []
}
```
