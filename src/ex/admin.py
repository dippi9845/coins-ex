from view import View, TerminalView
from database import Database
from uuid import uuid4
from time import time
from random import randbytes
from hashlib import sha256

class Admin:
    
    
    def __init__(self, view : View) -> None:
        self.view = view
        self.db = Database()
    
    
    def create_exchange(self):
        name = self.view.ask_input("Insert exchange name: ")
        oh = self.view.ask_input("Insert exchange operational headquarters: ")
        ro = self.view.ask_input("Insert exchange registered office: ")
        website = self.view.ask_input("Insert exchange website: ")
        founder = self.view.ask_input("Insert exchange founder: ")
        self.db.insert_into(f"INSERT INTO exchange (Nome, SedeOperativa, SedeLegale, SitoWeb, Fondatore) VALUES ('{name}', '{oh}', '{ro}', '{website}', '{founder}')")

    
    def create_atm(self):
        ex_name = self.view.ask_input("Insert exchange name: ")
        street = self.view.ask_input("Insert atm street: ")
        city = self.view.ask_input("Insert atm city: ")
        province = self.view.ask_input("Insert atm province: ")
        model = self.view.ask_input("Insert atm model: ")
        software_version = self.view.ask_input("Insert atm software version: ")
        spread = self.view.ask_input("Insert atm initial spread: ")
        fiat_ticker = self.view.ask_input("Insert atm fiat ticker: ")
        fiat_amount = self.view.ask_input("Insert atm fiat amount: ")
        crypto_ticker = self.view.ask_input("Insert atm crypto ticker: ")
        crypto_amount = self.view.ask_input("Insert atm crypto amount: ")
        atm_id = str(uuid4())
        
        self.db.insert_into(f"""
            INSERT INTO ATM 
            (exchange_name, Via, Citta, Provincia, `Codice Icentificativo`, Modello, `Versione Software`, `Spread attuale`)
            VALUES
            ('{ex_name}', '{street}', '{city}', '{province}', '{atm_id}', '{model}', '{software_version}', {spread * 100})
        """)
        
        self.db.insert_into(f"""
        INSERT INTO contante (`Ticker fiat`, `Codice ATM`, Quantita)
        VALUES ('{fiat_ticker}', '{atm_id}', {fiat_amount})
        """)
        
        self.db.insert_into(f"""
        INSERT INTO Wallet_ATM (ATM_ID, Indirizzo, Saldo, Nome, Ticker)
        VALUES ('{atm_id}', '{sha256(atm_id.encode())}', {crypto_amount}, '{ex_name}', '{crypto_ticker}')
        """)
    
    
    def create_crypto(self):
        pass
    

if __name__ == "__main__":
    pass