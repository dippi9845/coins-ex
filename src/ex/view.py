from abc import abstractmethod

class View:

    @abstractmethod
    def ask_input(self, msg : str):
        pass

    @abstractmethod
    def show_message(self, msg : str):
        pass

    def menu(self, msg : str, choises : list[str], list_char = "-"):
        self.show_message(msg)
        self.show_message("\n")
        self.show_message(list_char)
        self.show_message(f"\n{list_char}".join(choises))
        