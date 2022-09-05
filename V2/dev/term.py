from tools import *

class Term:
    def __init__(self, attr=0.+0.j, ref=None, bdd=None):
        self.attr = attr
        self.ref = ref
        self.bdd = bdd
    def tensor(self, t1=None):
        attr1 = self.attr * t1.attr
        ref1 = self.ref & t1.ref
        return Term(attr1, ref1, self.bdd)
    def cofactor(self, ex_var, boolref):
        res = []
        cof_0 = self.bdd.let({ex_var:False}, boolref)
        if cof_0 != self.bdd.false:
            res.append(cof_0)
        cof_1 = self.bdd.let({ex_var:True}, boolref)
        if cof_1 != self.bdd.false:
            res.append(cof_1)
        return res
    def exist(self, ex_var, boolref):
        res = []
        cof_0 = self.bdd.exist([ex_var], boolref)
        if cof_0 != self.bdd.false:
            res.append(cof_0)
        cof_1 = self.bdd.forall([ex_var], boolref)
        if cof_1 != self.bdd.false:
            res.append(cof_1)
        return res
    def sequential(self, t1=None, ex_list=[]): # ex_list: vars
        attr1 = self.attr * t1.attr
        ref_0 = self.ref & t1.ref
        res_refs = [ref_0]
        for ex_var in ex_list:
            new_res_refs = []
            for curr_ref in res_refs:
                new_res_refs += self.exist(ex_var, curr_ref)
            res_refs = new_res_refs
        res_terms = [Term(attr1, ref_i, self.bdd) for ref_i in res_refs] # Here simplify
        return res_terms
    def substitute(self, dic):
        self.ref = self.bdd.let(dic, self.ref)
    def equalattr(self, t1=None):
        return self.attr == t1.attr


def genRef(r, c, input_qubits, var_list, tt_input_num, q, curr_output, bdd):
    bias_in = curr_output
    bias_out = 2 if curr_output == 1 else 1
    input_vars = bin(r)[2:]
    if len(input_vars) < input_qubits:
        input_vars = '0'*(input_qubits-len(input_vars)) + input_vars
    output_vars = bin(c)[2:]
    if len(output_vars) < input_qubits:
        output_vars = '0'*(input_qubits-len(output_vars)) + output_vars
    reslist = []
    for i,e in enumerate(input_vars):
        if e == '1':
            reslist.append(var_list[q[i]+bias_in*tt_input_num])
        else:
            reslist.append('~'+var_list[q[i]+bias_in*tt_input_num])
    for i,e in enumerate(output_vars):
        if e == '1':
            reslist.append(var_list[q[i]+bias_out*tt_input_num])
        else:
            reslist.append('~'+var_list[q[i]+bias_out*tt_input_num])
    return dd_and(reslist, bdd)
