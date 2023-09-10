class PriorityQueue:
    """A min priority queue with decrease_key operations
    """

    def __init__(self, arr):

        self._map_key_to_idx = {}

        self._size = len(arr)
        self._arr = arr[:]

        self._build_heap()

    def is_empty(self):
        return self._size == 0

    def insert(self, key):
        self._arr.append(key)
        self._size += 1

        self._bubble_up(self._size - 1)

    def pop(self):
        assert not self.is_empty(), "Can not pop element from empty queue"

        ret = self._arr[0]

        self._swap(0, self._size - 1)
        self._size -= 1
        self._arr.pop()

        self._bubble_down(0)
        self._map_key_to_idx.pop(ret)
        return ret

    def decrease_key(self, key, decrement):
        """Assumption: key is unique

        This particular implementation is problematic because key is both the key and the value
        """
        assert decrement < 0, "Decrement can not be greater or equal to zero for a min priority queue"

        idx = self._map_key_to_idx[key]

        self._arr[idx] = key + decrement

        self._bubble_up(idx)

    def _build_heap(self):
        for i in reversed(range(self._start_of_child())):
            self._bubble_down(i)

    def _swap(self, i, j):

        self._map_key_to_idx[self._arr[i]] = j
        self._map_key_to_idx[self._arr[j]] = i

        self._arr[i], self._arr[j] = self._arr[j], self._arr[i]

    def _bubble_up(self, i):
        while i > 0 and self._arr[i] < self._arr[self._parent(i)]:
            self._swap(i, self._parent(i))
            i = self._parent(i)

    def _bubble_down(self, i):
        while i < self._start_of_child():
            left_child = self._left_child(i)
            right_child = self._right_child(i)
            min_idx = i
            min_val = self._arr[i]

            if min_val > self._arr[left_child]:
                min_idx = left_child
                min_val = self._arr[left_child]
            if right_child < self._size and min_val > self._arr[right_child]:
                min_idx = right_child
                min_val = self._arr[right_child]

            if min_idx != i:
                self._swap(i, min_idx)
                i = min_idx
            else:
                break

    def _left_child(self, i):
        return 2 * i + 1

    def _right_child(self, i):
        return 2 * (i + 1)

    def _parent(self, i):
        return (i - 1) // 2

    def _start_of_child(self):
        return self._size // 2


arr = [5, 4, 3, 2, 1]

pq = PriorityQueue(arr)

pq.decrease_key(5, -6)

sorted_arr = []

while not pq.is_empty():
    sorted_arr.append(pq.pop())

print(sorted_arr)
