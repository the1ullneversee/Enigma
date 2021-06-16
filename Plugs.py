#def class for PlugLeads
#plug leads will need an encoding function
#the constructor will take the combination of letters too ('AB')
from CustomExceptions import PlugException


class PlugLead():
    def __init__ (self, combination):
        if len(combination) == 2:
            #it should not be possible to connect a letter to itself. We check this after the length, as we don't want to access a list and get an index error if it's not of the correct size.
            if combination[0] != combination[1]:
                self.__combination = combination
                #create dic to match the letter to alternative letter. this will also help with quick memebership querying.
                self.__combinationDic = {combination[0] : combination[1], combination[1] : combination[0]}
            else:
                raise PlugException("It is not possible to connect a letter to itself",combination)
        else:
            raise PlugException("A Combination needs to be two characters!",combination)
    
    #returns the letter encoded as per the combination provided
    def encode(self, letter):
        if letter in self.__combinationDic:
            return self.__combinationDic[letter]
        else: 
            return letter

    #if we ever just want to get what the lead combo is
    def get(self):
        return self.__combination

    #function to help match a given letter to a set combination.
    def combinationContainLetter(self, letter):
        if not letter:
            return PlugException("Need a Letter!","")
        return letter in self.__combinationDic

    #check membership is used to check if a lead already exists
    def checkMembership(self, plugLead):
        if not plugLead:
            raise PlugException("Need a lead!","")


    #override eq operator
    def __eq__(self, other):
        if type(self) is type(other):
            return (self.__combination == other.__combination) or (self.__combination[0] in other.__combination) or (self.__combination[1] in other.__combination)
        else:
            raise NotImplementedError("Equality not supported on this type.")

    #need to override this for sets. Best practice to.
    def __hash__(self):
        return hash(self.combination)

#Plugboard not PlugBoard to fit the engima tests
class Plugboard():
    maxLeads = 10
    def __init__(self, pbInputs):
        self.__leads = []
        if len(pbInputs) > 0:
            self.configurePlugBoard(pbInputs)

    def configurePlugBoard(self, inputs):
        for plugIn in inputs:
            self.add(PlugLead(plugIn))

    #as adding a plug lead will construct a type of PlugLead, we do not need to check the value passed in as this is already done by the PlugLead Class
    #what we do need to check is if the pluglead that is being added into the board, already exists in the board, IE the plug combo contains a plug in one of the ports
    def add(self, plug):
        #plug = PlugLead(lead)
        if len(self.__leads) >= Plugboard.maxLeads:
            raise PlugException("Reached max amount of plugs.",plug)

        if not any(lead == plug for lead in self.__leads):
                self.__leads.append(plug)
        else:
            raise PlugException("Plug port already taken!",plug)
            
    
    #get leads
    def get(self):
        return self.__leads

    #print all the lead combos we have. This uses the get from the plug lead class to retrieve the store combination with is private.
    #
    def print(self):
        for plug in self.__leads:
            print(plug.get())

    #what this function does is take a letter, and check which pluglead stored contains that letter, we lean on the check membership function of the PlugLead class to make the code more readable. 
    #if membership is found, the function calls on PlugLead class to encode the letter to it's corresponding value in the combination. 
    #if no membership is found we just return the letter back. 
    #encode not Encode as we will need to fit it to the tests in the jupyter notebook.
    def encode(self, letter):
        for lead in self.__leads:
            if lead.combinationContainLetter(letter):
                return lead.encode(letter)
        
        return letter