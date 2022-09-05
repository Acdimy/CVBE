from term import *
from functools import cmp_to_key

class CVBE:
    def __init__(self, termlist=[], mode=0, bdd=None): # Assume that terms are already regularized
        self.bdd = bdd
        if mode == 0:
            self.term_list = self.deduplicate(termlist)
            self.regularized = 1
        else:
            self.term_list = termlist
            self.regularized = 0
    def deduplicate(self, termlist=[]):
        termdict = {}
        attrlist = []
        for term in termlist:
            if soundcomp(term.attr) not in termdict:
                termdict[soundcomp(term.attr)] = [term]
                attrlist.append(term.attr)
            else:
                termdict[soundcomp(term.attr)].append(term)
        for attr in attrlist:
            if len(termdict[soundcomp(attr)]) > 1:
                term_rd = Term(attr, dd_ref_or([t.ref for t in termdict[soundcomp(attr)]]), self.bdd)
                termdict[soundcomp(attr)] = term_rd
            else:
                termdict[soundcomp(attr)] = termdict[soundcomp(attr)][0]
        return list(termdict.values())
    def reduce(self):
        term_list_new = []
        for term in self.term_list:
            if term.ref != 0:
                term_list_new.append(term)
        self.term_list = term_list_new
    def regularize(self, termlist=[]):
        if termlist == []:
            termlist = self.term_list # len > 0
        ref_list = [term.ref for term in termlist]
        attr_list = [term.attr for term in termlist]
        term_num = len(termlist)
        ref_new_list, attr_new_list = [ref_list[0]], [attr_list[0]]
        for i in range(1, term_num): # curr_ref: ref_list[i]
            curr_term_num = len(ref_new_list)
            ref_shared = ref_list[i]
            for j in range(curr_term_num):
                ref_shared = ref_shared & (~ref_new_list[j])
                # if attr_list[i] + attr_new_list[j] != 0:
                if abs((attr_list[i] + attr_new_list[j]).real) + abs((attr_list[i] + attr_new_list[j]).imag) >= 0.0001:
                    ref_conj = ref_list[i] & ref_new_list[j]
                    if ref_conj != self.bdd.false:
                        ref_new_list.append(ref_conj)
                        attr_new_list.append(attr_list[i]+attr_new_list[j])
                    else:
                        ref_new_list.append(ref_new_list[j])
                        attr_new_list.append(attr_new_list[j])
                        continue
                ref_disj = ~ref_list[i] & ref_new_list[j]
                if ref_disj != self.bdd.false:
                    ref_new_list.append(ref_disj)
                    attr_new_list.append(attr_new_list[j])
            if ref_shared != self.bdd.false:
                ref_new_list.append(ref_shared)
                attr_new_list.append(attr_list[i])
            ref_new_list = ref_new_list[curr_term_num:]
            attr_new_list = attr_new_list[curr_term_num:]
            #
            term_temp_list = [Term(attr_new_list[i], ref_new_list[i], self.bdd) for i in range(len(ref_new_list))]
            term_dedup_list = self.deduplicate(term_temp_list)
            ## Order!
            ref_new_list = [term.ref for term in term_dedup_list]
            attr_new_list = [term.attr for term in term_dedup_list]
        term_new_list = [Term(round_complex(attr_new_list[i]), ref_new_list[i], self.bdd) for i in range(len(ref_new_list))] # not strong
        ### TERM MERGE!!!
        term_dedup_list = self.deduplicate(term_new_list)
        self.term_list = term_dedup_list
    def equals(self, c1, threshold=0.001):
        if len(self.term_list) != len(c1.term_list):
            print(len(self.term_list), len(c1.term_list))
            return False
        termlist0 = sorted(self.term_list, key=cmp_to_key(cmp_term))
        termlist1 = sorted(c1.term_list, key=cmp_to_key(cmp_term))
        # print([t.attr for t in termlist0])
        # print([t.attr for t in termlist1])
        res = True
        for i in range(len(termlist0)):
            attr_diff = termlist0[i].attr-termlist1[i].attr
            if abs(attr_diff.real) + abs(attr_diff.imag) >= threshold:
                print('attr_diff: ', attr_diff)
                print('attrs: ', termlist0[i].attr, termlist1[i].attr)
                res = False
            if termlist0[i].ref!=termlist1[i].ref:
                print("C0 ref: ", self.bdd.to_expr(termlist0[i].ref), "\n")
                print("C1 ref: ", self.bdd.to_expr(termlist1[i].ref))
                res = False
            if res == False:
                return res
        return res
    def tensor(self, c1):
        termlist1 = []
        for term1 in self.term_list:
            for term2 in c1.term_list:
                termlist1.append(term1.tensor(term2))
        return CVBE(termlist1, bdd=self.bdd)
    def sequential(self, c1, ex_list=[]):
        termlist1 = []
        # print(len(self.term_list), len(c1.term_list))
        for term1 in self.term_list:
            for term2 in c1.term_list:
                termlist1 += (term1.sequential(term2, ex_list))
        c0 = CVBE(termlist1, 1, self.bdd)
        # c0.regularize()
        return c0
    def substitute(self, dic):
        for term in self.term_list:
            term.substitute(dic)
    def switch(self, vars_num=0, s0=0, s1=0, s2=0, s3=0):
        # dic = {}
        # if s0 != s1:
        #     for i in range(vars_num):
        #         dic['i'+str(vars_num*(s0-1)+i)] = 'i' + str(vars_num*(s1-1)+i)
        # if s2 != s3:
        #     for i in range(vars_num):
        #         dic['i'+str(vars_num*(s2-1)+i)] = 'i' + str(vars_num*(s3-1)+i)
        # self.substitute(dic)
        if s0 == 1 and s1 == 2 and s2 == 2 and s3 == 3:
            dic = {}
            for i in range(vars_num):
                dic['i'+str(vars_num*(s2-1)+i)] = 'i' + str(vars_num*(s3-1)+i)
            self.substitute(dic)
            dic = {}
            for i in range(vars_num):
                dic['i'+str(vars_num*(s0-1)+i)] = 'i' + str(vars_num*(s1-1)+i)
            self.substitute(dic)
        else:
            dic = {}
            for i in range(vars_num):
                dic['i'+str(vars_num*(s2-1)+i)] = 'i' + str(vars_num*(s3-1)+i)
            self.substitute(dic)

def print_cvbe(cvbe):
    for term in cvbe.term_list:
        print(term.attr, term.ref)