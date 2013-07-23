import calculus

class Applier(object):
    def __init__(self, parent):
        self.parent = parent
        self.left = None

    def gen(self):
        return self.left

    def side(self, right):
        if self.left is None:
            self.left = right
        else:
            self.left = calculus.Apply(self.left, right)
        return self

    def close(self):
        raise Exception("excessive right parenthesis")
    
    def done(self):
        return self.left

    def bash(self):
        res = Letter(self, self.left)
        self.left = None
        return res

class Parenthesis(Applier):
    def close(self):
        if self.left is None:
            raise Exception("empty parentheses")
        return self.parent.side(self.left)

    def done(self):
        raise Exception("missing right parenthesis")

class Binder(Applier):
    def __init__(self, parent, bind):
        Applier.__init__(self, parent)
        self.bind = bind

    def gen(self):
        if self.left is None:
            raise Exception("empty lambda")
        return calculus.Lambda(self.bind, self.left)

    def close(self):
        return self.parent.side(self.gen()).close()

    def done(self):
        return self.parent.side(self.gen()).done()

    def bash(self):
        return self.parent.side(self.gen()).bash()

class Letter(Applier):
    def __init__(self, parent, defn):
        Applier.__init__(self, parent)
        self.defn = defn
        self.bind = None

    def gen(self):
        if self.bind is None:
            raise Exception("unnamed letrec")
        if self.left is None:
            raise Exception("empty letrec")
        return calculus.LetRec(self.bind, self.defn, self.left)

    def close(self):
        return self.parent.side(self.gen()).close()

    def done(self):
        return self.parent.side(self.gen()).done()

def tokens(source):
    s = u''
    for c in source:
        if (c.isspace() or c in '()') and len(s) > 0:
            yield s
            s = u''
        if c == '(':
            yield '('
        elif c == ')':
            yield ')'
        elif not c.isspace():
            s += c
    if len(s) > 0:
        yield s

def string(source, mapping):
    builder = Applier(None)
    for token in tokens(source):
        if isinstance(builder, Letter) and builder.bind is None:
            builder.bind = token
        elif token == ')':
            builder = builder.close()
        elif token == '(':
            builder = Parenthesis(builder)
        elif token.startswith(':'):
            builder = Binder(builder, token[1:])
        elif token == 'as':
            builder = builder.bash()
        elif token.isdigit():
            lit = calculus.Literal(mapping['Integer'], token)
            builder = builder.side(lit)
        else:
            idt = calculus.Identifier(token)
            builder = builder.side(idt)
    return builder.done()

def file(path, mapping):
    with open(path) as fd:
        return string(fd.read().decode('utf-8'), mapping)

if __name__=='__main__':
    import write, sys, os
    for name in os.listdir('examples'):
        path = os.path.join('examples', name)
        if name.startswith('.'):
            continue
        print 'reading %s' % path
        mapping = {'Integer': None}
        program = file(path, mapping)
        print 'checking %s' % path
        write.debug(program)
        write.expr(sys.stdout, program)
