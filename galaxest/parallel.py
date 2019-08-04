import enum

class ParallelType(enum.Enum): 
    AMOUNT = 0
    OS = 1
    DEVICE_ID = 2

class ParallelExecution(object):

    def __init__(self, new_type, new_specs):
        self.type_val = None
        self.specs = None
        self.specs_amount = 0
        self.set_parallel_type(new_type)
        self.parse_specs(new_specs)

    def set_parallel_type(self, val):
        self.type_val = val
    
    def remove_spec(self, spec):
        if spec in self.specs:
            self.specs.remove(spec)

    def parse_specs(self, val):
        self.specs = []
        self.specs_amount = 1
        if self.type_val == ParallelType.AMOUNT :
            self.specs_amount = int(val)
        else :
            self.specs = val.split(",")
            self.specs_amount = int(len(self.specs))

