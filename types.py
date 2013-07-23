class Variable(object):
    def __init__(self):
        self.instance = None

class Type(object):
    def __init__(self, name, types):
        self.name = name
        self.types = types

class Generic(object):
    def __init__(self, kind):
        self.kind = kind

def prune(t):
    while isinstance(t, Variable) and t.instance:
        t = t.instance
    return t

def inside(v, t):
    if isinstance(t, Type):
        return any(inside(v, x) for x in t.types)
    return v == t

def fresh(t, mappings=None):
    mappings = {} if mappings is None else mappings
    t = prune(t) 
    if isinstance(t, Generic):
        if t.kind not in mappings:
            mappings[t.kind] = Variable()
        return mappings[t.kind]
    if isinstance(t, Variable):
        return t
    if isinstance(t, Type):
        return Type(t.name, [fresh(x, mappings) for x in t.types])

def unify_var(v, t):
    if v != t:
        if inside(v, t):
            raise Exception("recursive unification")
        v.instance = t

def unify_types(a, b):
    if a.name != b.name or len(a.types) != len(b.types):
        raise Exception("type mismatch %s/%i != %s/%i" % (a.name, len(a.types), b.name, len(b.types))
    for p, q in zip(a.types, b.types):
        unify(p, q)

def unify(a, b):
    a = prune(a)
    b = prune(b)
    if isinstance(a, Variable):
        unify_var(a, b)
    if isinstance(b, Variable):
        unify_var(b, a)
    if isinstance(a, Type) and isinstance(b, Type):
        unify_types(a, b)

###Integer = op('Integer', [])
###Boolean = op('Boolean', [])
