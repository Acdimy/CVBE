import aiger
import tempfile
from pathlib import Path
from subprocess import PIPE, call

SIMPLIFY_TEMPLATE = 'read {0}; dc2; dc2; dc2; fraig; write_aiger -s {0}'


def simplify(circ, verbose=False, abc_cmd='abc', aigtoaig_cmd='aigtoaig'):
    circ = aiger.to_aig(circ)

    # avoids confusion and guarantees deletion on exit
    with tempfile.TemporaryDirectory() as tmpdirname:
        tmpdir = Path(tmpdirname)
        aag_path = tmpdir / 'input.aag'
        aig_path = tmpdir / 'input.aig'

        circ.write(aag_path)
        call([aigtoaig_cmd, aag_path, aig_path])
        command = [
            abc_cmd,
            '-c',
            SIMPLIFY_TEMPLATE.format(aig_path)
        ]
        call(command) if verbose else call(command, stdout=PIPE)
        print(command)
        call([aigtoaig_cmd, aig_path, aag_path])
        print([aigtoaig_cmd, aig_path, aag_path])
        with open(aag_path) as f:
            print(f.readlines())
        return aiger.parser.load(aag_path)

# x = aiger.atom('x')

# f = x ^ x
# print(f.aig)

# f2 = simplify(f)
# print(f2.aig)



circ1 = aiger.load('circ1.aag')
circ2 = aiger.load('circ2.aag')
print(circ1.aig)
print(circ2.aig)
circ3 = circ1 | circ2
print(circ3.aig)

# f2 = simplify(t, abc_cmd='abc', aigtoaig_cmd='aigtoaig')
# print(f2.aig)
