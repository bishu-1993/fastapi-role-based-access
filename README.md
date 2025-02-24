# User Authentication and Authorization Service

- User authentication and authorization module support customizable user roles with attachable permissions.

## For Docker Setup

- Create .env file in project root folder and set according to the environment.

    - POSTGRES_USER=postgres
    - POSTGRES_PASSWORD=admin123
    - POSTGRES_DB_HOST=db
    - POSTGRES_DB=userauthentication
    - SECRET_KEY=erpxcsd1234fed
    - DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_DB_HOST}/${POSTGRES_DB}
    - REDIS_URL=redis://redis:6379

_To Run Service using Docker_

    $ docker-compose up --build

    - Note: Above command will run Docker container on port 8000.

    _To Stop the Running Service Docker Container_

    $ docker-compose down

    _To go inside the running Docker Container_

    $ docker exec -it <container_id> bash

## For Local Development Setup

_System Requirements_

- Configure PEP8 in your editor/IDE
- Python 3.7+
- PostgreSQL 14+
- Redis

_Install Dependencies_

$ python3 -m venv env
$ source env/bin/activate
$ pip install --no-cache-dir -r requirements.txt

_To Run this Service Locally_

$ uvicorn app.main:app --reload

## Access the API Documentation

- Open the browser and go to http://localhost:8000/docs to access the Swagger UI interface provided by      FastAPI and test endpoints.

_Create Admin User_

- After the server is running, create the admin user by hitting the /create_admin API. Below are the credentials for the admin user:
    {
    "username": "admin",
    "email": "admin@example.com",
    "password": "admin",
    "roles": ["admin_role"]
    }
