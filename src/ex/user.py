from ex.view import View

class User:

    ACCESS_EXCHANGE = ["register", "access"]
    EXCHANGE_COMMANDS = ["deposit", "withdraw", "sell", "buy", "report" ,"exit"]

    def __init__(self, view : View) -> None:
        self.__view = view
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
    
    def exit(self):
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