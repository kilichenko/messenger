class MyFirstClass:
    #class variable
    var = 12

    def __init__(self, state = 1):
        #instance variable
        self.state = state
        self.pVar = 0

    def SetPVar(self, pVar):
        self.pVar = pVar

    @classmethod
    def SetVar(cls, x):
        cls.var = x

    @staticmethod
    def Doer():
        print("I'm static!")


var = 10
print(var)
var = 'gfdg'
print(var)


