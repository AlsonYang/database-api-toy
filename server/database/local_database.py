'''
A local database editor class that provide CRUD (create, read, update, delete) operations

Notes: The way I choose between Reponse and exception is that:
    - for response: it is something that the client should care ie. 1. Providing an `id` that doesnt exist. 2. Query when the database hasn't been created
    - for Exception: it is something that the client shouldn't care ie. 1. try to _init the database while it already exists. 2. multiple members with the same ids, which shouldn't happen
'''
import os
from dataclasses import dataclass
from enum import Enum
import pandas as pd

class ResponseCode(Enum):
    '''.'''
    info = 100
    success = 200
    redirect = 300
    client_error = 400
    server_error = 500

@dataclass
class Response:
    '''.'''
    code: ResponseCode
    msg:str = None
    data:dict = None


@dataclass
class DatabaseEditor:
    '''.'''
    db_file = 'server/database/member_data.pickle'

    @classmethod
    def _init(cls, force=False):
        if os.path.exists(cls.db_file) and not force:
            raise Exception(f'Database `{cls.db_file}` already exists')
        
        df = pd.DataFrame(columns=['id', 'name','description'])
        df.to_pickle(cls.db_file)
        return Response(msg=f'{cls.db_file} is initalised', code=ResponseCode.success)

    @classmethod
    def get_all(cls, ascending: bool=True):
        '''.'''
        try:
            df = pd.read_pickle(cls.db_file)
            df.sort_values(by='id', ascending=ascending, inplace=True)
            return Response(data=df.to_dict('records'), code=ResponseCode.success)
        except Exception as e:
            return Response(msg=e, code=ResponseCode.client_error)
    
    @classmethod
    def get(cls, id: int):
        '''.'''
        df = pd.read_pickle(cls.db_file)
        df = df.loc[df['id'] == id]
        if len(df) == 1:
            return Response(data=df.to_dict('records'),code=ResponseCode.success)
        elif len(df) == 0:
            return Response(msg=f'no such member with id: `{id}`', code=ResponseCode.client_error)
        else:
            raise Exception(f'multile members with the same id {id} detected')

    @classmethod
    def post(cls, name:str, description:str=None, capitalize_name:bool =True):
        '''.'''
        if capitalize_name:
            name = name.capitalize()
        df = pd.read_pickle(cls.db_file)
        if not name:
            return Response(msg=f'name `{name}` is not a valid name', code=ResponseCode.client_error)
        if name in df['name'].values:
            return Response(msg=f'name `{name}` already exists in the database', code=ResponseCode.client_error)

        if len(df) == 0:
            id = 1
        else:
            id = df.iloc[-1]['id'] + 1
        new_data = {'id': id, 'name': name, 'description': description}
        new_row = pd.DataFrame.from_dict({k:[v] for k,v in new_data.items()})
        new_df = pd.concat([df, new_row], axis=0)
        new_df.to_pickle(cls.db_file)
        return Response(msg=f'member `{new_data}` is added into database `{cls.db_file}`', code=ResponseCode.success)
    
    @classmethod
    def put(cls, id:int, name:str=None, description:str=None):
        '''.'''
        if name is None and description is None:
            return Response(msg='Nothing updated, nor name or description is provided', code=ResponseCode.client_error)
        df = pd.read_pickle(cls.db_file)
        if id not in df['id'].values:
            return Response(msg=f'no such member with id: `{id}`', code=ResponseCode.client_error)
        if name is not None:
            df.loc[df['id']==id, 'name'] = name
        if description is not None:
            df.loc[df['id']==id, 'description'] = description
        df.to_pickle(cls.db_file)
        member_data = cls.get(id).data
        return Response(msg=f'`{member_data}` is updated in `{cls.db_file}`', code=ResponseCode.client_error)

    @classmethod
    def delete(cls, id):
        '''.'''
        df = pd.read_pickle(cls.db_file)
        if id not in df['id'].values:
            return Response(msg=f'no such member with id: `{id}`', code=ResponseCode.client_error)
        member_data = cls.get(id).data
        df = df.loc[df['id']!=id]
        df.to_pickle(cls.db_file)
        return Response(msg=f'`{member_data}` is removed from `{cls.db_file}`', code=ResponseCode.success)

if __name__ == '__main__':
    print(DatabaseEditor._init())


