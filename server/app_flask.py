"""
A flask application to serve API endpoints to interact with the local database using self-built `DatabaseEditor`
"""
# pylint: disable=redefined-builtin
import json
from flask import Flask, request
from database.local_database import DatabaseEditor, Response

app = Flask(__name__)


def standardise_db_response(response: Response):
    """."""
    code = response.code.value
    data = response.data
    msg = response.msg
    print()
    return {"code": code, "data": data, "msg": msg}


def parse_bool_argument(argument: str):
    """."""
    if argument.lower() == "false":
        argument = False
    else:
        argument = True
    return argument


def read_request_json(json_data):
    """."""
    if isinstance(json_data, str):
        json_data = json.loads(json_data)
    return {"name": json_data.get("name"), "description": json_data.get("description")}


@app.route("/")
def welcome():
    """."""
    return "Welcome to the house! - By Flask"


# GET with params using request.args - for specific option
@app.route("/members", methods=["GET"])
def get_members():
    """."""
    ascending = request.args.get("ascending", default="true", type=str)
    if ascending.lower() not in ("true", "false"):
        return {"api_msg": "`ascending` takes value (true, false)"}
    ascending = parse_bool_argument(ascending)
    response = DatabaseEditor.get_all(ascending=ascending)
    print(standardise_db_response(response))
    return standardise_db_response(response)


# GET with params using special endpoint - for retriving special data item
@app.route("/members/<id>", methods=["GET"])
def get_member(id):
    """."""
    response = DatabaseEditor.get(int(id))
    return standardise_db_response(response)


# POST with data using request.json
@app.route("/members", methods=["POST"])
def add_member():
    """."""
    # json data
    data = read_request_json(request.json)

    # params
    capitalize_name = request.args.get("capitalize_name", default="true", type=str)
    if capitalize_name.lower() not in ("true", "false"):
        return {"api_msg": "`capitalize_name` takes value (true, false)"}
    capitalize_name = parse_bool_argument(capitalize_name)

    response = DatabaseEditor.post(
        name=data["name"],
        description=data["description"],
        capitalize_name=capitalize_name,
    )
    return standardise_db_response(response)


@app.route("/members/<id>", methods=["PUT"])
def edit_member(id):
    """."""
    data = read_request_json(request.json)
    response = DatabaseEditor.put(
        int(id), name=data["name"], description=data["description"]
    )
    return standardise_db_response(response)


@app.route("/members/<id>", methods=["DELETE"])
def delete_member(id):
    """."""
    response = DatabaseEditor.delete(int(id))
    return standardise_db_response(response)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
