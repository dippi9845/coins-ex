from ex.view import View

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
        
        self.__access_info = None

    def _register(self):
        name = self.__view.ask_input("Insert Name -> ")
        surname = self.__view.ask_input("Insert Surname -> ")
        email = self.__view.ask_input("Insert Emai -> ")
        password = self.__view.ask_input("Insert Password -> ")
        fiscal_code = self.__view.ask_input("Insert Fiscal Code -> ")
        nationality = self.__view.ask_input("Insert Natinality -> ")
        telephone = self.__view.ask_input("Insert Telephone -> ")


    def _access(self):
        '''
        Asks only the credentials
        '''
        self.__access_info = (self.__view.ask_input("insert email"), self.__view.ask_input("insert password"))
    
    def _report(self):
        '''
        request a report from the exchange
        '''
        pass

    def exit(self):
        '''
        exit from the current exchange
        '''
        self.__access_info = None

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
        pass

if __name__ == "__main__":
    user = User()
    user.run()