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
        #print(f"key in -> [{key}] ", end = "")
        plugKey =  self.__plugBoard.encode(key)
        #print(f"plugboard out -> [{plugKey}] ")
        rotorKey = self.__rotorBoard.encode(plugKey)
        #print(f"rotorKey out  -> [{rotorKey}] ", end = "")
        plugKey =  self.__plugBoard.encode(rotorKey)
        #print(f"plugboard out -> [{plugKey}] ")
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
if __name__ == "__main__":


    test_MultipleRotorDemonstration()
    #rotors = [("Beta",1,'A'),("III",1,'A'),("II",1,'A'),("I",1,'A'),("BThin",1,'A')]
    #plugBoardInputs = []
    #machine = EnigmaMachine(rotors, plugBoardInputs)
    #machine.encode("A")
    print("======= test_EnigmaMachineDemonstration1 =======")
    print("Set up your enigma machine with rotors I II III, reflector B, ring settings 01 01 01, and initial positions A A Z.")
    print("The plugboard should map the following pairs: HL MO AJ CX BZ SR NI YW DG PK.")
    text = "HELLOWORLD"
    print(f"INPUT = {text}")
    rotors = [("III",1,'Z'),("II",1,'A'),("I",1,'A'),("B",1,'A')]
    plugBoardInputs = ["HL", "MO" ,"AJ" ,"CX" ,"BZ" ,"SR" ,"NI", "YW" ,"DG" ,"PK"]
    machine = EnigmaMachine(rotors, plugBoardInputs)
    output = ""
    cipher = "RFKTMBXVVW"
    for ch in cipher:
        output += machine.encode(ch)
    print(f"OUTPUT = {output}")
    assert(output == text)
    """
    rotors = [("III",1,'Z'),("II",1,'A'),("I",1,'A'),("B",1,'A')]
    plugBoardInputs = ["HL", "MO" ,"AJ" ,"CX" ,"BZ" ,"SR" ,"NI", "YW" ,"DG" ,"PK"]
    machine = EnigmaMachine(rotors, plugBoardInputs)
    text = "HELLOWORLD".lower()
    cipher = "RFKTMBXVVW".lower()
    output = ""
    cipherOutput = ""
    for ch in cipher:
        output += machine.Encode(ch)
    assert(output == text)
    """
    #Set up your enigma machine with rotors IV V Beta I, reflector A, ring settings 18 24 03 05, and initial positions E Z G P.
    #The plugboard should map the following pairs: PC XZ FM QA ST NB HY OR EV IU.
    rotors = [("I",5,'P'),("Beta",3,'G'),("V",24,'Z'),("IV",18,'E'),("A",1,'A')]
    plugBoardInputs = ["PC", "XZ" ,"FM" ,"QA" ,"ST" ,"NB" ,"HY", "OR" ,"EV" ,"IU"]
    machine = EnigmaMachine(rotors, plugBoardInputs)
    #cipher = "B".lower()
    cipher = "BUPXWJCDPFASXBDHLBBIBSRNWCSZXQOLBNXYAXVHOGCUUIBCVMPUZYUUKHI"
    output = ""
    for ch in cipher:
        output += machine.encode(ch)
    print(output)
    #text = [machine.Encode(ch) for ch in cipher]