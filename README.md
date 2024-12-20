# Open Library

OpenLibrary is a Django-based book lending service API. This project allows users to manage books, requests, and authentication using SQL as the database.

## Features

- User authentication and registration
- Book management: add, update, and delete books
- Request system for lending books
- REST API built with Django Rest Framework (DRF)
- Swagger for API documentation
- Dockerized environment for easy deployment

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/username/OpenLibrary.git
   cd OpenLibrary

2. Create an .env file in the root directory and configure environment variables:
   ```bash
   SECRET_KEY=your_django_secret_key
   
   DEBUG=True

   POSTGRES_DB=openlibrary
   POSTGRES_USER=openlibrary_user
   POSTGRES_PASSWORD=openlibrary_password
   POSTGRES_HOST=db
   POSTGRES_PORT=5432

Change SECRET_KEY with your secret key.

 3. Build and start the Docker containers:
    
    ```bash
    docker-compose up --build

4. Apply migrations:
- On macOS, use:
   ```bash
   docker-compose exec web python3 manage.py migrate
- On other systems, use:

    ```bash
     docker-compose exec web python manage.py migrate

5. Create a superuser:
- On macOS, use:
   ```bash
   docker-compose exec web python3 manage.py createsuperuser
- On other systems, use:

    ```bash
     docker-compose exec web python manage.py createsuperuser

6. Access the development server at:
   ```bash
   http://localhost:8000/

## API Documentation

The API documentation is available at the following endpoint:

- Swagger: http://localhost:8000/swagger/



## Usage
1. Start the server:
   ```bash
   docker-compose up
2. Access the API endpoints:
- View books: GET /api/books/
- Create a book: POST /api/books/
- Request a book: POST /api/book-requests/

3. Admin Panel:
    ```bash
    http://localhost:8000/admin/
## Testing

Run tests inside the Docker container:
- On macOS, use:
   ```bash
   docker-compose exec web python3 manage.py test
- On other systems, use:

    ```bash
     docker-compose exec web python manage.py test
