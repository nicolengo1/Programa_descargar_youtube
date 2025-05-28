import tkinter as tk

from colorama import Fore

class ConsoleClass:
    def __init__(self, console):

        self.__console = console


    def ConsoleNormal(self, message):
        print(Fore.WHITE + f"{message}")

        message = str(message) + '\n'
        self.__console.configure(state=tk.NORMAL)
        self.__console.insert(tk.END, message)
        self.__console.configure(state=tk.DISABLED)


    def ConsoleOK(self, message):
        print(Fore.GREEN + f"{message}")

        message = str(message) + '\n'
        self.__console.configure(state=tk.NORMAL)
        self.__console.insert(tk.END, message)
        self.__console.configure(state=tk.DISABLED)


    def ConsoleInfo(self,  message):
        print(Fore.BLUE + f"{message}")

        message = str(message) + '\n'
        self.__console.configure(state=tk.NORMAL)
        self.__console.insert(tk.END, message)
        self.__console.configure(state=tk.DISABLED)


    def ConsoleWarning(self,  message):
        print(Fore.YELLOW + f"{message}")

        message = str(message) + '\n'
        self.__console.configure(state=tk.NORMAL)
        self.__console.insert(tk.END, message)
        self.__console.configure(state=tk.DISABLED)

    def ConsoleError(self, message):
        print(Fore.RED + f"{message}")

        message = str(message) + '\n'
        self.__console.configure(state=tk.NORMAL)
        self.__console.insert(tk.END, message)
        self.__console.configure(state=tk.DISABLED)