OPENQASM 2.0;
include "qelib1.inc";
qreg q[15];
x q[10];
z q[10];
x q[9];
z q[9];
x q[8];
x q[7];
z q[7];
x q[6];
z q[6];
x q[5];
x q[4];
z q[4];
z q[0];
h q[14];
sdg q[14];
h q[14];
sdg q[14];
cx q[14],q[13];
h q[13];
h q[12];
sdg q[12];
cx q[12],q[13];
h q[12];
cx q[14],q[12];
sdg q[12];
cx q[13],q[12];
sdg q[12];
swap q[14],q[12];
h q[11];
cx q[11],q[14];
cx q[11],q[13];
h q[11];
cx q[13],q[11];
cx q[12],q[11];
sdg q[11];
cx q[12],q[11];
sdg q[11];
cx q[11],q[14];
h q[10];
cx q[10],q[14];
cx q[10],q[11];
h q[10];
cx q[13],q[10];
cx q[12],q[10];
cx q[11],q[10];
sdg q[10];
cx q[14],q[10];
cx q[12],q[10];
cx q[11],q[10];
cx q[10],q[13];
h q[9];
sdg q[9];
cx q[9],q[13];
cx q[9],q[12];
cx q[9],q[10];
h q[9];
cx q[14],q[9];
cx q[13],q[9];
cx q[11],q[9];
sdg q[9];
cx q[14],q[9];
cx q[13],q[9];
cx q[12],q[9];
cx q[11],q[9];
cx q[10],q[9];
cx q[9],q[13];
cx q[9],q[11];
cx q[9],q[10];
h q[8];
sdg q[8];
cx q[1], q[0];
cx q[8],q[13];
cx q[8],q[11];
cx q[8],q[9];
h q[8];
cx q[13],q[8];
cx q[12],q[8];
cx q[11],q[8];
cx q[10],q[8];
cx q[9],q[8];
sdg q[8];
cx q[14],q[8];
cx q[13],q[8];
cx q[9],q[8];
sdg q[8];
cx q[8],q[14];
cx q[8],q[13];
cx q[8],q[12];
swap q[9],q[8];
h q[7];
cx q[7],q[10];
cx q[7],q[9];
cx q[7],q[8];
h q[7];
cx q[12],q[7];
cx q[11],q[7];
cx q[10],q[7];
cx q[8],q[7];
sdg q[7];
cx q[13],q[7];
cx q[12],q[7];
cx q[10],q[7];
cx q[9],q[7];
sdg q[7];
cx q[7],q[14];
cx q[7],q[12];
cx q[7],q[11];
cx q[7],q[10];
cx q[7],q[8];
h q[6];
sdg q[6];
cx q[6],q[12];
h q[6];
cx q[12],q[6];
cx q[10],q[6];
cx q[9],q[6];
cx q[8],q[6];
cx q[7],q[6];
sdg q[6];
cx q[14],q[6];
cx q[13],q[6];
cx q[12],q[6];
cx q[9],q[6];
cx q[8],q[6];
sdg q[6];
cx q[6],q[14];
cx q[6],q[13];
cx q[6],q[12];
cx q[6],q[9];
cx q[6],q[8];
swap q[7],q[6];
h q[5];
cx q[5],q[11];
cx q[5],q[10];
h q[5];
cx q[14],q[5];
cx q[12],q[5];
cx q[10],q[5];
cx q[7],q[5];
sdg q[5];
cx q[10],q[5];
cx q[6],q[5];
sdg q[5];
cx q[10],q[0];
cx q[7],q[0];
cx q[4],q[0];
cx q[3],q[0];
cx q[2],q[0];
cx q[1],q[0];
cx q[0],q[12];
cx q[0],q[11];
cx q[0],q[3];
swap q[2],q[0];
