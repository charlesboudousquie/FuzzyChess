from typing import List
from fuzzy_number import *



class Mamdani():
    def __init__(self, inputs : List[Function], outputs : List[Function], delta : float=0.01):
        self.inputs = inputs
        self.outputs = outputs
        self.delta = delta

    def __call__(self, x) -> float:
        # calculate firing levels:
        firing_levels = []
        for A_i in inputs:
            firing_levels.append(A_i(x))

        #cog:
        y = self.outputs[0].lower_bound
        upper_bound = self.outputs[-1].upper_bound
        delta = self.delta
        sum_b_prime_times_y = 0.0
        sum_b_prime = 0.0
        while y < upper_bound:
            B_prime = 0
            for firing_level, B_i in zip(firing_levels,outputs):
                B_prime = max(B_prime, min(firing_level, B_i(y)))
            sum_b_prime_times_y += B_prime*y
            sum_b_prime += B_prime
            y += delta

        return sum_b_prime_times_y / sum_b_prime



if __name__ == '__main__':
    a1 = Triangular(2,3,4)
    a2 = Triangular(3,5,7)

    b1 = Triangular(20,25,35)
    b2 = Triangular(30,35,40)

    inputs = [a1, a2]
    outputs = [b1, b2]

    m = Mamdani(inputs, outputs)

    print(m(3.8))
