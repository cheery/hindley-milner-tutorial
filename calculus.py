class Lambda(object):
    def __init__(self, bind, body):
        self.bind = bind
        self.body = body

class Identifier(object):
    def __init__(self, name):
        self.name = name

class Literal(object):
    def __init__(self, kind, value):
        self.kind = kind
        self.value = value

class Apply(object):
    def __init__(self, fun, arg):
        self.fun = fun
        self.arg = arg

class LetRec(object):
    def __init__(self, bind, defn, body):
        self.bind = bind
        self.defn = defn
        self.body = body
