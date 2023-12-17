from collections import namedtuple
from inspect import stack

import functools


class StackDepthRecorder:
    def __init__(self):
        self.max_stack_depth = 0

    def record_stack_depth(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):

            # this is not accurate because wrapper itself causes a new stack
            # frame to be pushed
            self.max_stack_depth = max(self.max_stack_depth, len(stack(0)))

            result = func(self, *args, **kwargs)

            return result

        return wrapper


class StackDepthMeta(type):
    def __new__(cls, name, bases, dct):
        for key, value in dct.items():
            if callable(value):
                dct[key] = StackDepthRecorder.record_stack_depth(value)
        return super().__new__(cls, name, bases, dct)


class FibonacciRecursive(StackDepthRecorder, metaclass=StackDepthMeta):
    def fib(self, n):
        if n <= 1:
            return n
        else:
            return self.fib(n - 1) + self.fib(n - 2)


class FibonacciRecursiveCPS(StackDepthRecorder, metaclass=StackDepthMeta):
    def fib(self, n):
        ret = [0]

        def help(v):
            ret[0] = v
            return None
        self.fib_aux(n, help)
        return ret[0]

    def fib_aux(self, n, c):
        if n <= 1:
            return c(n)
        else:
            return self.fib_aux(
                n - 2,
                lambda v1: self.fib_aux(
                    n - 1,
                    lambda v2: c(
                        v1 + v2)))


Tramp = namedtuple('Tramp', ['f', 'a', 'c'])

# The main idea is that functions written in CPS style return a pointer to the function to be invoked
# along with the arguments to be used for evaluating the function and a continuation function.
# The trampoline device (the method) then iterates through the function chain until the base is reached
# at which point the continuation function should be called.


def trampoline(tramp):
    while tramp is not None:
        f, a, c = tramp
        if f is None:
            tramp = c(a)
        else:
            tramp = f(a, c)


class FibonacciRecursiveTrampoline(
        StackDepthRecorder,
        metaclass=StackDepthMeta):

    def fibt(self, n, c):
        if n <= 1:
            return Tramp(f=None, a=n, c=c)
        else:
            return Tramp(
                f=self.fibt,
                a=n - 1,
                c=lambda v1: Tramp(
                    f=self.fibt,
                    a=n - 2,
                    c=lambda v2: Tramp(
                        f=None,
                        a=v1 + v2,
                        c=c)))

    def fib(self, n):
        ret = [0]

        def help(v):
            ret[0] = v

        trampoline(Tramp(f=self.fibt, a=n, c=help))

        return ret[0]


fib_recursive = FibonacciRecursive()
fib_recursive_cps = FibonacciRecursiveCPS()
fib_trampoline = FibonacciRecursiveTrampoline()

n = 12
print("FibonacciRecursive:              {}".format(
    [fib_recursive.fib(i) for i in range(0, n)]))
print("FibonacciRecursiveCPS:           {}".format(
    [fib_recursive_cps.fib(i) for i in range(0, n)]))
print("FibonacciRecursiveTrampoline:    {}".format(
    [fib_trampoline.fib(i) for i in range(0, n)]))

print(
    "FibonacciRecursive max call depth:              {}".format(
        fib_recursive.max_stack_depth))
print("FibonacciRecursiveCPS max call depth:           {}".format(
    fib_recursive_cps.max_stack_depth))
print(
    "FibonacciRecursiveTrampoline max call depth:    {}".format(
        fib_trampoline.max_stack_depth))
