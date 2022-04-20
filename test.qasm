OPENQASM 2.0;
include "qelib1.inc";
qreg q[5];

//constant
x q[4];

h q[4];
cx q[3], q[4]; tdg q[4];
cx q[0], q[4]; t q[4];
