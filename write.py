import calculus
import read
import StringIO

def debug(expr):
    fd = StringIO.StringIO()
    subexpr(fd, expr)
    a = fd.getvalue()
    fd = StringIO.StringIO()
    subexpr(fd, read.string(a, {'Integer':None}))
    b = fd.getvalue()
    assert a == b, "bad match\n%r\n%r" % (a, b)

def subexpr(fd, expr, mode=0):
    if isinstance(expr, calculus.LetRec):
        subexpr(fd, expr.defn)
        fd.write(' as %s ' % expr.bind)
        subexpr(fd, expr.body)
    elif isinstance(expr, calculus.Lambda):
        if mode == 0:
            fd.write('(')
            subexpr(fd, expr, 1)
            fd.write(')')
        else:
            fd.write(':%s ' % expr.bind)
            subexpr(fd, expr.body)
    elif isinstance(expr, calculus.Apply):
        if mode == 1:
            fd.write('(')
            subexpr(fd, expr, 0)
            fd.write(')')
        else:
            subexpr(fd, expr.fun, 0)
            fd.write(' ')
            subexpr(fd, expr.arg, 1)
    elif isinstance(expr, calculus.Identifier):
        fd.write(expr.name)
    elif isinstance(expr, calculus.Literal):
        fd.write(expr.value)
    else:
        fd.write('%r' % expr)

def expr(fd, root):
    subexpr(fd, root)
    fd.write('\n')
    fd.flush()
