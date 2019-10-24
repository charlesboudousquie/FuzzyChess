from typing import Tuple,List,Callable


class Function():
    def __init__(self, f : Callable[[float],float], lower_bound : float, upper_bound : float):
        self.f = f
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def  __call__(self, x):
        return self.f(x)



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

def Triangular(a,b,c):
    return lambda x: (x-a)/(b-a) if a<x and x<=b else (c-x)/(c-b) if b<x and x<=c else 0


if __name__ == '__main__':
    a1 = Triangular(2,3,4)
    a2 = Triangular(3,5,7)

    b1 = Triangular(20,25,35)
    b2 = Triangular(30,35,40)

    inputs = [Function(a1,2,4), Function(a2,3,7)]
    outputs = [Function(b1,20,35), Function(b2,30,40)]

    m = Mamdani(inputs, outputs)

    print(m(3.8))
