from calculus import Lambda, Identifier, Literal, Apply, LetRec
import scope

class Native(object):
    def __init__(self, fn, arity):
        self.fn = fn
        self.arity = arity

def substitute(node, bind, value):
    if isinstance(node, Identifier) and node.name == bind:
        return value
    if isinstance(node, Apply):
        return Apply(
            substitute(node.fun, bind, value),
            substitute(node.arg, bind, value),
        )
    if isinstance(node, Lambda) and node.bind != bind:
        return Lambda(node.bind,
            substitute(node.body, bind, value)
        )
    if isinstance(node, LetRec) and node.bind != bind:
        return LetRec(node.bind,
            substitute(node.defn, bind, value),
            substitute(node.body, bind, value),
        )
    return node

def get_native_call(node, args, env):
    if isinstance(node, Apply):
        return get_native_call(node.fun, (node.arg,) + args, env)
    if isinstance(node, Identifier):
        layer = env.unroll(node.name)
        if layer is None:
            return None
        nat = layer[node.name]
        if isinstance(nat, Native) and len(args) == nat.arity:
            return (nat, node) + args

def get_lambda(node, env):
    if isinstance(node, Identifier):
        layer = env.unroll(node.name)
        if layer is None:
            return None
        node = layer[node.name]
    if isinstance(node, Lambda):
        return node

def step(node, env):
    if isinstance(node, Identifier):
        return node
    if isinstance(node, Literal):
        return node
    if isinstance(node, Apply):
        fun = step(node.fun, env)
        lam = get_lambda(fun, env)
        if lam is not None:
            return substitute(lam.body, lam.bind, node.arg)
        nat = get_native_call(fun, (node.arg,), env)
        if nat is None:
            return node
        else:
            res = nat[0].fn(env, *nat[1:])
            return node if res is None else res
    if isinstance(node, LetRec):
        x = env.extend({node.bind: node.defn})
        res = step(node.body, x)
        if isinstance(res, (Identifier, Literal)):
            return res
        elif res != node.body:
            return LetRec(node.bind, node.defn, res)
        else:
            return node
    if isinstance(node, Lambda):
        return node
    raise Exception(node.__class__.__name__)

import operator

def mk_operator(op):
    def do(env, node, _a, _b):
        a = step(_a, env)
        b = step(_b, env)
        if isinstance(a, Literal) and isinstance(b, Literal):
            return Literal(None, str(op(int(a.value), int(b.value))))
        if _a != a or _b != b:
            return Apply(Apply(node, a), b)
    return do

def do_if(env, node, _cond, _then, _else):
    cond = step(_cond, env)
    if isinstance(cond, Literal):
        if cond.value == 'True':
            return _then
        if cond.value == 'False':
            return _else
    if cond != _cond:
        return Apply(Apply(Apply(node, cond), _then), _else)

if __name__=='__main__':

    system_env = scope.empty()
    system_env.update({
        '-': Native(mk_operator(operator.sub), 2),
        '*': Native(mk_operator(operator.mul), 2),
        '<=': Native(mk_operator(operator.le), 2),
        '?': Native(do_if, 3),
    })

    import read, write, sys, os
    for name in os.listdir('examples'):
        path = os.path.join('examples', name)
        if name.startswith('.'):
            continue
        print 'reading %s' % path
        mapping = {'Integer': None}
        program = read.file(path, mapping)
        print 'checking %s' % path
        write.debug(program)
        last_program = None
        print 'stepping %s' % path
        while last_program != program:
            last_program = program
            program = step(program, system_env)
            write.expr(sys.stdout, program)
        print 'checking result validity %s' % path
        write.debug(program)
