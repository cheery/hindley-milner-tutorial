from types import Variable, Type, Generic, fresh, prune, unify
from calculus import Lambda, Identifier, Literal, Apply, LetRec

def analyse(node, env):
    if isinstance(node, Identifier):
        layer = env.unroll(node.name)
        if layer is None:
            raise Exception("undefined symbol %r" % node.name)
        return fresh(layer[node.name])
    if isinstance(node, Literal):
        return node.kind
    if isinstance(node, Apply):
        fun_type = analyse(node.fun, env)
        arg_type = analyse(node.arg, env)
        res_type = Variable()
        unify(Type('->', [arg_type, res_type]), fun_type)
        return res_type
    if isinstance(node, LetRec):
        new_type = Variable()
        new_env = env.extend({node.bind: new_type})
        defn_type = analyse(node.defn, new_env)
        unify(defn_type, new_type)
        return analyse(node.body, new_env)
    if isinstance(node, Lambda):
        arg_type = Variable()
        new_env = env.extend({node.bind: arg_type)
        res_type = analyse(node.body, new_env)
        return Type('->', [arg_type, res_type])
    raise Exception("%r not in lambda calculus" % node)
