from tools import *

class Term:
    def __init__(self, attr=0.+0.j, ref=None):
        self.attr = attr
        self.ref = ref
    def tensor(self, t1=None):
        attr1 = self.attr * t1.attr
        ref1 = And(self.ref, t1.ref)
        return Term(attr1, ref1)
    def exist(self, ex_var, boolref):
        exp_exist = Then('qe','simplify')(Exists([ex_var], boolref)).as_expr()
        exp_forall = Then('qe','simplify')(ForAll([ex_var], boolref)).as_expr()
        res = []
        solver = Solver()
        solver.add(exp_exist)
        if solver.check() == z3.sat:
            res.append(exp_exist)
        solver = Solver()
        solver.add(exp_forall)
        if solver.check() == z3.sat:
            res.append(exp_forall)
        return res
    def sequential(self, t1=None, ex_list=[]): # ex_list: vars
        attr1 = self.attr * t1.attr
        ref_0 = And(self.ref, t1.ref)
        res_refs = [ref_0]
        for ex_var in ex_list:
            new_res_refs = []
            for curr_ref in res_refs:
                new_res_refs += self.exist(ex_var, curr_ref)
            res_refs = new_res_refs
        res_terms = [Term(attr1, ref_i) for ref_i in res_refs] # Here simplify
        return res_terms
    def simplify(self):
        ref_new = simplify(self.ref)
        self.ref = ref_new
    def equalattr(self, t1=None):
        return self.attr == t1.attr
    def is_neg(self):
        solver = Solver()
        solver.add(self.ref)
        if solver.check() == z3.sat:
            return False
        return True
    def toCNF(self):
        self.ref = convert2cnf(self.ref)

def genRef(r, c, input_qubits, var_list, tt_input_num, q, curr_output):
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
            reslist.append(Not(var_list[q[i]+bias_in*tt_input_num]))
    for i,e in enumerate(output_vars):
        if e == '1':
            reslist.append(var_list[q[i]+bias_out*tt_input_num])
        else:
            reslist.append(Not(var_list[q[i]+bias_out*tt_input_num]))
    return And(tuple(reslist))