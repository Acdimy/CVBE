OPENQASM 2.0;
include "qelib1.inc";
qreg q[4];

sdg q[0];
h q[2];
cx q[0],q[3];
cx q[2],q[1];
cx q[1],q[3];
cx q[2],q[0];
t q[0];
t q[1];
tdg q[2];
tdg q[3];
cx q[1],q[3];
cx q[0],q[2];
cx q[0],q[1];
cx q[2],q[3];