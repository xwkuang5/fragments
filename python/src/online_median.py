import copy
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt


class Heap:
    def __init__(self, list_, min_heap=True):

        self._size = len(list_)
        self._arr = list_[:]
        self._min_heap = min_heap

        self._build_heap()

    @property
    def size(self):
        return self._size

    def get_top(self):
        assert self._size >= 1, "[get_min]: size of heap can not be smaller than 1"

        return self._arr[0]

    def pop_top(self):

        ret = self._arr[0]

        self._arr[0], self._arr[self._size - 1] = self._arr[self._size
                                                            - 1], self._arr[0]

        self._size -= 1

        self._bubble_down(0)

        self._arr.pop(-1)

        return ret

    def insert(self, key):
        self._arr.append(key)
        self._size += 1

        self._bubble_up(self._size - 1)

    def _build_heap(self):

        for i in reversed(range(self._first_leaf())):
            self._bubble_down(i)

    def _parent(i):
        return (i - 1) // 2

    def _left(i):
        return i * 2 + 1

    def _right(i):
        return (i + 1) * 2

    def _first_leaf(self):
        return self._size // 2

    def _bubble_down(self, i):

        if i < self._first_leaf():

            left = Heap._left(i)
            right = Heap._right(i)

            swap_idx = i

            if self._min_heap:
                if left < self._size and self._arr[swap_idx] > self._arr[left]:
                    swap_idx = left

                if right < self._size and self._arr[swap_idx] > self._arr[right]:
                    swap_idx = right
            else:
                if left < self._size and self._arr[swap_idx] < self._arr[left]:
                    swap_idx = left
                if right < self._size and self._arr[swap_idx] < self._arr[right]:
                    swap_idx = right

            if swap_idx != i:

                self._arr[swap_idx], self._arr[i] = self._arr[i], self._arr[
                    swap_idx]

                self._bubble_down(swap_idx)

    def _bubble_up(self, i):
        parent = Heap._parent(i)

        if self._min_heap:
            if parent >= 0 and self._arr[i] < self._arr[parent]:

                self._arr[parent], self._arr[i] = self._arr[i], self._arr[
                    parent]

                self._bubble_up(parent)
        else:
            if parent >= 0 and self._arr[i] > self._arr[parent]:
                self._arr[parent], self._arr[i] = self._arr[i], self._arr[
                    parent]

                self._bubble_up(parent)


class OnlineMedian:
    def __init__(self):

        self._max_heap = Heap([], min_heap=False)
        self._min_heap = Heap([], min_heap=True)

    def find_median(self, val):
        """This algorithm implements the O(log(n)) method for finding median
        of a sequence in an online fashion. The algorithm maintains two heap
        for bookeeping. A max_heap to store the smaller half of the sequence
        and a min_heap to store the greater half of the sequence. Median is
        defined as a_ceiling(n/2). Note that the algorithm only needs to be
        tweaked a little bit to work for the general definition of median.
        """

        if self._max_heap.size == 0 and self._min_heap.size == 0:
            self._max_heap.insert(val)
            return val

        elif self._max_heap.size != 0 and self._min_heap.size == 0:
            cur_median = self._max_heap.get_top()

            if cur_median <= val:
                self._min_heap.insert(val)
                return cur_median
            else:
                self._min_heap.insert(cur_median)
                self._max_heap.pop_top()
                self._max_heap.insert(val)
                return val
        else:
            max_heap_top = self._max_heap.get_top()
            min_heap_top = self._min_heap.get_top()

            if val <= max_heap_top:
                if self._max_heap.size == self._min_heap.size:
                    self._max_heap.insert(val)
                    return max_heap_top
                else:
                    self._min_heap.insert(max_heap_top)
                    self._max_heap.pop_top()
                    self._max_heap.insert(val)
                    return self._max_heap.get_top()
            elif max_heap_top < val < min_heap_top:
                if self._max_heap.size == self._min_heap.size:
                    self._max_heap.insert(val)
                    return val
                else:
                    self._min_heap.insert(val)
                    return max_heap_top
            else:
                if self._max_heap.size == self._min_heap.size:
                    self._max_heap.insert(min_heap_top)
                    self._min_heap.pop_top()
                    self._min_heap.insert(val)
                    return min_heap_top
                else:
                    self._min_heap.insert(val)
                    return max_heap_top


online_median = OnlineMedian()

seq = [15, 10, 1, 20, 30]

ret = [online_median.find_median(val) for val in seq]

print(ret)
