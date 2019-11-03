from typing import Callable

class Function():
    def __init__(self, f : Callable[[float],float], lower_bound : float, upper_bound : float):
        self.f = f
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def  __call__(self, x):
        return self.f(x)


class Triangular:
    def __init__(self,a,b,c):
        self.a = a
        self.b = b
        self.c = c
        self.lower_bound = a
        self.upper_bound = c

    def __call__(self, x: float) -> float:
        if x == self.b:
            return 1.0
        elif self.a < x and x < self.b:
            return float(x-self.a)/float(self.b-self.a)
        elif self.b < x and x < self.c:
            return float(self.c-x)/float(self.c-self.b)
        else:
            return 0.0

