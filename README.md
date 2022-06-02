# Purpose of this repo
For new learner who wants to explore web framework (`FastAPI` and `Flask`) for developing RESTful APIs in python.

# What this repo do
TLDR: mimic the real life application where web server hosting different APIs Endpoints for the clients to submit CRUD request to interact with database. 
1. Server side
    - Created a database class `DatabaseEditor` that can create a mock up local database and provides CRUD functionalities.
        - (Design principle) All the business logic goes in here
    - Use `Flask` and `FastAPI` to create RestFul API that talks to the database via `DatabaseEditor` class. Both frameworks provide the same entrypoints and functionalities.
        - (Desig prinicple) Only make sure the requests data are the right type, and formatting return response to be jsonifiable.
3. Client side
    - Create bash scripts that can be run to submit pre-defined API requests 
    - Create python CLI script to submit customisable API requests

### API funtionality covered
- request type: `POST`, `GET`, `PUT`, `DELETE`
- request info: `Path Param`, `Query Param`, `Request Body` (json data)

# Notes
### FastAPI
- by default, if the parameter in the function is not specified in the endpoint path as path param, then it is a query parameter
- `uvicorn`: FastAPI is a framework to build API, but to host API, we need an API server, and it recommends to use `uvicorn` or `Hypercorn`
- `Pydantic`: FastAPI recommends specifying the 'request body' with Pydantic's `BaseModel` to control data typing for request data. It does automatic data validation for you under the hood.

## TODO
- serve this repo on AWS cloud runner and test it with `Postman`

## What can be improved for this repo
- on API application, when client_error is met, it's better to raise `HTTPException(status_code=..., detail=...)` for error instead of return the reponse directly from database


## My finding of `FastAPI` vs `Flask`
### `FastAPI` better than `Flask`
- Easier to get query-param and json-data in the API function. ref: fn `@post add_member`
    - for FastAPI, simply add them as function arguments
    - for Flask, need to get them from request
- Auto-reinforce request data type with type hint. ref: fn`@post add number`
    - For FastAPI, the type hint in the function arguments tells FastAPI to auto-convert the request's data into the right typing. If it cannot convert into the right type, it will raise error back to client side to ask for the right data type -> No need to do data validation on API side
    - For Flask, I will need to create a function `parse_bool_argument` to reinforce the type of argument, or do tons of data validation after receiving the request data
### `Flask` better than `FastAPI`
- haven't noticed any yet

# Repo structure
```bash
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
```
# Quickstart
## Directly run scripts steps
1. install dependency 

    `pip install -r requirements.txt`
2.  Initialise the database: 

    `python server/db_init_cli.py`
3.  spin up the server: 
    - fastapi
        - `python server/app_fastapi.py` 
        - `cd server && uvicorn app_fastapi:app --reload`
    - flask
        - `python server/app_flask.py`
        - `cd server && export FLASK_APP=app_flask.py && flask run --reload`

4.  use any of the client to send API request: see below Client side sections various methods.

## Use Makefile steps
1. install dependency, init database, spinup server

    `make all_fastapi` or `make all_flask`
2. Submit multiple predefined CRUD request
    
    `make curl_request`

# Main scripts/usages details
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

### 5. built-in docs for `FastAPI`
- (Interactive request UI) http://0.0.0.0:8080/docs
- (Documentation) http://0.0.0.0:8080/redoc


# Trouble shooting
### find out which PID is using port 8080
`lsof -i tcp:8080`
### kill the process with PID
`htop` -> `F9` -> `9` -> `Enter`
or
`kill -9 50954`


# Reference
- [Repo functionalities ideas (server + client)](https://github.com/AlsonYang/Python-MLOps-Cookbook) - Noah Gift: Good to get ideas of what functionalities/tools to learn and code out)
- [How to use Flask (API concept + Flask code)](https://www.youtube.com/watch?v=qbLc5a9jdXo) - Caleb Curry: very beginer friendly
- How to use FastAPI (API concept + FastAPI code) 
    - [Tech with Team](https://www.youtube.com/watch?v=-ykeT6kk4bk&t=2394s): A little advanced and  random errors and debug, good to watch once have written own FastAPI to know a few extra useful stuffs and watch the debug and thinking process
    - [Amjgoscode](https://www.youtube.com/watch?v=GN6ICac3OXY): covers some other concepts like `uvicorn` and `pydantic`

