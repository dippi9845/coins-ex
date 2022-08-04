from typing import Any
import mysql.connector
from json import loads

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
