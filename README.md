# Flask api Boilerplate

REST API developed with Python 3 (Flask) and Postgres.

## Structure

The project was developed following the *application factories* design pattern and some *twelve-factor app* practices, being:

* ```/app/__init . py```: responsible for initializing the application and its dependencies, such as *CORS*;

* ```/app/api/```: contains the business rules, including the models, decoupled, in case it is necessary to use the Flask templates; and endpoints, already versioned via blueprints + directories;

* ```/app/config/```: application settings, segregated by environment types (*development*, *production* and *testing*);

* ```/app/ext/```: third-party libraries/extensions used in the project, such as *sqlalchemy* and *flask-jwt-extended*;

* ```/app/tests/```: tests written with unittest;

* ```/migrations/```: Postgres migration files;

* ```/static/```: directory for storing images.

**Overview:**
```
.
├── app
│   ├── api
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── utils
│   │   │   └── __init__.py
│   │   └── v1
│   │       ├── __init__.py
│   │       ├── main.py
│   │       └── user
│   │           ├── __init__.py
│   │           ├── resources.py
│   │           └── serializer.py
│   ├── config
│   │   ├── config.py
│   │   └── __init__.py
│   ├── ext
│   │   ├── auth.py
│   │   ├── db.py
│   │   ├── __init__.py
│   │   ├── log.py
│   │   ├── migrate.py
│   │   └── serializer.py
│   ├── __init__.py
│   └── tests
│       └── __init__.py
├── LICENSE
├── Makefile
├── manager.py
├── migrations
│   ├── alembic.ini
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions
│       └── e3a93a4499c3_create_users_table.py
├── Procfile
├── README.md
├── requirements.txt
├── runtime.txt
├── static
└── wsgi.py
```

The application can be run in the following environments: *development*, *production* and *testing*, requiring Python 3 and other tools, such as pip and virtualenv, to be installed.

Each environment has its own database, install Postgres and create a database, with user/password, according to .env.example

## Settings

**Requirements:**

* Git - https://git-scm.com/downloads
* Python - https://www.python.org
* Docker - https://www.docker.com/

After installing the above requirements:

1. Clone this repository: `git clone https://github.com/arilsonsouza/flask-api.git`
2. Go to the directory: `cd flask-api/`
3. Build the new image and spin up the containers `docker-compose up -d --build`
4. Setup database `docker-compose exec web python manager.py db upgrade`
  
## Application

Default endpoint for *development*: `http://localhost:5000/api/v1...`, authentication via JWT token for some operations.
* Authorization Bearer
```
    Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MDIwMzIxMDcsIm5iZiI6MTYwMjAzMjEwNywianRpIjoiNTRlNDg4OTMtMGVhNS00NjdlLTg0YjctZDE1NGZhMzYxMTg1IiwiZXhwIjoxNjAyMTE4NTA3LCJpZGVudGl0eSI6MiwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.r2CYzZHlt1Kw4oi0gAAKO54M6o1g1s-coo_tY6IbpgA
```
### Users

* **[POST]** `/api/v1/users`

    Create user.

    Payload:

    ```JSON
    {
        "email": "admin@example.com",
        "username": "admin",
        "password": "admin",        
    }
    ```
    Response:

    ```JSON
    {       
        "success": true,
        "content": null,
        "message": "User admin was successfully registered"
    }
    ```
* **[GET]** `/api/v1/users`
    Lists all users.    
    Response:

    ```JSON
    {
        "success": true,
        "content": {
            "items": [
                {
                    "id": 1,
                    "created_at": "2020-10-06T16:05:10.916741-03:00",
                    "email": "admin@example.com",
                    "username": "admin"
                },               
            ],
            "_meta": {
                "page": 1,
                "per_page": 10,
                "total_pages": 1,
                "total_items": 1
            },
            "_links": {
                "self": "/api/v1/users?page=1&per_page=10",
                "next": null,
                "prev": null
            }
        }
    }
    ```

* **[POST]** `/api/v1/auth/login`
    
    User authentication.

    Payload:

    ```JSON
    {
        "email": "admin@example.com",
        "password": "admin"
    }
    ```

    Response:

    ```JSON
    {
        "success": true,
        "content": {
            "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MDIwMzIxMDcsIm5iZiI6MTYwMjAzMjEwNywianRpIjoiNTRlNDg4OTMtMGVhNS00NjdlLTg0YjctZDE1NGZhMzYxMTg1IiwiZXhwIjoxNjAyMTE4NTA3LCJpZGVudGl0eSI6MiwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.r2CYzZHlt1Kw4oi0gAAKO54M6o1g1s-coo_tY6IbpgA"
        },
        "message": "User logged successfully."
    }
    ```   

### Tests
1. Export the environment variable for testing: `export ENV APP = testing`
* Work in progress