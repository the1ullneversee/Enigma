
class EnigmaException(BaseException):
    def __init__(self, message):
        self.__message = message
    
    def GetMessage(self):
        return self.__message

class ConfigurationException(EnigmaException):
    def __init__(self, configurationIssue, val):
        super().__init__(configurationIssue)
        self.value = val

class PlugException(EnigmaException):
    def __init__(self, plugIssue, val):
        super().__init__(plugIssue)
        self.value = val
        
    def GetExceptionValue(self):
        return self.value
    
    