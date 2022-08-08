from view import View, TerminalView
from packet_trasmitter import PacketTransmitter
from database import Database
from functools import reduce
from  json import dumps
from exchange import ExchangeCommands

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
        
        self.__exchange_addr = None
        self.__exchange_name = None
        self.__access_info = None
        self.__sender = PacketTransmitter()
        self.__database = Database()
    
    def __send_to_exchange(self, cmd_data : dict):
        self.__sender.send_data(dumps(cmd_data), self.__exchange_addr)

    def _register(self):
        to_send = {
            ExchangeCommands.COMMAND_SPECIFIER.value : ExchangeCommands.REGISTER.value,
            "name" : self.__view.ask_input("Insert Name -> "),
            "surname" : self.__view.ask_input("Insert Surname -> "),
            "email" : self.__view.ask_input("Insert Emai -> "),
            "password" : self.__view.ask_input("Insert Password -> "),
            "fiscal_code" : self.__view.ask_input("Insert Fiscal Code -> "),
            "nationality" : self.__view.ask_input("Insert Natinality -> "),
            "telephone" : self.__view.ask_input("Insert Telephone -> ")

        }

        self.__send_to_exchange(to_send)
        self.__access_info, _ = self.__sender.get_data()

        if self.__access_info is None:
            return False
        
        else:
            return True

    def _set_exchange(self, name : str, addr : tuple[str, int]):
        self.__exchange_addr = addr
        self.__exchange_name = name

    def _current_exchanges(self) -> dict:
        '''
        list all currrent databases
        '''
        rtr = self.__database.select("SELECT name, host, port FROM server")
        rtr = list(map(lambda x: {x[0] : (x[1], x[2])}, rtr))
        rtr = reduce(lambda a, b: {**a, **b}, rtr)
        return rtr

    def _access(self) -> bool:
        '''
        Asks only the credentials
        '''
        to_send = {
            ExchangeCommands.COMMAND_SPECIFIER.value : ExchangeCommands.GET_COOKIE.value,
            "email" : self.__view.ask_input("insert email -> "),
            "password" : self.__view.ask_input("insert password -> ")
        }
        
        self.__send_to_exchange(to_send)
        self.__access_info, _ = self.__sender.get_data()

        if self.__access_info is None:
            return False
        
        else:
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
            possibles = set(excs.keys())
            possibles.update({"", "update"})

            ch = self.__view.menu("Choose avaiable exchanges", possibles)
            
            if ch == "":
                break

            elif ch == "update":
                continue

            self._set_exchange(ch, excs.get(ch))

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