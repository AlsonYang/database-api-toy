#!/usr/bin/env python3
'''
A fastapi application to serve API endpoints to interact with the local database using self-built `DatabaseEditor`
'''
#pylint: disable=redefined-builtin
from typing import Union
from fastapi import FastAPI, Path
from pydantic import BaseModel
from database.local_database import DatabaseEditor, Response

app = FastAPI()

class MemberData(BaseModel):
    '''define request body'''
    name: Union[str, None] = None
    description: Union[str, None] = None

def standardise_db_response(response:Response):
    '''.'''
    code = response.code.value
    data = response.data
    msg = response.msg
    return {
        'code': code,
        'data': data,
        'msg': msg
    }

@app.get("/")
def welcome():
    '''.'''
    return 'Welcome to the house! - by FastAPI'

# GET with query-params simply using function argument - for specific option
@app.get("/members")
def get_members(ascending: bool=True):
    '''.'''
    response = DatabaseEditor.get_all(ascending=ascending)
    print(standardise_db_response(response))
    return standardise_db_response(response)

# GET with path-params using special endpoint - for retriving special data item
@app.get("/members/{id}")
def get_member(id: int = Path(None, describe="The ID of the member you'd like to get", gt=0, lt=9999)): # The Path is used to specify description and value constraints for the path parameter.
    '''.'''
    response = DatabaseEditor.get(id)
    return standardise_db_response(response)
    
# POST with data using request-data-model `MemberData` and with query-param
@app.post("/members")
def add_member(member_data: MemberData, capitalize_name:bool =True):
    '''.'''
    response = DatabaseEditor.post(
        name=member_data.name,
        description=member_data.description,
        capitalize_name=capitalize_name
        )
    return standardise_db_response(response)


# PUT with data using request-data-model `MemberData` and with query-param
@app.put("/members/{id}")
def edit_member(id: int, member_data: MemberData):
    '''.'''
    response = DatabaseEditor.put(id, name=member_data.name, description=member_data.description)
    return standardise_db_response(response)

# DELETE using path-param
@app.delete("/members/{id}")
def delete_member(id: int):
    '''.'''
    response = DatabaseEditor.delete(id)
    return standardise_db_response(response)

def run_app(): #
    import nest_asyncio
    import uvicorn
    nest_asyncio.apply()
    host = '0.0.0.0'
    uvicorn.run("app_fastapi:app", host=host, port=8080, reload=True)

if __name__ == '__main__':
    run_app()

