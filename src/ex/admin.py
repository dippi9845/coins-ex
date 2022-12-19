from view import View, TerminalView, GUI, HybridView
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
            "create crypto" : self.create_crypto,
            "add worker" : self.add_workers,
            "show workers" : self.show_workers
            
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
        
        while True:
            
            data = ['name', 'surname', 'position', 'salary', 'department', 'residence', 'supervisor']
            worker_data = self.view.ask_for_multiples("Insert worker", data)
            
            if worker_data["name"] == '':
                break
            
            else:
                if worker_data['supervisor'] == '' or worker_data['supervisor'] == 'None' or worker_data['supervisor'] == 'Null':
                    worker_data['supervisor'] = 'NULL'
                
                self.db.insert_into(f"""
                    INSERT INTO dipendente (Nome, Cognome, Carica, Reparto, Residenza, Salario, Presso, Supervisore)
                    VALUES ('{worker_data['name']}', '{worker_data['surname']}', '{worker_data['position']}', '{worker_data['department']}', '{worker_data['residence']}', {worker_data['salary']}, '{exchange_name}', {worker_data['supervisor']})
                """)
            
    
    def show_workers(self):
        columns = ["Carica", "Reparto", "Nome", "Cognome", "Residenza", "Matricola", "Salario", "Presso", "Supervisore"]
        workers = self.db.select("SELECT " + ", ".join(columns) + " FROM dipendente")
        
        to_show = ""
        
        for worker in workers:
            for col, val in zip(columns, worker):
                
                if col == "Supervisore" and val == None:
                    to_show = to_show[:-2]
                    continue
                
                to_show += f"{col} : {val}, "
            
            to_show += "\n"
        
        self.view.show_message(to_show)
    
    
    def add_fiat(self):
        fiat_data = self.view.ask_for_multiples("Insert fiat fileds: ", ["name", "ticker"])
        self.db.insert_into(f"INSERT INTO fiat (Nome, Ticker) VALUES ('{fiat_data['name']}', '{fiat_data['ticker']}')")
        
    
    def create_exchange(self):

        data = ['name', 'operational headquarters', 'registered office', 'website', 'founder']
        exchange_data = self.view.ask_for_multiples("Insert exchange ", data)

        self.db.insert_into(f"""
        INSERT INTO exchange (Nome, `Sede Operativa`, `Sede Legale`, `Sito web`, Fondatore)
        VALUES ('{exchange_data['name']}', '{exchange_data['operational headquarters']}', '{exchange_data['registered office']}', '{exchange_data['website']}', '{exchange_data['founder']}')
        """)

        ch = self.view.menu("Wanto to add workers?", ["y", "n"])
        
        if ch == 'y':
            self.add_workers(exchange_data['name'])
        
    
    def create_atm(self):

        data = ['exchange name', 'street', 'city', 'province', 'model', 'software version', 'commission', 'fiat ticker', 'fiat amount']
        atm_data = self.view.ask_for_multiples("Insert atm data", data)
        
        self.db.insert_into(f"""
            INSERT INTO ATM 
            (Presso, Via, Citta, Provincia, Modello, `Versione Software`, `commissione`)
            VALUES
            ('{atm_data['exchange name']}', '{atm_data['street']}', '{atm_data['city']}', '{atm_data['province']}', '{atm_data['model']}', '{atm_data['software version']}', {atm_data['commission']})
        """)
        
        atm_id = self.db.insered_id()
        
        self.db.insert_into(f"""
        INSERT INTO contante (`Ticker fiat`, `Codice ATM`, Quantita)
        VALUES ('{atm_data['fiat ticker']}', '{atm_id}', {atm_data['fiat amount']})
        """)
    
    
    def create_crypto(self):
        
        crypto_data = self.view.ask_for_multiples("Insert crypto data", ["name", "ticker"])
        self.db.insert_into(f"INSERT INTO crypto (Nome, Ticker) VALUES ('{crypto_data['name']}', '{crypto_data['ticker']}')")
    

if __name__ == "__main__":
    Admin(GUI())
    #Admin(HybridView(["create atm", "Coinbase", "Via Roma", "Roma", "RM", "ATM-001", "1.0", "10", "USD", "1000"]))