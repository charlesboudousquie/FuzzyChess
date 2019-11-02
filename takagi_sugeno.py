"""
    Implementation of Takagi-Sugeno fuzzy systems
    MAT 362 A - Professor Bede
"""

import fuzzy_number as fn

class Consequence:
    # Consequence part for the fuzzy system
    def __init__(self, line):
        self.line = line

    # inputs must be a list type of size len(constants)-1
    def __call__(self, inputs):
        result = 0
        
        # for multiple antecedents
        for x, a in zip(inputs, self.line):
            result += x * a
            print(result)
        
        result += self.line[-1]
        print("consequence:", result)
        return result


class Rule:
    # class to store the fuzzy rule
    def __init__(self, a, c):
        self.antecedents = a
        self.consequence = c

    def __call__(self, crisp):
        # call antecedent with crisp to get firing level
        alpha = self.firing_levels(crisp)
        indiv = self.consequence(crisp)
        print("individual output:", indiv)
        result = (alpha, indiv)
        return result

    def firing_levels(self, crisp):
        results = [a(c) for a,c in zip(self.antecedents, crisp)]
        result = min(results)
        print("alpha:", result)
        return result


class TakagiSugeno:
    def __init__(self, rules):
        # init the rules
        self.rules = rules

    def evaluate(self, crisp):
        alphas = []
        outputs = []

        for rule in self.rules:
            a, o = rule(crisp)
            alphas.append(a)
            outputs.append(o)

        result = self.weighted_average(alphas, outputs)
        return result

    def __call__(self, *crisp):
        return(self.evaluate(crisp))

    def weighted_average(self, alpha, outputs):
        result = 0

        num = 0
        denom = sum(alpha)
       
        print("alphas:", alpha)

        for i, j in zip(alpha, outputs):
            num += i * j

        result = num / denom

        return result

# Test function to debug TS system
if __name__ == '__main__':
    tri = fn.Triangular(1, 3, 5)
    a = []
    a.append(tri)
    tri2 = fn.Triangular(3, 6, 9)
    a.append(tri2)
    c = Consequence([3, 6, 5])
    r = Rule(a, c)
    a2 = []
    tri3 = fn.Triangular(5, 10, 15)
    a2.append(tri3)
    tri4 = fn.Triangular(10, 15, 20)
    a2.append(tri4)
    c2 = Consequence([2, 4, 5])
    r2 = Rule(a2, c2)
    system = TakagiSugeno([r, r2])
    crisp = [4.5, 3.5]
    value = system.evaluate(crisp)
    print(value)

