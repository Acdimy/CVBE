from cvbe import *
from qiskit import QuantumCircuit
from qiskit.quantum_info.operators import Operator
from qiskit import *

def init_cir(circ):
    qubits_num = get_total_qubit_num(circ)
    vars_num = qubits_num
    var_list = []
    for i in range(3*vars_num):
        var_list.append(Bool(str(i)))
    gates = circ.data
    gates_layer_list = [[]]
    head_ptr = [0]*qubits_num
    curr_head = 0
    for k in range(len(gates)):
        g = gates[k]
        q = [q.index for q in g[1]]
        if len(q) == 1:
            head_ptr[q[0]] += 1
        else:
            head_ptr[q[0]] = head_ptr[q[1]] = max(head_ptr[q[0]], head_ptr[q[1]]) + 1
        if head_ptr[q[0]] > curr_head:
            gates_layer_list.append([g])
            curr_head += 1
        else:
            gates_layer_list[head_ptr[q[0]]].append(g)
    return gates_layer_list,vars_num,var_list

def gen_cvbe_from_layer(gates_list, vars_num, var_list, curr_output):
    circ_cvbe = None
    uninvolved_q = [1]*vars_num
    bias_out = 2 if curr_output == 1 else 1
    for g in gates_list:
        nam = g[0].name
        q = [q.index for q in g[1]]
        if nam == 'cx': # ***
            tmp = q[0]
            q[0] = q[1]
            q[1] = tmp
        for idx in q:
            uninvolved_q[idx] = 0
        U = Operator(g[0]).data
        termlist = []
        for r in range(U.shape[0]):
            for c in range(U.shape[1]):
                if U[r][c] != 0:
                    ref = genRef(r,c,len(q), var_list, vars_num, q, curr_output)
                    termlist.append(Term(U[r][c], ref))
        cvbe = CVBE(termlist)
        if circ_cvbe == None:
            circ_cvbe = cvbe
        else:
            circ_cvbe = circ_cvbe.tensor(cvbe)
    identity_list = []
    for i in range(len(uninvolved_q)):
        if uninvolved_q[i] != 0:
            var_in = var_list[curr_output*vars_num+i]
            var_out = var_list[bias_out*vars_num+i]
            identity_list.append(var_in==var_out)
    if len(identity_list) != 0:
        identity_cvbe = CVBE([Term(1, And(tuple(identity_list)))])
        if circ_cvbe == None:
            circ_cvbe = identity_cvbe
        else:
            circ_cvbe = circ_cvbe.tensor(identity_cvbe)
    return circ_cvbe

std_layer = 1
def gen_cvbe(circ):
    gates_layer_list,vars_num,var_list = init_cir(circ)
    if len(gates_layer_list) % 2 != std_layer:
        gates_layer_list.append([])
    curr_output = 0
    circ_cvbe = None
    for ii,layer in enumerate(gates_layer_list[1:]):
        print(ii, 'layer')
        if ii != 0:
            print(len(circ_cvbe.term_list))
#             circ_cvbe.toCNF()
            circ_cvbe.regularize()
            circ_cvbe.toCNF()
        cvbe = gen_cvbe_from_layer(layer, vars_num, var_list, curr_output)
        cvbe.simplify()
        internal_vars = var_list[curr_output*vars_num:(curr_output+1)*vars_num]
        curr_output = 2 if curr_output == 1 else 1
        if circ_cvbe == None:
            circ_cvbe = cvbe
        else:
            circ_cvbe = circ_cvbe.sequential(cvbe, internal_vars)
        circ_cvbe.toCNF()
#     circ_cvbe.toCNF()
    return circ_cvbe

if __name__ == '__main__':
    path = '../benchmark/'
    name1 = 'qft_10.qasm'
    # name2 = 'RandomClifford_q10_0_1.qasm'
    circ0 = QuantumCircuit().from_qasm_file(path+name1)
    # circ1 = QuantumCircuit().from_qasm_file(path+name2)
    cvbe0_time_1 = time.time()
    cvbe0 = gen_cvbe(circ0)
    cvbe0.regularize()
    cvbe0.toCNF()
    cvbe0_time_2 = time.time()
    cvbe1_time_1 = time.time()
    # cvbe1 = gen_cvbe(circ1)
    # cvbe1.regularize()
    # cvbe1.toCNF()
    # cvbe1_time_2 = time.time()

    # equal_time1 = time.time()
    # res = cvbe0.equals(cvbe1)
    # equal_time2 = time.time()
    # print(res)
    # print("C1 construction: %.6f"%(cvbe0_time_2-cvbe0_time_1))
    # print("C2 construction: %.6f"%(cvbe1_time_2-cvbe1_time_1))
    # print("Equivalence checking time: %.6f"%(equal_time2-equal_time1))
