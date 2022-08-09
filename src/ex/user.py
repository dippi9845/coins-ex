from view import View, TerminalView
from database import Database
from hashlib import sha256
from time import time
from random import randbytes
from enum import Enum

class OptionType(Enum):
    BUY = "Compra",
    SELL = "Vendi"

class User:

    def __init__(self, view : View) -> None:
        self.__view = view
        
        self.access_exchange = {
            "register" : self._register,
            "access" : self._access
        }

        self.exchange_commands = {
            "deposit" : self._deposit,
            "withdraw" : self._withdraw,
            "sell" : self._sell,
            "buy" : self._buy,
            "report" : self._report,
            "exit" : self.exit
        }
        
        self.__exchange_name = None
        self.__access_info = None
        self.__registered_exchanges = []
        self.__database = Database()

    def __make_transaction(self, address_in : str, address_out : str, ticker : str, amount : int):
        # QUERY create a transaction
        self.__database.insert_into(f'''INSERT INTO transazione () VALUES() ''')

    def _first_access(self):
        
        name = self.__view.ask_input("Insert Name -> ")
        surname = self.__view.ask_input("Insert Surname -> ")
        email = self.__view.ask_input("Insert Emai -> ")
        password = self.__view.ask_input("Insert Password -> ")
        fiscal_code = self.__view.ask_input("Insert Fiscal Code -> ")
        nationality = self.__view.ask_input("Insert Natinality -> ")
        telephone = self.__view.ask_input("Insert Telephone -> ")
        residence = self.__view.ask_input("Insert Residence -> ")
        bith_day = self.__view.ask_input("Insert Bith Day -> ")

        to_register = self.__view.menu("Choose the first exchange", self._current_exchanges())

        # QUERY insert utente instance
        self.__database.insert_into(f'''
        INSERT INTO utente
        (Nome, Cognome, Email, Password, `Codice Fiscale`, Nazionalita, `Numero Di Telefono`, Residenza, `Data di nascita`)
        VALUES({name}, {surname}, {email}, {password}, {fiscal_code}, {nationality}, {telephone}, {residence}, {bith_day})
        ''')

        # QUERY get ID of least insered user
        resp = self.__database.insert_into(f"SELECT ID FROM utente WHERE Email = '{email}' AND Password = '{password}'")
        self.__access_info = resp[0]

        self._register(to_register)
        
    def _register(self, exchange_name : str):
        '''
        register the user to the exchange provided as paramenter
        '''
        if self.__access_info is not None:
            # QUERY register to that exchange
            self.__database.insert_into(f"INSERT INTO registrati (ID, Nome) VALUES ({self.__access_info}, '{exchange_name}')")
            self._create_fiat_account(exchange_name)
            self.__registered_exchanges.append(exchange_name)

    def _set_exchange(self, name : str):
        self.__exchange_name = name

    def _current_exchanges(self) -> list[str]:
        '''
        list all currrent databases
        '''
        # QUERY get all existing exchanges
        rtr = self.__database.select("SELECT Nome FROM exchange")
        rtr = list(map(lambda x: x[0], rtr))
        return rtr

    def _access(self) -> bool:
        '''
        Asks only the credentials
        '''
        
        email = self.__view.ask_input("insert email -> ")
        password = self.__view.ask_input("insert password -> ")
        
        # QUERY get id
        resp = self.__database.select(f"SELECT ID FROM utente WHERE Email = '{email}' AND Password = '{password}'")
        
        if len(resp) == 0:
            return False

        user_id = resp[0]
        self.__access_info = user_id
        # QUERY get registerd exchnges
        resp = self.__database.select(f"SELCECT Nome FROM registrati WHERE ID = {user_id}")
        self.__registered_exchanges = list(map(lambda x: x[0], resp))
        return True

    def _create_wallet(self, exchange_name : str, crypto_ticker : str):
        if self.__access_info is not None:
            to_hash = str(self.__access_info).encode() + b"ID" + str(int(time())).encode() + b"RND" + randbytes(10)
            # QUERY create an istance of contocorrente
            
            self.__database.insert_into(f'''
                INSERT INTO wallet (Indirizzo, Saldo, Nome, Ticker)
                VALUES ("{sha256(to_hash).hexdigest()}", 0, "{exchange_name}", "{crypto_ticker}")
            ''')

    def _create_fiat_account(self, exchange_name : str, fiat_ticker : str="EUR", amount : int=1000):
        if self.__access_info is not None:
            to_hash = str(self.__access_info).encode() + b"ID" + str(int(time())).encode() + b"RND" + randbytes(10)
            # QUERY create an istance of contocorrente
            
            self.__database.insert_into(f'''
                INSERT INTO contocorrente (Indirizzo, Saldo, Nome, Ticker)
                VALUES ("{sha256(to_hash).hexdigest()}", {amount}, "{exchange_name}", "{fiat_ticker}")
            ''')
            

    def _report(self):
        '''
        request a report from the exchange
        '''
        pass

    def _sell(self):
        '''
        want to sell crypto
        '''
        pass

    def _buy(self):
        '''
        want to buy crypto
        '''
        pass

    def _withdraw(self, atm_id : str):
        '''
        withdraw fiat money 
        '''
        pass

    def _deposit(self):
        '''
        deposit fiat money
        '''
        pass

    def run(self):
        '''
        keep intercting with the user
        '''
        while True:
            excs = self._current_exchanges()
            possibles = set(excs)
            possibles.update({"", "update"})

            ch = self.__view.menu("Choose avaiable exchanges", possibles)
            
            if ch == "":
                break

            elif ch == "update":
                continue

            self._set_exchange(ch)

            ch = self.__view.menu(f"Do you want to register or access to {self.__exchange_name}", ["register", "access"])
            
            if self.access_exchange[ch]():
                while ch != "exit":
                    ch = self.__view.menu(f"What do you want to do on {self.__exchange_name} ?", self.exchange_commands.keys())
                    self.exchange_commands[ch]()
            else:
                print(f"error during {ch}")


    def exit(self):
        '''
        exit from the current exchange
        '''
        self.__access_info = None
        self.__database.close()

if __name__ == "__main__":
    user = User(TerminalView())
    user.run()