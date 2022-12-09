from abc import abstractmethod
from typing import Any
from os import system


class View:

    @abstractmethod
    def ask_input(self, msg : str) -> str:
        pass

    @abstractmethod
    def show_message(self, msg : str) -> Any:
        pass

    @abstractmethod
    def menu(self, msg : str, choises : list[str]) -> str:
        pass

    @abstractmethod
    def chagne_view(self, name_view : str) -> Any:
        pass
    
    @abstractmethod
    def ask_for_multiples(self, msg : str, values : list[str]) -> dict[str]:
        pass


class TerminalView(View):

    def ask_input(self, msg: str) -> str:
        return input(msg)

    def show_message(self, msg: str) -> Any:
        return print(msg)
    
    def menu(self, msg : str, choises : list[str], list_char = "-") -> str:
        self.show_message(msg)
        #self.show_message(list_char)
        self.show_message(f"\n{list_char}" + f"\n{list_char}".join(choises))
        ch = self.ask_input("\n-> ")
        
        if ch in choises:
            return ch
        
        else:
            self.show_message(f"{ch} is not an option, retry")
            return self.menu(msg, choises, list_char=list_char)
    
    
    def chagne_view(self, name_view : str) -> Any:
        system("cls")
    
    
    def ask_for_multiples(self, msg : str, values : list[str]) -> dict[str]:
        self.show_message(msg)
        rtr = {}
        for value in values:
            rtr[value] = self.ask_input(f"{value}: ")
        
        return rtr

class QueueView(View):
    
    def __init__(self, values : str | list[str], sep : str=" ") -> None:
        super().__init__()
        self.queue = values.split(sep) if isinstance(values, str) else values
    
    
    def ask_input(self, msg : str) -> str:
        return self.queue.pop(0)

    
    def show_message(self, msg : str) -> Any:
        pass


    def menu(self, msg : str, choises : list[str]) -> str:
        return self.queue.pop(0)


    def chagne_view(self, name_view : str) -> Any:
        pass
    

    def ask_for_multiples(self, msg : str, values : list[str]) -> dict[str]:
        rtr = {}
        
        for i in values:
            rtr[i] = self.queue.pop(0)
        
        return rtr


class HybridView(View):
    
    def __init__(self, values : str | list[str]=[], sep : str=" ") -> None:
        super().__init__()
        self.queue = values.split(sep) if isinstance(values, str) else values
    
    
    def __get_value(self, msg : str) -> str:
        if len(self.queue) > 0:
            return self.queue.pop(0)
        
        else:
            return input(msg)
    
    
    def ask_input(self, msg : str) -> str:
        return self.__get_value(msg)

    
    def show_message(self, msg : str) -> Any:
        print(msg)


    def menu(self, msg : str, choises : list[str]) -> str:
        self.show_message(msg)
        #self.show_message(list_char)
        self.show_message(f"\n-" + f"\n-".join(choises))
        return self.__get_value("\n-> ")


    def chagne_view(self, name_view : str) -> Any:
        pass
    

    def ask_for_multiples(self, msg : str, values : list[str]) -> dict[str]:
        self.show_message(msg)
        rtr = {}
        
        for i in values:
            rtr[i] = self.__get_value(msg)
        
        return rtr