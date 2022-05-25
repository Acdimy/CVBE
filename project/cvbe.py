from term import *
from functools import cmp_to_key

class CVBE:
    def __init__(self, termlist=[], mode=0): # Assume that terms are already regularized
        if mode == 0:
            self.term_list = self.deduplicate(termlist)
            self.regularized = 1
        else:
            self.term_list = termlist
            self.regularized = 0
    def deduplicate(self, termlist=[]):
        termdict = {}
        for term in termlist:
            if term.attr not in termdict:
                termdict[term.attr] = [term]
            else:
                termdict[term.attr].append(term)
        for attr in termdict:
            if len(termdict[attr]) > 1:
                term_rd = Term(attr, Or(tuple([t.ref for t in termdict[attr]])))
                termdict[attr] = term_rd
            else:
                termdict[attr] = termdict[attr][0]
        return list(termdict.values())
    def reduce(self):
        term_list_new = []
        for term in self.term_list:
            if not term.is_neg():
                term_list_new.append(term)
        self.term_list = term_list_new
    def simplify(self):
        for term in self.term_list:
            term.simplify()
    def regularize(self, termlist=[]):
        if termlist == []:
            termlist = self.term_list # len > 0
        ref_list = [term.ref for term in termlist]
        attr_list = [term.attr for term in termlist]
        term_num = len(termlist)
        ref_new_list, attr_new_list = [ref_list[0]], [attr_list[0]]
        for i in range(1, term_num): # curr_ref: ref_list[i]
            ref_new = ref_list[i]
            curr_term_num = len(ref_new_list)
            s1 = Solver()
            s1.add(ref_list[i])
            for j in range(curr_term_num):
                s1.add(Not(ref_new_list[j]))
                ref_new = And(ref_new, Not(ref_new_list[j]))
                if attr_list[i] + attr_new_list[j] != 0:
                    s2 = Solver()
                    s2.add(ref_list[i])
                    s2.add(ref_new_list[j])
                    if s2.check() == z3.sat:
                        ref_new_list.append(And(ref_list[i], ref_new_list[j]))
                        attr_new_list.append(attr_list[i]+attr_new_list[j])
                    else:
                        ref_new_list.append(ref_new_list[j])
                        attr_new_list.append(attr_new_list[j])
                        continue
                s2 = Solver()
                s2.add(Not(ref_list[i]))
                s2.add(ref_new_list[j])
                if s2.check() == z3.sat:
                    ref_new_list.append(And(Not(ref_list[i]), ref_new_list[j]))
                    attr_new_list.append(attr_new_list[j])
            if s1.check() == z3.sat:
                ref_new_list.append(ref_new)
                attr_new_list.append(attr_list[i])
            ref_new_list = ref_new_list[curr_term_num:]
            attr_new_list = attr_new_list[curr_term_num:]
            #
            term_temp_list = [Term(attr_new_list[i], ref_new_list[i]) for i in range(len(ref_new_list))]
            term_dedup_list = self.deduplicate(term_temp_list)
            ## Order!
            ref_new_list = [term.ref for term in term_dedup_list]
            attr_new_list = [term.attr for term in term_dedup_list]
        term_new_list = [Term(round_complex(attr_new_list[i]), ref_new_list[i]) for i in range(len(ref_new_list))] # not strong
        ### TERM MERGE!!!
        term_dedup_list = self.deduplicate(term_new_list)
        self.term_list = term_dedup_list
    def equals(self, c1, threshold=0.001):
        if len(self.term_list) != len(c1.term_list):
            print(len(self.term_list), len(c1.term_list))
            return False
        length = len(self.term_list)
        termlist0 = sorted(self.term_list, key=cmp_to_key(cmp_term))
        termlist1 = sorted(c1.term_list, key=cmp_to_key(cmp_term))
        # print([term.attr for term in termlist0])
        # print([term.attr for term in termlist1])
        res = True
        for i in range(len(termlist0)):
            attr_diff = termlist0[i].attr-termlist1[i].attr
            if abs(attr_diff.real) + abs(attr_diff.imag) >= threshold:
                print('attr_diff: ', attr_diff)
                res = False
            solver = Solver()
            solver.add(termlist0[i].ref!=termlist1[i].ref)
            if solver.check() == z3.sat:
                print(termlist0[i])
                print(termlist1[i])
                print(solver.model())
                res = False
            if res == False:
                return res
        return res
    def tensor(self, c1):
        termlist1 = []
        for term1 in self.term_list:
            for term2 in c1.term_list:
                termlist1.append(term1.tensor(term2))
        return CVBE(termlist1)
    def sequential(self, c1, ex_list=[]):
        termlist1 = []
        for term1 in self.term_list:
            for term2 in c1.term_list:
                termlist1 += (term1.sequential(term2, ex_list))
        c0 = CVBE(termlist1, 1)
#         c0.regularize()
        c0.simplify()
        return c0
    def toCNF(self):
        for i in range(len(self.term_list)):
            self.term_list[i].toCNF()

def print_cvbe(cvbe):
    for term in cvbe.term_list:
        print(term.attr, term.ref)