OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];
x q[2];
z q[2];
x q[0];
h q[2];
sdg q[2];
h q[2];
h q[2];
h q[1];
cx q[1],q[2];
h q[0];
h q[1];
cx q[0], q[1];
h q[0];
h q[1];
h q[1];
swap q[2],q[1];
h q[2];
h q[0];
sdg q[0];
cx q[0],q[1];
h q[0];
sdg q[0];
cx q[2],q[0];
cx q[1],q[0];
sdg q[0];
swap q[2],q[0];
