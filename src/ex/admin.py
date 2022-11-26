from view import View, TerminalView
from database import Database
from uuid import uuid4
from hashlib import sha256

class Admin:
    
    
    def __init__(self, view : View) -> None:
        self.view = view
        self.db = Database()
        self.functions = {
            "add fiat" : self.add_fiat,
            "create exchange" : self.create_exchange,
            "create atm" : self.create_atm,
            "create crypto" : self.create_crypto
        }
        self.main()
    
    
    def main(self):
        possibilities = set(self.functions.keys())
        possibilities.update(["exit"])
        
        while True:
        
            choice = self.view.menu("Choose an option", possibilities)
        
            if choice == "" or choice == "exit":
                break
        
            self.functions[choice]()
        
    
    
    def add_workers(self, exchange_name=None):
        if exchange_name == None:
            exchange_name = self.view.ask_input("Insert exchange name: ")
        
        num = int(self.view.ask_input("how many workers do you want to add? "))
        for _ in range(num):
            
            data = ['name', 'surname', 'position', 'salary', 'department', 'residence', 'supervisor']
            worker_data = self.view.ask_for_multiples("Insert worker", data)

            if supervisor == '' or supervisor == 'None' or supervisor == 'Null':
                supervisor = 'NULL'
            
            self.db.insert_into(f"""
                INSERT INTO dipendente (Nome, Cognome, Carica, Reparto, Residenza, Stipendio, Presso, Supervisore)
                VALUES ('{worker_data['name']}', '{worker_data['surname']}', '{worker_data['position']}', {worker_data['department']}, {worker_data['residence']}, {worker_data['salary']}, '{exchange_name}', {worker_data['supervisor']}))")
            """)
    
    
    def add_fiat(self):
        fiat_name = self.view.ask_input("Insert fiat name: ")
        fiat_ticker = self.view.ask_input("Insert fiat ticker: ")
        self.db.insert_into(f"INSERT INTO fiat (Nome, Ticker) VALUES ('{fiat_name}', '{fiat_ticker}')")
        
    
    def create_exchange(self):

        data = ['name', 'operational headquarters', 'registered office', 'website', 'founder']
        exchange_data = self.view.ask_for_multiples("Insert exchange ", data)

        self.db.insert_into(f"""
        INSERT INTO exchange (Nome, `Sede Operativa`, `Sede Legale`, `Sito web`, Fondatore)
        VALUES ('{exchange_data['name']}', '{exchange_data['operational headquarters']}', '{exchange_data['registered office']}', '{exchange_data['website']}', '{exchange_data['founder']}')
        """)

        ch = self.view.ask_input("want to add workesr? (y/n): ")
        
        if ch == 'y':
            self.add_workers(exchange_data['name'])
        
    
    def create_atm(self):

        data = ['ex_name', 'street', 'city', 'province', 'model', 'software_version', 'spread', 'fiat_ticker', 'fiat_amount', 'crypto_ticker', 'crypto_amount']
        atm_data = self.view.ask_for_multiples("Insert atm", data)

        atm_id = str(uuid4())
        
        self.db.insert_into(f"""
            INSERT INTO ATM 
            (exchange_name, Via, Citta, Provincia, `Codice Icentificativo`, Modello, `Versione Software`, `Spread attuale`)
            VALUES
            ('{atm_data['ex_name']}', '{atm_data['street']}', '{atm_data['city']}', '{atm_data['province']}', '{atm_data['atm_id']}', '{atm_data['model']}', '{atm_data['software_version']}', {atm_data['spread'] * 100})
        """)
        
        self.db.insert_into(f"""
        INSERT INTO contante (`Ticker fiat`, `Codice ATM`, Quantita)
        VALUES ('{atm_data['fiat_ticker']}', '{atm_id}', {atm_data['fiat_amount']})
        """)
        
        self.db.insert_into(f"""
        INSERT INTO Wallet_ATM (ATM_ID, Indirizzo, Saldo, Nome, Ticker)
        VALUES ('{atm_id}', '{sha256(atm_id.encode())}', {atm_data['crypto_amount']}, '{atm_data['ex_name']}', '{atm_data['crypto_ticker']}')
        """)
    
    
    def create_crypto(self):
        
        nome = self.view.ask_input("Insert crypto name: ")
        ticker = self.view.ask_input("Insert crypto ticker: ")
        
        self.db.insert_into(f"INSERT INTO criptovaluta (Nome, Ticker) VALUES ('{nome}', '{ticker}')")
    

if __name__ == "__main__":
    Admin(TerminalView())