from enum import Enum
import itertools
from typing import Mapping
from CustomExceptions import *

import os 
alphabet = [
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    ]

LABEL_TO_MAPPING = {"Beta": "L,E,Y,J,V,C,N,I,X,W,P,B,Q,M,D,R,T,A,K,Z,G,F,U,H,O,S",
"Gamma": "F,S,O,K,A,N,U,E,R,H,M,B,T,I,Y,C,W,L,Q,P,Z,X,V,G,J,D",
"I": "E,K,M,F,L,G,D,Q,V,Z,N,T,O,W,Y,H,X,U,S,P,A,I,B,R,C,J",
"II": "A,J,D,K,S,I,R,U,X,B,L,H,W,T,M,C,Q,G,Z,N,P,Y,F,V,O,E",
"III":"B,D,F,H,J,L,C,P,R,T,X,V,Z,N,Y,E,I,W,G,A,K,M,U,S,Q,O",
"IV": "E,S,O,V,P,Z,J,A,Y,Q,U,I,R,H,X,L,N,F,T,G,K,D,C,M,W,B",
"V": "V,Z,B,R,G,I,T,Y,U,P,S,D,N,H,L,X,A,W,M,J,Q,O,F,E,C,K",
"VI": "J,P,G,V,O,U,M,F,Y,Q,B,E,N,H,Z,R,D,K,A,S,X,L,I,C,T,W",
"VII": "N,Z,J,H,G,R,C,X,M,Y,S,W,B,O,U,F,A,I,V,L,P,E,K,Q,D,T",
"VIII": "F,K,Q,H,T,L,X,O,C,B,J,S,P,D,Z,R,A,M,E,W,N,I,U,Y,G,V",
"A": "E,J,M,Z,A,L,Y,X,V,B,W,F,C,R,Q,U,O,N,T,S,P,I,K,H,G,D",
"B": "Y,R,U,H,Q,S,L,D,P,X,N,G,O,K,M,I,E,B,F,Z,C,W,V,J,A,T",
"C": "F,V,P,J,I,A,O,Y,E,D,R,Z,X,W,G,C,T,K,U,Q,S,B,N,M,H,L",
"BThin": "E,N,K,Q,A,U,Y,W,J,I,C,O,P,B,L,M,D,X,Z,V,F,T,H,R,G,S",
"CThin" :"R,D,O,B,J,N,T,K,V,E,H,M,L,F,C,W,Z,A,X,G,Y,I,P,S,U,Q"}

#This class is of type Enum, allowing us to set the rotor types we support and allow comparision of rotor types.
class RotorType(Enum):
    Notch = 0
    NonNotch = 1
    Reflector = 2


