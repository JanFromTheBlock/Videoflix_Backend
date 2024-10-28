# Django backend for "Videoflix"

## Project Description

This project was developed as part of my studies at the Developer Akademie. It functions as the backend for a video platform application, with the corresponding frontend available here [here](https://github.com/JanFromTheBlock/Videoflix_Frontend).

## Installation and Setup

1. Clone the Repository:
    ```bash
    Git clone https://github.com/JanFromTheBlock/Videoflix_Backend.git
    cd Videoflix_Backend
    ```
2. Create a virtual environment and install the dependencies:
    ```bash
    python -m venv env
    source env/bin/activate
    pip install -r requirements.txt
    ```
3. Install postgresql with own username and password in WSL:

    ```bash
    #If you prefer sqLite update settings.py and skip step 3.
    python -m venv env_lin
    source env_lin/bin/activate
    sudo apt install postgresql postgresql-contrib
    sudo service postgresql start
    su postgres
    psql
    Create Database videoflix;
    CREATE USER chose a Username WITH PASSWORD ‘choose password’;
    ALTER ROLE your Username SET client_encoding TO ‘utf8’; 
    ALTER ROLE your Username SET default_transaction TO ‘read comitted’;
    ALTER ROLE your Username SET timezone TO ‘UTC’;
    GRANT ALL PRIVILIGES ON DATABASE ‘videoflix’ TO your Username;
    \q
    exit
    ```
4. For security reasons create .env file on base of the .env.template
5. Apply migrations:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
6. Create a Superuser with own username and password
    ```bash
    python manage.py createsuperuser
    ```
7. Start the Django development server:
    ```bash
    python manage.py runserver
    ```
8. Bonus: To convert videos after uploading the RQ Worker needs to be started:
    ```bash
    sudo service redis-server start
    python manage.py rqworker default

    ```