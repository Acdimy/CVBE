OPENQASM 2.0;
include "qelib1.inc";
qreg q[5];
x q[4];
z q[4];
x q[1];
x q[0];
z q[0];
sdg q[4];
h q[3];
sdg q[3];
h q[3];
cx q[4],q[3];
sdg q[3];
swap q[4],q[3];
h q[2];
sdg q[2];
cx q[2],q[3];
h q[2];
cx q[4],q[2];
cx q[1], q[0];
cx q[3],q[2];
sdg q[2];
cx q[3],q[2];
sdg q[2];
swap q[3],q[2];
h q[1];
cx q[1],q[4];
h q[1];
sdg q[1];
h q[0];
sdg q[0];
cx q[0],q[3];
h q[0];
cx q[3],q[0];
cx q[1],q[0];
sdg q[0];
cx q[2],q[0];
cx q[1],q[0];
sdg q[0];
cx q[0],q[4];
swap q[3],q[0];