class Rotor():

    supportedRotors = [ "I","II", "III", "IV", "V","VI","VII","VIII", "A", "B","C","BThin","CThin", "Beta", "Gamma"]
    rotorTypeToLabel = {"I": RotorType.Notch,"II": RotorType.Notch, "III": RotorType.Notch, "IV": RotorType.Notch, "V": RotorType.Notch,"VI": RotorType.Notch,"VII": RotorType.Notch,"VIII": RotorType.Notch,
     "A": RotorType.Reflector, "B": RotorType.Reflector,"C": RotorType.Reflector,"BThin": RotorType.Reflector,"CThin": RotorType.Reflector, "Beta": RotorType.NonNotch, "Gamma": RotorType.NonNotch}

    def __init__ (self, label, ringSetting, offset):
        #check inputs are in valid ranges
        self.ringSettingMax = 26

        if not self.__checkInputs(label, ringSetting, offset):
            return

        self.RotorType = self.rotorTypeToLabel[label]
        self.rPins = alphabet.copy()
        self.alphabetRing = alphabet.copy()
        #holds the wiring pins mapping
        self.mapping = [None]*2
        self.mapping[0] = alphabet.copy()
        self.mapping[1] = [a for a in self.__loadInputData(label)]
        #name of our rotor

        self.rotorName = label
        
        self.rotorOffset = alphabet.index(offset)
        self.ringSetting = ringSetting
        self.options = len(self.mapping[0])
        self.__ringSettingAdjustment()
    
    #Function is used to check the inputs passed in during construction and raising an exception if they fall out of acceptable ranges and inputs
    def __checkInputs(self, label, ringSetting, offset):
        if label not in self.supportedRotors:
            raise ConfigurationException("Rotor Type Not Supported!",label)
        if label == "" or label not in self.supportedRotors:
            raise ConfigurationException("Rotor Not Supported!", label)
        if ringSetting < 0 or ringSetting > self.ringSettingMax:
            raise ConfigurationException("Ring Setting Not Supported!", ringSetting)
        if offset not in alphabet:
            raise ConfigurationException("Rotor Offet Not Supported!", offset)
        return True

    #this function takes the ring setting provided in the constructor and adjusts the mappings accordingly.
    #A ring setting adjustment has the effect of moving up the values by the ring setting adjustment. This can be done in one swoop by working out the offsets and applying that to a new list and copying it back.
    def __ringSettingAdjustment(self):
        #if ring setting is greater than 1, IE A, and rotor is not a refelctor
        if self.ringSetting > 1 and self.RotorType.value != RotorType.Reflector:
            #adjust the ring setting for a zero indexed array
            rs = (self.ringSetting -1)
            index = 0
            #generate a new list of size options, which is our mappings number (26)
            newList = [0]*self.options
            #i is equal to rs modulo options - 1
            i = rs  % (self.options -1)
            #for each map in out mappings list
            for map in self.mapping[1]:
                #get the initial index
                alphabetIndex = alphabet.index(map)
                #adjust the index based on the ring setting, using modulo to wrap
                adjusted = (alphabetIndex + rs)%26
                #set that mapping to the alphabet value with the adjusted index
                self.mapping[1][index] = alphabet[adjusted]
                #set the newList[i] to the adjusted value
                newList[i] = alphabet[adjusted]
                index += 1
                i = (i + 1) % (self.options)
            #copy over the mapping
            self.mapping[1] = newList.copy()

    #instead of physically rotating the mapping list, all we do is store a rotor offset to be used in calculation. This should save us time. 
    def rotate(self):
        if self.RotorType != RotorType.Reflector:
            self.rotorOffset = (self.rotorOffset + 1) % self.options

    #Purpose of this function is to load the Rotor Mappings from a local text file. This was later changed to read from a static list. Reason being Jupyter was kicking up such a fuss about not finding the file. 
    def __loadInputData(self, label):
        try:
            if label in LABEL_TO_MAPPING:
                return LABEL_TO_MAPPING[label].split(',')
        except:
            return
    
    #purpose of this function is to encode the key value from the input, adjusting for rotor offsets
    def encodeRight(self,key):
        #print(f"key in {key} ",end="")
        #do key in to pin transform if the offset is > 0. Basically if the rotor has rotated then the input pins no longer match up with what is incoming. 
        if self.rotorOffset > 0:
            offset = self.rotorOffset
            modAdjusted = ((alphabet.index(key)) + offset) % self.options
            key = alphabet[modAdjusted]
            #print(f"adjusted by offset to {key} ",end="")
        
        #mapping is two lists [0] = Labels, [1] = pin to map to.
        #from the self.mapping[0] labels, search for the input key, use that index to retrieve the map in the corresponding list.
        outputKey = self.mapping[1][self.mapping[0].index(key)]
        #print(f"mapped to {outputKey} ",end="")
        #print(f"in {key} to mapping {outputKey}")
        #like the input transformation, we must offset are output by the rotor offset
        if self.rotorOffset > 0:
            offset = self.rotorOffset
            modAdjusted = ((alphabet.index(outputKey)) - offset) % self.options
            outputKey = alphabet[modAdjusted]
            #print(f"adjusted by rotor offset to {outputKey} ",end="")
        #print(f" out {outputKey}")
        return outputKey
        
    #function like encode right, except we perform the mapping different
    def encodeLeft(self,key):
        #print(f"key in {key} ",end="")
        if self.rotorOffset > 0:
            offset = self.rotorOffset
            modAdjusted = ((alphabet.index(key)) + offset) % self.options
            key = alphabet[modAdjusted]
            #print(f"adjusted by offset to {key} ",end="")
            #print(f"rotor adjusted {key} ", end= "")
        
        #this works like the encode right version, except we search in the pins to find the label. 
        outputKey = self.mapping[0][self.mapping[1].index(key)]
        #print(f"mapped to {outputKey} ",end="")
        #print(f"in {key} to mapping {outputKey}")
        if self.rotorOffset > 0:
            offset = self.rotorOffset
            modAdjusted = ((alphabet.index(outputKey)) - offset) % self.options
            outputKey = alphabet[modAdjusted]
            #print(f"adjusted by rotor offset to {outputKey} ",end="")
        #print(f" out {outputKey}")
        return outputKey
    
    #to satisfy the built in tests on the Jupyter sheet
    def encode_right_to_left(self, letter):
        return self.encodeRight(letter)
        
    #to satisfy the built in tests on the Jupyter sheet
    def encode_left_to_right(self, letter):
        return self.encodeLeft(letter)

