class TrieNode:
    """A character trie node
    """

    def __init__(self, val):

        self._val = val
        self._children = {}


class Trie:
    """A character trie
    """

    def __init__(self):

        self._root = TrieNode(None)

    def search(self, key):
        node = self._root

        for ch in key:
            if ch not in node._children:
                return None
            else:
                node = node._children[ch]

        return node._val

    def insert(self, key, val):

        node = self._root

        last_idx = -1

        for idx, ch in enumerate(key):
            if ch not in node._children:
                last_idx = idx
                break
            else:
                node = node._children[ch]

        if last_idx != -1:
            for ch in key[last_idx:]:
                node._children[ch] = TrieNode(None)
                node = node._children[ch]

        node._val = val

    def remove(self, key):
        """Assume key is present

        remove with compression
        """

        stack = []

        node = self._root

        for ch in key:
            stack.append((node, ch))
            node = node._children[ch]

        node.val = None

        while len(stack) > 0 and len(node._children) == 0:
            node, ch = stack.pop()
            node._children.pop(ch)
