from enum import Enum

class Protocol(Enum):
    
    EWL = "EWL quantization protocol"
    MW = "MW quantization protocol"
    
    def describe(self):
        # self is the member here
        return self.name, self.value