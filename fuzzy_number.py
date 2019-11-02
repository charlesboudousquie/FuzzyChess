from typing import Callable

class Function():
    def __init__(self, f : Callable[[float],float], lower_bound : float, upper_bound : float):
        self.f = f
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def  __call__(self, x):
        return self.f(x)


def Triangular(a,b,c):
    return Function(lambda x: 1 if x==b else (x-a)/(b-a) if a<x and x<=b else (c-x)/(c-b) if b<x and x<=c else 0,a,c)
