import math

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Vector({self.x!r}, {self.y!r})'

    def __bool__(self):
        return bool(self.x or self.y)

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __pos__(self):
        return self

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __add__(self, other):
        return Vector(self.x+other.x, self.y+other.y)

    __iadd__ = __add__

    def __mul__(self, s):
        return Vector(self.x*s, self.y*s)

    __imul__ = __rmul__ = __mul__

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __sub__(self, other):
        return Vector(self.x-other.x, self.y-other.y)

    __isub__ = __sub__

    def __matmul__(self, other):
        return self.x*other.x + self.y*other.y

    __imatmul__ = __matmul__

a = Vector(1, 2)
a @= Vector(1, 2)
print(a)
