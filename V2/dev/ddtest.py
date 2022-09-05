import dd.autoref as _bdd

bdd = _bdd.BDD()
bdd.declare('x1')
bdd.declare('x2')
bdd.declare('x3')

# u = bdd.add_expr(r'x1 /\ x2')  # conjunction
# v = bdd.add_expr(r'x3 \/ ~ x2')  # disjunction and negation

u = bdd.add_expr('x1 & x2')  # conjunction
v = bdd.add_expr('x3 | ! x2')  # disjunction and negation

# And
w1 = u & ~v

# Or
w2 = u | ~v

# Cofactor
# values = dict(x1=True)
w3 = bdd.let({'x1':True}, w2)

# Equiv
print(w3 != bdd.false)
