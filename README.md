# CORE-NOTIF 

application for manage Notification

## Prerequisites

[![Code](https://img.shields.io/badge/Code-Python-1B9D73?style=flat&logo=python)](https://python.org)
[![Framework](https://img.shields.io/badge/Framework-Flask-1B9D73?style=flat&logo=flask)](https://flask.palletsprojects.com/)


## How to run
Make sure you already installed **python3.8** in your machine

1. Create your virtualenv and activate
2. Install library `pip install -r requirements.txt`
3. Move your root path to this project
4. make config.py file in `./cores` directory  
duplicate `config_dev/stag/prod.py` file and rename as config.py
5. init flask migrate file location `flask db init -d 'models/migrations'`
    <br> if not yet and only for the first time, check `./models/migrations`
6. run server command `sh ./start-app.sh` 

### How to run server manually
1. set your Env Variabel key for `Flask_APP` and `FLASK_ENV` 
    <br> `$env:FLASK_APP="server.py"`
    <br> `$env:FLASK_ENV="development"`
2. migrate your db
    <br> `flask db upgrade -d 'models/migrations'`
3. run server
    <br> `flask run --host=0.0.0.0 --port=63000`

### How to connect DB locally
Set your Env Variable key for `DATABASE_URL` 
<br> ex : `$env:DATABASE_URL="postgresql://username:password@host:port/db_name"`
<br><br>

### How to Manage ORM DB 
1. make migrate file (alembic), for any change in your models
    <br>`flask db migrate -d 'models/migrations' -m 'message'`
    <br> recheck your migrate file in `./models/migrations/versions`, cz cannot detect rename table/column automatically.
2. execute migration for your change in db
    <br>`flask db upgrade -d 'models/migrations'`

after make ORM class for table [`path: ./models]
<br> make sure your ORM class is registered in table rageister
[`path: ./models/register_tables.py`]
<br> if your new ORM class isnot reistered, you cann't migrate your db
<br><br>


### Unit Test
all of unit test all saved in `tests` folder. 

1. Python unittest 
<br>You can run unit test by executing this command 
<br> `python -m unittest -v tests.{module}`
<br> ex : `python -m unittest -v ./tests.services.moduleName.className.functionName`

2. Coverage
      * `coverage run --source='.' --rcfile='.coveragerc' -m unittest -v tests`
      * `coverage report`
      * `coverage html`
<br><br>

### Linting

`flake8 --config='.pep8'`
<br><br>


### Direktory explaination:
```sh
./code_executes     # place for code to run independently
./cores             # place for config, static data, common function 
./models            # place for ORM models and place migration file 
__./migrations      # place migration file 
./services          # place for controller, modules that run service
./settings          # place for setting env, instance librabry 
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
