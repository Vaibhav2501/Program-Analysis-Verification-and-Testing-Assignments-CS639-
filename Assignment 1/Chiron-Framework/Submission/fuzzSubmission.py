from kast import kachuaAST
import sys
from z3 import *
sys.path.insert(0, "KachuaCore/interfaces/")
from interfaces.fuzzerInterface import *
sys.path.insert(0, '../KachuaCore/')
import random

# Each input is of this type.
# class InputObject():
#    def __init__(self, data):
#        self.id = str(uuid.uuid4())
#        self.data = data
#        # Flag to check if ever picked
#        # for mutation or not.
#        self.pickedOnce = False
        
class CustomCoverageMetric(CoverageMetricBase):
    # Statements covered is used for
    # coverage information.
    def __init__(self):
        super().__init__()

    # TODO : Implement this
    def compareCoverage(self, curr_metric, total_metric):
        # must compare curr_metric and total_metric
        # True if Improved Coverage else False
        # return False  
        return all(curr_metric != temp_metric for temp_metric in total_metric if len(temp_metric) == len(curr_metric))
 

    # TODO : Implement this
    def updateTotalCoverage(self, curr_metric, total_metric):
        # Compute the total_metric coverage and return it (list)
        # this changes if new coverage is seen for a
        # given input.
        # return total_metric
        
        if self.compareCoverage(curr_metric,total_metric):
            total_metric.append(curr_metric)
            return total_metric

class CustomMutator(MutatorBase):
    def __init__(self):
        pass

    # TODO : Implement this
    def mutate(self, input_data, coverageInfo, irList):
        # Mutate the input data and return it
        # coverageInfo is of type CoverageMetricBase
        # Don't mutate coverageInfo
        # irList : List of IR Statments (Don't Modify)
        # input_data.data -> type dict() with {key : variable(str), value : int}
        # must return input_data after mutation.

        data_dict = input_data.data.copy()
        print('Value of Input:- ',data_dict)
        values_list = list(data_dict.values())
    
        for key, value in data_dict.items():
            random_integer = random.randint(1, 5)
            random_item = random.choice(values_list)
            data_dict[key] = ((random_item*random_integer) +1) & 63

        input_data.data = data_dict

        return input_data
        

# Reuse code and imports from
# earlier submissions (if any).
