from operator import le
from view import View, TerminalView
from database import Database
from functools import reduce
from  json import dumps

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
        
    def _register(self, excahnge_name : str):
        '''
        register the user to the exchange provided as paramenter
        '''
        if self.__access_info is not None:
            # QUERY register to that exchange
            self.__database.insert_into(f"INSERT INTO registrati (ID, Nome) VALUES ({self.__access_info}, '{excahnge_name}')")

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
        # QUERY get registerd exchnges
        resp = self.__database.select(f"SELCECT Nome FROM registrati WHERE ID = {user_id}")
        self.__registered_exchanges = list(map(lambda x: x[0], resp))
        return True


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
        self.__exchange_addr = None
        self.__access_info = None
        self.__sender = None

if __name__ == "__main__":
    user = User(TerminalView())
    user.run()