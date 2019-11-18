from enum import Enum

class Protocol(Enum):
    """
    The various different quantum/classical game theory game protocols 
    """
    EWL = "EWL quantization protocol"
    MW = "MW quantization protocol"
    Classical = "Classical protocol"
    
    def describe(self):
        # self is the member here
        return self.name, self.value