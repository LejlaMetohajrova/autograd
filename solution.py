import math


class Variable:
    def __init__(self, value, left=None, right=None, op=None):
        self.value = float(value)
        self.left = left
        self.right = right
        self.op = op
        self.d = Deriv(0)

    def __add__(self, other):
        if not isinstance(other, self.__class__):
            other = Variable(other)
        return Variable(self.value + other.value, self, other, d_add)

    def __sub__(self, other):
        if not isinstance(other, self.__class__):
            other = Variable(other)
        return Variable(self.value - other.value, self, other, d_sub)

    def __mul__(self, other):
        if not isinstance(other, self.__class__):
            other = Variable(other)
        return Variable(self.value * other.value, self, other, d_mul)

    def __div__(self, other):
        if not isinstance(other, self.__class__):
            other = Variable(other)
        return Variable(self.value / other.value, self, other, d_div)

    def __radd__(self, other):
        if not isinstance(other, self.__class__):
            other = Variable(other)
        return Variable(other.value + self.value, other, self, d_add)

    def __rsub__(self, other):
        if not isinstance(other, self.__class__):
            other = Variable(other)
        return Variable(other.value - self.value, other, self, d_sub)

    def __rmul__(self, other):
        if not isinstance(other, self.__class__):
            other = Variable(other)
        return Variable(other.value * self.value, other, self, d_mul)

    def __rdiv__(self, other):
        if not isinstance(other, self.__class__):
            other = Variable(other)
        return Variable(other.value / self.value, other, self, d_div)

    def backward(self):
        self.d.value = 1
        self.chain()

    def chain(self):
        if not self.left:
            return

        self.op(self)
        self.left.chain()
        self.right.chain()

    def exp(self):
        return Variable(math.exp(self.value))

    def log(self):
        return Variable(math.log(self.value))

    def tanh(self):
        return Variable(math.tanh(self.value))


def d_add(me):
    me.left.d.value += me.d.value
    me.right.d.value += me.d.value

def d_sub(me):
    me.left.d.value += me.d.value
    me.right.d.value -= me.d.value

def d_mul(me):
    me.left.d.value += me.d.value * me.right.value
    me.right.d.value += me.d.value * me.left.value

def d_div(me):
    me.left.d.value += me.d.value / me.right.value
    me.right.d.value -= (me.d.value * me.left.value) / \
                              (me.right.value**2)


class Deriv:
    def __init__(self, value):
        self.value = value
