import numpy as np
import time
# from z3 import *
import dd.cudd as _bdd

def is_diagonal(U):
    i, j = np.nonzero(U)
    return np.all(i == j)

def add_hyper_index(var_list,hyper_index):
    for var in var_list:
        if not var in hyper_index:
            hyper_index[var]=0
            
def reshape(U):
    if U.shape==(2,2):
        return U
    
    if U.shape[0]==U.shape[1]:
        split_U=np.split(U,2,1)
    else:
        split_U=np.split(U,2,0)
    split_U[0]=reshape(split_U[0])
    split_U[1]=reshape(split_U[1]) 
    return np.array([split_U])[0]            
            
def get_real_qubit_num(cir):
    """Calculate the real number of qubits of a circuit"""
    gates=cir.data
    q=0
    for k in range(len(gates)):
        q=max(q,max([qbit.index for qbit in gates[k][1]]))
    return q+1

def get_total_qubit_num(cir):
    return cir.num_qubits

def round_complex(x,n=6):
    a = round(x.real,n)
    b = round(x.imag,n)
    return a+b*(0.+1j)

def cmp_term(p, q):
    x = round_complex(p.attr, 4)
    y = round_complex(q.attr, 4)
    if x.real > y.real:
        return 1
    elif x.real == y.real:
        if x.imag > y.imag:
            return 1
        elif x.imag == y.imag:
            return 0
        else:
            return -1
    else:
        return -1

def cpx_diff(x, y, threshold=0.001):
    diff = x - y
    diff_real = abs(diff.real)
    diff_imag = abs(diff.imag)
    return diff_real + diff_imag

# def convert2cnf(exp):
#     s1 = Solver()
#     s2 = Solver()
#     s1.add(Not(exp))
#     s2.add(Not(And(s1.assertions())))
#     s2.set("core.minimize", True)

#     clauses = []
#     while sat == s1.check():
#         mdl = s1.model()
#         decls = mdl.decls()
#         core = [d() for d in decls if is_true(mdl[d])] + [Not(d()) for d in decls if is_false(mdl[d])] 
#         assert unsat == s2.check(core)
#         clause = Or([mk_not(c) for c in s2.unsat_core()])
#         clauses += [clause]
#         s1.add(clause)
#     return And(tuple(clauses))

def dd_and(reslist, bdd):
    tp_reslist = tuple(reslist)
    if len(tp_reslist) == 1:
        return bdd.add_expr(tp_reslist[0])
    else:
        res_str = ' & '.join(tp_reslist)
        return bdd.add_expr(res_str)


def dd_or(reslist, bdd):
    tp_reslist = tuple(reslist)
    if len(tp_reslist) == 1:
        return bdd.add_expr(tp_reslist[0])
    else:
        res_str = ' | '.join(tp_reslist)
        return bdd.add_expr(res_str)

def dd_ref_and(reflist):
    res_ref = reflist[0]
    if len(reflist) == 1:
        return res_ref
    else:
        for ref in reflist[1:]:
            res_ref = res_ref & ref
        return res_ref

def dd_ref_or(reflist):
    res_ref = reflist[0]
    if len(reflist) == 1:
        return res_ref
    else:
        for ref in reflist[1:]:
            res_ref = res_ref | ref
        return res_ref

def soundcomp(comp):
    r = comp.real if comp.real != 0 else 0
    i = comp.imag if comp.imag != 0 else 0
    return 'r' + '%.4f'%r + 'i' + '%.4f'%i
