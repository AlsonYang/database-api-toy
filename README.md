# Purpose of this repo
For new learner who wants to explore web framework (`FastAPI` and `Flask`) for developing RESTful APIs in python.

# What this repo do
TLDR: mimic the real life application where web server hosting different APIs Endpoints for the clients to submit CRUD request to interact with database. 
1. Server side
    - Created a database class `DatabaseEditor` that can create a mock up local database and provides CRUD functionalities.
    - Use `Flask` and `FastAPI` to create RestFul API that talks to the database via `DatabaseEditor` class. Both frameworks provide the same entrypoints and functionalities.
3. Client side
    - Create bash scripts that can be run to submit pre-defined API requests 
    - Create python CLI script to submit customisable API requests

# My finding of `FastAPI` vs `Flask`
### `FastAPI` better than `Flask`
- Easier to get query-param and json-data in the API function. ref: fn `@post add_member`
    - for FastAPI, simply add them as function arguments
    - for Flask, need to get them from request
- Auto-reinforce request data type with type hint. ref: fn`@post add number`
    - For FastAPI, the type hint in the function arguments tells FastAPI to auto-convert the request's data into the right typing
    - For Flask, I will need to create a function `parse_bool_argument` to reinforce the type of argument
### `Flask` better than `FastAPI`
- haven't noticed any yet

# Repo structure
├── Makefile
├── README.md
├── client
│   ├── api_cli.py
│   ├── delete_member.sh
│   ├── get_member.sh
│   ├── get_members.sh
│   ├── post_member.sh
│   └── put_member.sh
├── requirements.txt
└── server
    ├── app_fastapi.py
    ├── app_flask.py
    ├── database
    │   ├── local_database.py
    │   └── member_data.pickle
    └── db_init_cli.py

# Quickstart
## directly run scripts steps
1. install dependency 

    `pip install -r requirements.txt`
2.  Initialise the database: 

    `python server/db_init_cli.py`
3.  spin up the server: 

    `python server/app_fastapi.py` or `python server/app_flask.py`

4.  use any of the client to send API request: see below Client side sections various methods.

## use make file steps
1. install dependency, init database, spinup server

    `make all_fastapi` or `make all_flask`
2. Submit multiple predefined CRUD request
    
    `make curl_request`

# main scripts
## Server side
### database
local database class `server.database.local_database:DatabaseEditor`

    - _init: initialise the database -> output a pickle file `server/database/member_data.pickle` with three columns ('id','name','description')
    - get_all: get all records
    - get: get a specific record by id
    - post: add new record
    - put: edit existing record for a id
    - delete: delete existing record for a id

The purpose of this class is to provide a very simple and ready-to-use mock up database with CRUD operations. Then it can be used by any application (FastApi or Flask) to build 

### `db_init_cli.py`
Script to run the `init` method of the `DatabaseEditor`
usage: `python server/db_init_cli.py --help`

### `server/app_fastapi.py` - FastAPI
Createa API that takes API request and perform corresponding CRUD to the database using `DatabaseEditor`

### `server/app_flash.py` - Flask
Do the same thing as FastAPI

## Client side methods

### 1. client/api_cli.py for API CRUD
usage: `python client/api_cli.py --help`

### 2. client/*.sh for API CRUD
usage: `bash client/<bashfile>`

### 3. postman for CRUD
- GET: http://localhost:8080/members?ascending=True
- GET: http://localhost:8080/members/<id>
- POST: http://localhost:8080/members?capitalize_name=False with data = {"name": "yasuo"}
- PUT:  http://localhost:8080/members/<id> with data = {"name": "yasuo"}
- DELETE: http://localhost:8080/members/<id>

### 4. webbrowser for GET
- http://localhost:8080/members?ascending=True
- http://localhost:8080/members/<id>

# Trouble shooting
### find out which PID is using port 8080
`lsof -i tcp:8080`
### kill the process with PID
`htop` -> `F9` -> `9` -> `Enter`
or
`kill -9 50954`

