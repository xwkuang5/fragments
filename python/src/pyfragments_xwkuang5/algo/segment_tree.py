import sys
import math


class SegmentTree:
    """
    1. Properties of rangeSum with Segmentree:
        construction: O(n) time, O(n) space
        range query: O(log(n)) time (O(1) for prefix sum and O(n) for array)
        update: O(log(n)) (O(n) for prefix sum and O(1) for array)
    
    2. Properties of rangeMinimum with Segmentree:
        construction: O(n) time, O(n) space
        range query: O(log(n)) time (O(n) for array)
        update: O(log(n)) (O(1) for array)
    """

    def __init__(self, arr, tree_type='sum'):

        height = math.ceil(math.log2(len(arr)))
        self._tree_size = int(2 * math.pow(2, height) - 1)
        self._size = len(arr)
        self._tree_type = tree_type
        self._arr = [None] * self._tree_size
        self._construct(0, 0, self._size - 1, self._arr, arr, tree_type)

    def _construct(self, root, l, r, tree_arr, arr, tree_type):

        if l == r:
            tree_arr[root] = arr[l]
        else:

            mid = (l + r) // 2

            left = self._left(root)
            right = self._right(root)

            self._construct(left, l, mid, tree_arr, arr, tree_type)
            self._construct(right, mid + 1, r, tree_arr, arr, tree_type)

            if tree_type == 'sum':
                tree_arr[root] = tree_arr[left] + tree_arr[right]
            elif tree_type == 'min':
                tree_arr[root] = min(tree_arr[left], tree_arr[right])

    def _update_range_min(self, idx, val):
        l = 0
        r = self._size - 1
        root = 0

        while l < r:
            self._arr[root] = min(self._arr[root], val)

            mid = (l + r) // 2

            if idx <= mid:
                r = mid
                root = self._left(root)
            else:
                l = mid + 1
                root = self._right(root)

        self._arr[root] = min(self._arr[root], val)

    def _update_range_sum(self, idx, val):
        l = 0
        r = self._size - 1

        root = 0

        while l < r:
            mid = (l + r) // 2

            if idx <= mid:
                r = mid
                root = self._left(root)
            else:
                l = mid + 1
                root = self._right(root)

        diff = val - self._arr[root]

        l = 0
        r = self._size - 1

        root = 0

        while l < r:
            self._arr[root] += diff

            mid = (l + r) // 2
            if idx <= mid:
                r = mid
                root = self._left(root)
            else:
                l = mid + 1
                root = self._right(root)

        self._arr[root] += diff

    def update(self, idx, val):

        if idx < 0 or idx >= self._size:
            raise ValueError("Incorrect update index!")

        if self._tree_type == 'sum':
            self._update_range_sum(idx, val)
        elif self._tree_type == 'min':
            self._update_range_min(idx, val)
        else:
            raise ValueError("Invalid tree type!")

    def _query_helper(self, root, l, r, low, high):

        if l <= low <= high <= r:
            return self._arr[root]
        elif r < low or high < l:
            if self._tree_type == 'sum':
                return 0
            elif self._tree_type == 'min':
                return sys.maxsize
            else:
                raise ValueError("Invalid tree type!")
        else:
            mid = (low + high) // 2

            left = self._query_helper(self._left(root), l, r, low, mid)
            right = self._query_helper(self._right(root), l, r, mid + 1, high)

            if self._tree_type == 'sum':
                return left + right
            elif self._tree_type == 'min':
                return min(left, right)
            else:
                raise ValueError("Invalid tree type!")

    def query(self, l, r):

        return self._query_helper(0, l, r, 0, self._size - 1)

    def _left(self, i):
        return 2 * i + 1

    def _right(self, i):
        return 2 * (i + 1)


arr = [1, 2, 3, 4, 5, 6]

tree = SegmentTree(arr, 'sum')

print(tree.query(4, 5))
tree.update(5, -1)
print(tree.query(4, 5))
