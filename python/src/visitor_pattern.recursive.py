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
        method_name = 'visit_{}'.format(node.__class__.__name__)

        if hasattr(self, method_name):
            method = getattr(self, method_name)
        else:
            method = self._generic_visit
        
        return method(node)

    def _generic_visit(self, node):
        raise NotImplementedError('No visit method found for {}'.format(node.__class__.__name__))

class EvaluatorVisitor(Visitor):

    def visit_Number(self, node):
        return node.val
    
    def visit_Add(self, node):
        return self.visit(node.left) + self.visit(node.right)

    def visit_Subtract(self, node):
        return self.visit(node.left) - self.visit(node.right)

    def visit_Multiply(self, node):
        return self.visit(node.left) * self.visit(node.right)

    def visit_Divide(self, node):
        return self.visit(node.left) / self.visit(node.right)


a = Number(0)

for i in range(100):
    a = Add(a, Number(i))

visitor = EvaluatorVisitor()

print(visitor.visit(a))