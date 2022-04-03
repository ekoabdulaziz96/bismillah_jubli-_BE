# CORE-NOTIF 

application for manage Notification

## Prerequisites

[![Code](https://img.shields.io/badge/Code-Python-1B9D73?style=flat&logo=python)](https://python.org)
[![Framework](https://img.shields.io/badge/Framework-Flask-1B9D73?style=flat&logo=flask)](https://flask.palletsprojects.com/)


## How to run
Make sure you already installed **python3.8** or higher in your machine

1. Create your virtualenv and activate (if you are using virtuanenv)
2. Install library 
    ```sh
    pip install -r requirements.txt
    ```
3. Move your root path to this project
    ```sh
    cd core-notif
    ```
4. make .env file, you can duplicate it from .env.dev and rename it to .env
    - you can edit the value for your own environment IP/port or something else
    - recommend to use some environment with developer, we use docker that inclue `PostgreSQL, Adminer, Redis`
    - step to run container docker
        ```sh
        # change directory to docs
        cd docs

        # run docker compose
        docker-compose -f .\postgres_redis.yml up -d
        ```
    - step to turn off container docker
        ```sh
        # turn off docker compose
        docker-compose -f .\postgres_redis.yml down
        ```
    - make sure the DB is already created, 
        - you can open adminer in your browser with url `http://localhost:8080/`
        - login with credential:
            - sistem = PostgreSQL
            - server = postgresDocker
            - pengguna = postgres
            - sandi = postgres
        - check the the DB `db_notification` is exist or not, 
            - you can create it, if not exist
    - make sure your .env file is corrent value
        - FLASK_ENV : value ['development', 'staging', 'production']
        - MAIL_* value, if you want to change it make sure your account is less security and activate IMAP
    
5. run migraton file
    ```sh
    flask db upgrade -d 'models/migrations'
    ```
6. seed data in DB
    ```sh
    # maske sure your root terminal is */core-notif/
    # seed data user recipient
    python .\seeders\seed_user_recipients.py
    ```
7. run server flask
    ```sh
    # maske sure your root terminal is */core-notif/
    flask run
    ```
8. run server celery worker
    ```sh
    # create new terminal and activate the virtualenv
    # maske sure your root terminal is */core-notif/
    
    # celery worker
    celery -A server.celery worker--loglevel INFO

    # celery worker on windows user, `--pool solo`
    celery -A server.celery worker --pool solo --loglevel INFO
    ```

9. run server celery beat (scheduler)
    ```sh
    # create new terminal and activate the virtualenv
    # maske sure your root terminal is */core-notif/
    # maske sure to run celery worker first

    # celery beat
    celery -A server.celery beat --loglevel INFO
    ```

### Need to know
- threshold of timestamp (like delta current_time with input_timestamp) for now is 5 minutes 
<br> you can change it in module `cores/constant` class `ConstEmail` for attribut `THRESHOLD_TIMESTAMP`
     ```
    THRESHOLD_TIMESTAMP = 1     # minutes
    ```


### How to set connection DB
Set your .env file for variable key for `SQLALCHEMY_DATABASE_URI` 
<br> ex : `SQLALCHEMY_DATABASE_URIL="postgresql://username:password@host:port/db_name"`
<br><br>

### How to Manage ORM DB 
1. only for the first time, when you create migration file
    ``` sh
    flask db init -d 'models/migrations'
    ```
2. make migrate file (alembic), for any change in your models
    ``` sh
    flask db migrate -d 'models/migrations' -m 'custom_message'
    ```
    <br> re-check your migrate file in `./models/migrations/versions`, cz cannot detect rename table/column automatically.
3. execute migration for your change in db
    ``` sh
    flask db upgrade -d 'models/migrations'
    ```

    after make ORM class for table [`path: ./models]
<br> make sure your ORM class is registered in table rageister
[`path: ./models/register_tables.py`]
<br> if your new ORM class is not registered yet, you cann't migrate your db
<br><br>


### Unit Test
all of unit test all saved in `tests` folder. 

1. Python unittest 
<br>You can run unit test by executing this command 
    ``` sh
    # run all unittest
    python -m unittest -v tests

    # run specific unittest
    # python -m unittest -v tests.services.moduleName.className.functionName
    # ex:
    python -m unittest -v tests.test_models.test_emails.TestModelForScenarionSendEmail.test_email_query_function_for_filter_by_current_datetime_with_tz_singapore
    ```
2. Coverage
    ``` sh
    # run all test
    # you can skip module/file in .coveragerc file
    coverage run --source='.' --rcfile='.coveragerc' -m unittest -v tests

    # make report
    coverage report

    # make html report
    coverage html
    # you can open it in browser with url input is complete path of htmlcov
    # ex: E:\core-notif\htmlcov
    ```
<br><br>

### Linting
```sh
# you can also you extension for linting like .cornflakes-linter in VSCode
flake8 --config='.pep8'
```
    
<br>


### Direktory explaination:
```sh
./cores             # place for config, static data, common function 
./docs              # place for documentation and important file environment
./models            # place for ORM models and place migration file 
__./migrations      # place migration file 
./schemas           # place for schema validation and serializetion
./seeder            # place for seed data for aplication
./services          # place for controller, modules that run service
./tests             # place for unittest
./urls              # place for url route
.coveragerc         # setting data coverage
.pep8               # setting data flake8
app.py              # setting app flask
server.py           # instance app
requirements.txt    # requirement library python
start-app.sh        # setting bash script to run app
```

### Note:
- this project is create and inspire from flask cookiecuter: https://github.com/cookiecutter-flask/cookiecutter-flask and other 
- The goal is to build blueprint/skeleton microservices project for RESTfull API
- author: ekoabdulaziz96@gmail.com


