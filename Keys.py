import abc
from abc import abstractmethod
from colorama import Fore, Back, Style

class KeysInterface():
    KeyList = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
    ]

import time
import os
class Keyboard(KeysInterface):
    
    def DisplayAvailableKeys(self):
        count = 0
        print(Back.WHITE)
        for key in self.KeyList:
            print(f"[", end='')
            print(Fore.BLUE, f"{key}", end='')
            print(Fore.BLACK, f"]", end='')
            if count == 9:
                print("\n")
                count = 0
            count += 1
        print("\n")

    def DisplayIndicators(self, inKey):
        count = 0
        print(Back.WHITE)
        for key in self.KeyList:
            print(f"(", end='')
            if inKey == key:
                print(Back.YELLOW,Fore.BLUE, f"{key}", end='')
                print(Back.WHITE, end='')
            else:
                print(Fore.BLUE, f"{key}", end='')
            print(Fore.BLACK, f")", end='')
            if count == 9:
                print("\n")
                count = 0
            count += 1    

    def DisplayOutput(self, inKey):
        self.DisplayIndicators(inKey)
        time.sleep(3)
        clear = lambda: os.system('cls')
        clear()
        

    
    def Display(self):
        self.DisplayIndicators("")
        self.DisplayAvailableKeys()
        
    
    def GatherInput(self):

        print(Fore.GREEN, "\n ====> Please input a key.")
        print(Fore.BLACK)
        validKey = False
        counter = 0
        keyPress = ""
        while not validKey:
            keyPress = input()
            if keyPress in self.KeyList:
                break
            else:
                print(Fore.RED,"====> Error, your selection does not match the available list. Please Try Again")
                print(Fore.BLACK)
            if counter == 5:
                print(Fore.RED,"====> Too many errors.")
                print(Fore.BLACK)
                break

        return keyPress