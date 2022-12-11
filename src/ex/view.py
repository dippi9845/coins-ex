from abc import abstractmethod
from typing import Any, Callable
from os import system
import tkinter as tk

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
            rtr[i] = self.__get_value(f"{i}: ")
        
        return rtr


class TKview:
    
    def __init__(self, elements : list[dict], handler : Callable, window_size : str="600x600") -> None:
        super().__init__()
        self.window = tk.Tk()
        self.window.geometry(window_size)
        self.window.title("Coins-EX")
        self.handler = handler
        
        self.text_variables = {}
        
        for i in elements:
            
            if i["type"] == "label":
                tk.Label(self.window, text=i["text"]).pack()
            
            elif i["type"] == "button-menu":
                tk.Button(self.window, text=i["text"], command=lambda: self.__close(i["value"])).pack()
            
            elif i["type"] == "input":
                var = tk.StringVar()
                tk.Entry(self.window, textvariable=var).pack()
                self.text_variables[i["text"]] = var
            
            elif i["type"] == "button-confirm":
                tk.Button(self.window, text="confirm", command=lambda: self.__close(self.text_variables)).pack()
    
    def __close(self, value):
        self.handler(value)
        self.window.destroy()
    
    
    def run(self):
        self.window.mainloop()


class GUI(View):  
    
    def __init__(self) -> None:
        super().__init__()
        self.to_add = []
        self.returned = None
    
    
    def _add_elements_next_view(self, elements : list):
        self.to_add = elements
    
    
    def ask_input(self, msg : str) -> str:
        elements = [{
            "type": "label",
            "text": msg
        },
        {
            "type": "input",
            "text": "data"
        },
        {
            "type": "button-confirm"
        }] + self.to_add
        
        self.to_add = []
        
        TKview(elements, self.__get_return_value).run()
        return self.returned
        

    def __get_return_value(self, value=None):
        
        if isinstance(value, dict):
            for i, j in value.items():
                value[i] = j.get()
        
            self.returned = value
        
        elif isinstance(value, tk.StringVar):
            self.returned = value.get()
        
        elif isinstance(value, list):
            self.returned = list(map(lambda x: x.get(), value))
    
        else:
            self.returned = value
    
    
    def show_message(self, msg : str) -> Any:
        elements = [{
            "type": "label",
            "text": msg
        }] + self.to_add
        
        self.to_add = []
        
        TKview(elements, self.__get_return_value).run()

    
    def menu(self, msg : str, choises : list[str]) -> str:
        elements = [{
            "type": "label",
            "text": msg
        }]
        for i in choises:
            elements.append({
                "type": "button-menu",
                "text": i,
                "value": i
            })
        
        elements += self.to_add
        self.to_add = []
        
        TKview(elements, self.__get_return_value).run()
        return self.returned


    
    def chagne_view(self, name_view : str) -> Any:
        pass
    

    
    def ask_for_multiples(self, msg : str, values : list[str]) -> dict[str]:
        elements = [{
            "type": "label",
            "text": msg
        }]
        
        for i in values:
            elements.append({
                "type": "input",
                "text": i
            })
        
        elements += self.to_add
        
        elements.append({
            "type":"button-confirm"
        })
        
        
        self.to_add = []
        
        TKview(elements, self.__get_return_value).run()
        return self.returned
