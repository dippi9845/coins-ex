from abc import abstractmethod

class View:

    @abstractmethod
    def ask_input(self, msg : str):
        pass

    @abstractmethod
    def show_message(self, msg : str):
        pass