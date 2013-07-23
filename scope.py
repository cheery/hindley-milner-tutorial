class Scope(object):
    def __init__(self, objects, parent):
        self.objects = objects
        self.parent = parent

    def unroll(self, name):
        if name in self:
            return self
        if self.parent is not None:
            return self.parent.unroll(name)
        
    def __contains__(self, name):
        return name in self.objects

    def __getitem__(self, name):
        return self.objects[name]

    def __setitem__(self, name, value):
        self.objects[name] = value

    def extend(self, objects=None):
        objects = {} if objects is None else objects
        return Scope(objects, self)

    def update(self, *a, **kw):
        self.objects.update(*a, **kw)

def empty():
    return Scope({}, None)
