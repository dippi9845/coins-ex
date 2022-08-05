from typing import Any
import mysql.connector
from json import loads
from functools import partial

class Database:
    def __init__(self) -> None:
        
        with open("database_config.json", "r") as f:
            data = loads(f.read())
        
        self.__cnx = mysql.connector.connect(
            host=data['host'],
            user=data['username'],
            password=data['password'],
            database=data["database_name"]
        )

        self.__cursor = self.__cnx.cursor()

        self.insert_into = self.delete = self.update = partial(self.execute, commit=True)
        self.insert_many = partial(self.execute_many, commit=True)
        self.close = self.__cnx.close
    
    def execute(self, sql : str, commit : bool=False) -> Any:
        rtr = self.__cursor.execute(sql)
        
        if commit:
            self.__cnx.commit()
        
        return rtr
    
    def execute_many(self, sql : str, val, commit : bool=False) -> Any:
        rtr = self.__cursor.executemany(sql, val)
        
        if commit:
            self.__cnx.commit()
        
        return rtr
    
    def select(self, sql : str) -> Any:
        self.execute(sql)
        return self.__cursor.fetchall()

