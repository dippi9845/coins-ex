from logging import root
from typing import Any
import mysql.connector
from json import loads
from functools import partial
from config import DatabaseConfig

class Database:
    def __init__(self) -> None:
        
        self.__cnx = mysql.connector.connect(
            host=DatabaseConfig['host'],
            user=DatabaseConfig['username'],
            password=DatabaseConfig['password'],
            database=DatabaseConfig["database_name"]
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

if __name__ == "__main__":
    host = input("Insert hostname (localhost) : ").strip()
    
    if host == "":
        host = "localhost"
    
    user = input("Insert user name (root) -> ")

    if user == "":
        user = "root"

    passw = input(f"Insert {user} password -> ")
    
    cnx = mysql.connector.connect(
        host=host,
        user=user,
        password=passw
    )
    
    cursor = cnx.cursor()
    # crea il database
    cursor.execute(f"CREATE DATABASE {DatabaseConfig['database_name']}")
    # crea l'utente
    cursor.execute(f"CREATE USER '{DatabaseConfig['username']}'@'{DatabaseConfig['host']}' IDENTIFIED BY '{DatabaseConfig['password']}'")
    cursor.execute(f"GRANT ALL PRIVILEGES ON `{DatabaseConfig['database_name']}` . * TO '{DatabaseConfig['username']}'@'{DatabaseConfig['host']}'")
    cursor.execute("FLUSH PRIVILEGES")
    # crea tabella echanges online
    cursor.execute(f"USE {DatabaseConfig['database_name']}")
    cursor.execute("CREATE TABLE running_exchanges (name VARCHAR(255), host VARCHAR(255), port INT)")
    print("Done")