#to satisfy the built in tests on the Jupyter sheet
def rotor_from_name(letter):
        return Rotor(letter, 1, 'A')

#This class is an implementation of what the Enigma Rotor Board would do. Housing the Rotors, allowing for rotation.
class Rotorboard():
    #rotor notch to label map
    rotorNotchMap = {"I": 'Q', "II": "E", "III": "V", "IV": "J", "V": "Z", "VI" :"Z,M", "VII": "Z,M", "VII": "Z,M"}
    rotorList = []
    #Your Enigma machine must support three or four rotors and one reflector
    #notice that a reflector is really just a type of rotor where the characters line up in 13 perfect pairs. 
    #extend this to take a list of arguements
    def __init__ (self, rotorInputs):
        #set up the rotors from the input list. 
        self.__addRotorsFromInput(rotorInputs)
        
    def __addRotorsFromInput(self, rotorInputs):
        self.rotorList = []
        for arg in rotorInputs:
            self.rotorList.append(Rotor(*arg))

    #function is responsible for rotating each of the rotors based on pre-defined conditions. 
    def __rotateRings(self):
        nextRingRotate = False
        #when we rotate we always rotate the first ring
        rotor = self.rotorList[0]
        #grab the current key we are on
        currentKey = rotor.rPins[rotor.rotorOffset]
        #we check non notch here as we need to grab the notch value out of notch map
        if rotor.rotorName in self.rotorNotchMap:
            notchPoint = self.rotorNotchMap[rotor.rotorName]
        else:
            notchPoint = ""

        #rotate the rotor.
        rotor.rotate()
        
        #no need to continue if rotor type is non notch
        if rotor.RotorType == RotorType.NonNotch:
            return

        #check that the current key is on its notch point, if so we need to rotate the next ring. But we only do this if the Rotor is of a certain type.
        if currentKey in notchPoint and rotor.RotorType != RotorType.NonNotch:
            nextRingRotate = True
        i = 1
        #if we enter this loop, it means the first rotor has rotated.
        #the loop checks if the rotor is of type to be rotated, if so it rotates, then checks the notch point.
        for i in range(1, len(self.rotorList)):
            #get next rotor
            rotor = self.rotorList[i]
            #check rotor number, if we have already checked up till 3, but there's more than 4 rotors in the list (remember a reflector counts as a rotor) then we exit out as the 4th never rotates.
            if len(self.rotorList) > 4 and i == 3:
                break

            #get the current key and notch point
            currentKey = rotor.rPins[rotor.rotorOffset]
            if rotor.rotorName in self.rotorNotchMap:
                notchPoint = self.rotorNotchMap[rotor.rotorName]
            else:
                notchPoint = ""

            #if we are on the notch point, and we are rotating ourselves, then we rotate the next rotor too.
            if currentKey == notchPoint:
                #for this case the rotor to the right was on its notch point, and so are we, so we rotate and tell next one too.
                nextRingRotate = True
                rotor.rotate()
            elif nextRingRotate:
                #this means the rotor to the right of us was on its notch point, but we aren't so we just rotate and move on. 
                rotor.rotate()
                nextRingRotate = False
                #if the rotor is non-notch then exit
                if rotor.RotorType == RotorType.NonNotch:
                    break
            elif rotor.RotorType == RotorType.NonNotch:
                break
    
    #print the rotors to give us a better idea of the transformations
    def __printRotors(self):
        i = len(self.rotorList) -1
        while i >= 0:
            rotor = self.rotorList[i]
            print(f"[{rotor.rotorName}] ({alphabet[alphabet.index(rotor.rPins[rotor.rotorOffset])]}) ",end="")
            i -= 1
        print("")


    def encode(self, keyIn):
        keyOut = keyIn
        #self.__printRotors()
        self.__rotateRings()
        #self.__printRotors()
        rotorNum = len(self.rotorList)
        
        #right to left
        
        #set i is greater than 0, as we don't want to hit 0 on this run, to miss out the reflector
        ringOffset = 0
        #because of the way we set up our rotors, the right most rotor is the first in the list. The reflector is last. 
        for rotor in self.rotorList:
            #print(f"rotor {rotor.rotorName} -> ",end = "")
            keyOut = rotor.encodeRight(keyOut)
        #rotor number -2 so we miss out the reflector which was hit on the above encode.
        i = (rotorNum-2)
        while i >= 0:
            #print(f"rotor {self.rotorList[i].rotorName} -> ",end = "")
            keyOut = self.rotorList[i].encodeLeft(keyOut)
            i -= 1
        #left to right
        return keyOut

if __name__ == "__main__":
    pass