from view import View, TerminalView
from database import Database
from uuid import uuid4
from hashlib import sha256

class Admin:
    
    
    def __init__(self, view : View) -> None:
        self.view = view
        self.db = Database()
        self.main()
        self.functions = {
            "add fiat" : self.add_fiat,
            "create exchange" : self.create_exchange,
            "create atm" : self.create_atm,
            "create crypto" : self.create_crypto
        }
    
    
    def main(self):
        self.view.menu("Choose an option", list(self.functions.keys()))
    
    
    def add_workers(self, exchange_name=None):
        if exchange_name == None:
            exchange_name = self.view.ask_input("Insert exchange name: ")
        
        num = int(self.view.ask_input("how many workers do you want to add? "))
        for _ in range(num):
            name = self.view.ask_input("Insert worker name: ")
            surname = self.view.ask_input("Insert worker surname: ")
            position = self.view.ask_input("Insert worker role: ")
            salary = self.view.ask_input("Insert worker salary: ")
            department = self.view.ask_input("Insert worker department: ")
            residence = self.view.ask_input("Insert worker residence: ")
            supervisor = self.view.ask_input("Insert worker supervisor's number: ")
            
            if supervisor == '' or supervisor == 'None' or supervisor == 'Null':
                supervisor = 'NULL'
            
            self.db.insert_into(f"""
                INSERT INTO dipendente (Nome, Cognome, Carica, Reparto, Residenza, Stipendio, Presso, Supervisore)
                VALUES ('{name}', '{surname}', '{position}', {department}, {residence}, {salary}, '{exchange_name}', {supervisor}))")
            """)
    
    
    def add_fiat(self):
        fiat_name = self.view.ask_input("Insert fiat name: ")
        fiat_ticker = self.view.ask_input("Insert fiat ticker: ")
        self.db.insert_into(f"INSERT INTO fiat (Nome, Ticker) VALUES ('{fiat_name}', '{fiat_ticker}')")
        
    
    def create_exchange(self):
        name = self.view.ask_input("Insert exchange name: ")
        oh = self.view.ask_input("Insert exchange operational headquarters: ")
        ro = self.view.ask_input("Insert exchange registered office: ")
        website = self.view.ask_input("Insert exchange website: ")
        founder = self.view.ask_input("Insert exchange founder: ")
        self.db.insert_into(f"INSERT INTO exchange (Nome, SedeOperativa, SedeLegale, SitoWeb, Fondatore) VALUES ('{name}', '{oh}', '{ro}', '{website}', '{founder}')")

        ch = self.view.ask_input("want to add workesr? (y/n): ")
        
        if ch == 'y':
            self.add_workers(name)
        
    
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
        
        nome = self.view.ask_input("Insert crypto name: ")
        ticker = self.view.ask_input("Insert crypto ticker: ")
        
        self.db.insert_into(f"INSERT INTO criptovaluta (Nome, Ticker) VALUES ('{nome}', '{ticker}')")
    

if __name__ == "__main__":
    pass