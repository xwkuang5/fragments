class Node:
    def __init__(self, val, left, right):
        self._val = val
        self._left = left
        self._right = right


def traverse(node):
    print(node._val)


def construct_tree_from_array(arr):
    size = len(arr)
    start_of_children = size // 2

    node_arr = [None] * len(arr)

    for i in range(start_of_children, size):
        node_arr[i] = Node(arr[i], None, None)

    for i in reversed(range(start_of_children)):
        left_child = i * 2 + 1
        right_child = (i + 1) * 2

        node_arr[i] = Node(arr[i], node_arr[left_child], node_arr[right_child])

    return node_arr[0]


def preorder_traversal_iterative(node):

    stack = [node]

    while len(stack) != 0:
        node = stack.pop()
        traverse(node)

        if node._right is not None:
            stack.append(node._right)
        if node._left is not None:
            stack.append(node._left)


def postorder_traversal_iterative(node):
    seen = set()

    stack = [node]

    while len(stack) != 0:

        node = stack.pop()

        if node in seen:
            traverse(node)
        else:
            if node._left is None and node._right is None:
                traverse(node)
            elif node._left is not None and node._right is None:
                seen.add(node)
                stack.append(node)
                stack.append(node._left)
            elif node._left is None and node._right is not Node:
                seen.add(node)
                stack.append(node)
                stack.append(node._right)
            else:
                seen.add(node)
                stack.append(node)
                stack.append(node._right)
                stack.append(node._left)


def inorder_traversal_iterative(node):

    seen = set()

    stack = [node]

    while len(stack) != 0:

        node = stack.pop()

        if node in seen:
            traverse(node)
        else:
            if node._left is None and node._right is None:
                traverse(node)
            elif node._left is not None and node._right is None:
                seen.add(node)
                stack.append(node)
                stack.append(node._left)
            elif node._left is None and node._right is not Node:
                traverse(node)
                stack.append(node._right)
            else:
                seen.add(node)
                stack.append(node._right)
                stack.append(node)
                stack.append(node._left)


arr = [1, 2, 3, 4, 5]

root = construct_tree_from_array(arr)

# inorder_traversal_iterative(root)

# postorder_traversal_iterative(root)

# preorder_traversal_iterative(root)
