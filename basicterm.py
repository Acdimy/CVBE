import numpy as np
from z3 import *

class Term:
    def __init__(self, attr=0.+0.j, ref=None):
        self.attr = attr
        self.ref = ref
    def equalattr(self, t1=None):
        return self.attr == t1.attr
    def equalref(self, t1=None):
        # check ref equivalence
        return False
    def contra(self, t1=None):
        # check conrtradictoriness
        return False
    def shrink(self):
        # simplify ref
        pass
    def reduce(self, t1=None):
        if self.equalref(t1):
            return Term(self.attr+t1.attr, self.ref)
        elif self.contra(t1) and self.equalattr(t1):
            pass
        pass

class CVBE:
    def __init__(self, termlist=[]):
        self.termlist = termlist
    def regularize(self):
        pass