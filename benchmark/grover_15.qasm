OPENQASM 2.0;
include "qelib1.inc";
qreg q[15];
h q[0];
h q[1];
h q[2];
h q[3];
h q[4];
h q[5];
h q[6];
h q[7];
h q[14];
ccx q[0],q[1],q[8];
ccx q[2],q[8],q[9];
ccx q[3],q[9],q[10];
ccx q[4],q[10],q[11];
ccx q[5],q[11],q[12];
ccx q[6],q[12],q[13];
ccx q[7],q[13],q[14];
ccx q[6],q[12],q[13];
ccx q[5],q[11],q[12];
ccx q[4],q[10],q[11];
ccx q[3],q[9],q[10];
ccx q[2],q[8],q[9];
ccx q[0],q[1],q[8];
h q[0];
h q[1];
h q[2];
h q[3];
h q[4];
h q[5];
h q[6];
h q[7];
x q[0];
x q[1];
x q[2];
x q[3];
x q[4];
x q[5];
x q[6];
x q[7];
h q[7];
ccx q[0],q[1],q[8];
ccx q[2],q[8],q[9];
ccx q[3],q[9],q[10];
ccx q[4],q[10],q[11];
ccx q[5],q[11],q[12];
ccx q[6],q[12],q[7];
ccx q[5],q[11],q[12];
ccx q[4],q[10],q[11];
ccx q[3],q[9],q[10];
ccx q[2],q[8],q[9];
ccx q[0],q[1],q[8];
h q[7];
x q[0];
x q[1];
x q[2];
x q[3];
x q[4];
x q[5];
x q[6];
x q[7];
h q[0];
h q[1];
h q[2];
h q[3];
h q[4];
h q[5];
h q[6];
h q[7];
h q[14];
