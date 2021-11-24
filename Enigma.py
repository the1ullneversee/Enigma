from Keys import Keyboard
from Plugs import *
from Rotor import *
"""
The battery supplies a current.
The operator presses the A key.
The current flows, 'sending' an A to the plugboard – there is no lead connected to A, so this remains an A.
An A is sent to the rotors through the entry board.
At each rotor, the A is exchanged for another character: in this four-character simplification, at each rotor from right to left:
A becomes F
then F becomes D
then D becomes A
Now, the reflector maps back through the entire circuit again: A becomes F, and this is passed back through the rotors, from left to right:
F becomes S
S becomes A
and A becomes S
S is sent to the plugboard, which this time has a lead connected.
So S is exchanged for D through the lead.
Finally, the D bulb is lit up.
"""
class EnigmaMachine():

    def __init__ (self, rotors, pbInputs):
        self.__plugBoard = Plugboard(pbInputs)
        self.__keyboard = Keyboard()
        #rotors, rotor1 (choice), rotor2 (choice), rotor3 (choice), Reflector choice
        #rotors = [("III",1,'Z'),("II",1,'A'),("I",1,'A'),("B",1,'A')]
        self.__rotorBoard = Rotorboard(rotors)
        self.__message = ""
       
    def GatherInput(self):
        return self.__indicatorKeys.GatherInput()
    
    def DisplayOutput(self, key):
        print(f"=====>  {key}  <======")
        
    def GetRotorBoard(self):
        return self.__rotorBoard
        
    def encode(self, key):
        key = key.upper()
        #first send to plugboard
        plugKey =  self.__plugBoard.encode(key)
        rotorKey = self.__rotorBoard.encode(plugKey)
        plugKey =  self.__plugBoard.encode(rotorKey)
        return plugKey
    
    def Start(self):
        print("Welcome to ENIGMA!")
        key = ''
        while key != '1':
            self.__keyboard.Display()
            print(f"[{self.__message}]")
            key = self.__keyboard.GatherInput()
            if key == "" or key == '1':
                break
            
            outKey = self.Encode(key)
            self.__message += outKey
            self.__keyboard.DisplayOutput(outKey)


        
    

from EnigmaTests import *
from GUI import *
from Keys import *
if __name__ == "__main__":
    gui = GUI()
    
    """
    print("Please input your rotor selections. Example: I,IV,III,C. This is from LEFT to RIGHT on the actual machine.")
    rotorSelection = input()
    rotorSelection = rotorSelection.split(',')
    print("Please input your start positions selections. Example: A,A,B")
    startPositions = input()
    startPositions.split(',')
    print("Please input your ring settings selection. Example: 1,1,2")
    ringSettings = input()
    ringSettings = [int(i) for i in ringSettings.split(',')]
    rotors = [(rotorSelection[0],ringSettings[0],startPositions[0]),(rotorSelection[1],ringSettings[1],startPositions[1]),(rotorSelection[2],ringSettings[2],startPositions[2]),(rotorSelection[3],1,'A')]
    em = EnigmaMachine(rotors,[])
    kb = Keyboard()
    kb.Display()
    kb.GatherInput()
    """
    
