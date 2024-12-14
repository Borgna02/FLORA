import random


class GenericSensor:
    def __init__(self, boundaries, thresholds):
        self.min_value, self.max_value = boundaries
        self.min_threshold, self.max_threshold = thresholds
        
    def read(self):
        if random.random() < 0.99: # generate random below threshold with probability 0.9
            return random.uniform(self.min_threshold, self.max_threshold)
        # generate random above threshold with probability 0.1
        if random.random() < 0.5:
            return random.uniform(self.min_value, self.min_threshold)
        return random.uniform(self.max_threshold, self.max_value)
        
    
    