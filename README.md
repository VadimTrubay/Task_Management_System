# Task_Management_System

Test project for DRF(django rest framework)

- This project is implemented using Django Rest Framework.

### Install

- Clone the project repository from
  GitHub: https://github.com/VadimTrubay/Task_Management_System.git
- create in root folder your own .env file like .env.example

#### create environment

    python -m venv venv

#### active environment

    .\venv\Scripts\activate

#### install requirements:

    pip install -r requirements.txt

#### run in terminal command:
    cd task_management
    python manage.py migrate

#### run server:

    python manage.py runserver


### Running the project using Docker
  To start the using Docker, run:

    docker-compose up --build  

### You can run tests using pytest:
  To start the using Docker, run:

    pytest

#### use application for url:

http://127.0.0.1:8000


### Swagger UI:

To access the Swagger UI, go to:

http://127.0.0.1:8000/api/schema/swagger-ui/

# WebSocket Connection for Task Status Notifications:

- Open Postman.
- Enter the following WebSocket URL: `ws://127.0.0.1:8000/ws/tasks/`
- In the Headers section, add the following header for authorization:
- Key: Authorization
- Value: Bearer <your_access_token>
- Once connected, you will start receiving notifications whenever the status of a task changes.


# Used technologies:

- Python
- DRF(django rest framework)
- GitHub
