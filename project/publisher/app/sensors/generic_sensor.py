import random


class GenericSensor:
    def __init__(self, boundaries):
        self.min_value, self.max_value = boundaries
        
    def read(self):
        return random.uniform(self.min_value, self.max_value)
        
    
    