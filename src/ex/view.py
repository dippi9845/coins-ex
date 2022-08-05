from abc import abstractmethod
from typing import Any

class View:

    @abstractmethod
    def ask_input(self, msg : str) -> str:
        pass

    @abstractmethod
    def show_message(self, msg : str) -> Any:
        pass

    def menu(self, msg : str, choises : list[str], list_char = "-") -> str:
        self.show_message(msg)
        self.show_message("\n")
        self.show_message(list_char)
        self.show_message(f"\n{list_char}".join(choises))
        return self.ask_input("")


class TerminalView(View):

    def ask_input(self, msg: str) -> str:
        return input(msg)

    def show_message(self, msg: str) -> Any:
        return print(msg)
