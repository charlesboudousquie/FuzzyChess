from typing import List
from fuzzy_number import *



class Mamdani():
    """
    Class that implements a Mamdani Fuzzy System.
    """

    def __init__(self, inputs : List[List[Function]], outputs : List[Function], delta : float=0.01):
        """
        Constructs a new instance.

        :param      inputs:   List of antecedents, each is a list of Functions
        :type       inputs:   List[List[Function]]
        :param      outputs:  The consequence
        :type       outputs:  List[Function]
        :param      delta:    The delta to use for Riemann Sums
        :type       delta:    float
        """
        self.inputs = inputs  # can have multiple antecedents
        self.outputs = outputs
        self.delta = delta
        #cog:
        self.lower_bound = self.outputs[0].lower_bound
        self.upper_bound = self.outputs[0].upper_bound
        for consequence in self.outputs:
            self.lower_bound = min(self.lower_bound, consequence.lower_bound)
            self.upper_bound = max(self.upper_bound, consequence.upper_bound)

    def __call__(self, *x) -> float:
        """
        Evaluate the Mamdani Fuzzy System with the given inputs

        :param      x:    The inputs to the fuzzy system. len(x) = # antecedents
        :type       x:    list

        :returns:   The output of the Mamdani System
        :rtype:     float
        """
        firing_levels = []

        # for each rule
        for i in range(len(self.inputs[0])):

            # min the truth of each rule together
            firing_level = 1.0
            for xn, input in zip(x, self.inputs):
                val = input[i](xn)

                firing_level = min(firing_level, val)

            firing_levels.append(firing_level)

        #print(f'Firing levels: {firing_levels}')
        y = self.lower_bound
        upper_bound = self.upper_bound
        #print(f'Bounds: [{y:.4f},{upper_bound:.4f}]')
        delta = self.delta
        #print(f'delta: {delta}')
        sum_b_prime_times_y = 0.0
        sum_b_prime = 0.0
        while y <= upper_bound:
            B_prime = 0
            for firing_level, B_i in zip(firing_levels, self.outputs):
                if firing_level:
                    B_prime = max(B_prime, min(firing_level, B_i(y)))
            sum_b_prime_times_y += B_prime*y
            sum_b_prime += B_prime
            y += delta

        #if sum_b_prime == 0:
            #print('AGH!')
        return sum_b_prime_times_y / sum_b_prime if sum_b_prime else 0.0



if __name__ == '__main__':
    a1 = Triangular(2,3,4)
    a2 = Triangular(3,5,7)

    b1 = Triangular(20,25,35)
    b2 = Triangular(30,35,40)

    a = [a1, a2]
    b = [b1, b2]

    m = Mamdani([a], b)

    print(m(3.8))
