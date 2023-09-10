import types

class Node:
    pass

class Number(Node):
    def __init__(self, val):
        self.val = val

class BinaryNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Add(BinaryNode):
    pass

class Subtract(BinaryNode):
    pass

class Multiply(BinaryNode):
    pass

class Divide(BinaryNode):
    pass

class Visitor:

    def visit(self, node):
        """
        At its core, this method uses generators to yield control back to the main method (visit).
        While a recursive method recurisvely call visit to move the algorithm forward and go deeper
        in the tree, the generator method upon receiving an expression that is not yet available,
        create a task (generator) corresponding to that expression, suspense its execution and ask
        the main method to finish performing the task before asking itself to do the task.

        Because a generator function (functions that have yield keyword in it) packs all the execution
        context into the generator object, there is no extra stack frame being generated. Instead, the
        generator object lives in the heap. As a result, this method will not encounter a maximum
        recursive depth exceeded error.

        The reason why we need to use recursion or generator on a node is that the result is not
        immediately available without further computation.
        """
        last_result = None
        stack = [node]
        while stack:
            try:
                last = stack[-1]
                if isinstance(last, types.GeneratorType):
                    # send last result to resume execution of generator object
                    stack.append(last.send(last_result))
                    # consume last result
                    last_result = None
                elif isinstance(last, Node):
                    stack.append(self._visit(stack.pop()))
                else:
                    last_result = stack.pop()
            except StopIteration:
                # catch the case where the generator has nothing to yield opon receiving send(None)
                # this is the only place where a generator object can popped off the stack
                stack.pop()

        return last_result


    def _visit(self, node):
        method_name = '_visit_{}'.format(node.__class__.__name__)

        if hasattr(self, method_name):
            method = getattr(self, method_name)
        else:
            method = self._generic_visit
        
        return method(node)

    def _generic_visit(self, node):
        raise NotImplementedError('No visit method found for {}'.format(node.__class__.__name__))

class EvaluatorVisitor(Visitor):

    def _visit_Number(self, node):
        yield node.val

    def _visit_Add(self, node):
        yield (yield node.left) + (yield node.right)

    def _visit_Subtract(self, node):
        yield (yield node.left) - (yield node.right)

    def _visit_Multiply(self, node):
        yield (yield node.left) * (yield node.right)

    def _visit_Divide(self, node):
        yield (yield node.left) / (yield node.right)



a = Number(0)

for i in range(100):
    a = Add(a, Number(i))

visitor = EvaluatorVisitor()

print(visitor.visit(a))