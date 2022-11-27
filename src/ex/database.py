from typing import Any
import mysql.connector
from functools import partial
from ex.config import DatabaseConfig

class Database:
    def __init__(self, cofig : dict=DatabaseConfig) -> None:
        
        self.__cnx = mysql.connector.connect(
            host=cofig['host'],
            user=cofig['username'],
            password=cofig['password'],
            database=cofig["database_name"]
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
    
    def insered_id(self) -> Any:
        return self.__cursor.lastrowid
    
    '''
    from datetime import date, timedelta

    def dategenerator(start, end):
        current = start
        while current <= end:
            yield current
            current += timedelta(days=1)
    '''

    def get_countervalue_by_date(self, ticker_fiat : str, ticker_crypto : str, date : str):
        return self.get_countervalue_by_time(ticker_fiat, ticker_crypto, date, "00:00:00", "23:59:59")
    
    def get_countervalue_by_time(self, ticker_fiat : str, ticker_crypto : str, date : str, time_start : str, time_end : str):
        rtr = self.select(f'''
            SELECT t1.Quantita as crypto, t2.Quantita as fiat
            FROM scambio s
            LEFT JOIN transazione t1 ON s.`Transazione crypto` = t1.ID
            LEFT JOIN transazione t2 ON s.`Transazione fiat` = t2.ID
            WHERE t1.Data="{date}" AND t1.Ticker="{ticker_crypto}" AND t2.Ticker="{ticker_fiat}" AND
            t1.Ora BETWEEN "{time_start}" AND "{time_end}";
        ''')
        numerator = 0

        for i, j in rtr:
            numerator += i * j
        
        return numerator/sum(map(lambda x: x[1], rtr))
        



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
    
    #cursor.execute("")

    with open("../../init.sql", "r") as f:
        query = f.read().split(";")
    
    for i in query:
        
        if i == "" or i == "\n":
            continue
        
        cursor.execute(i)

    print("Done")
