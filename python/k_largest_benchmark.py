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


class FindKLargest:
    def __init__(self, k):
        self._k = k

    @property
    def k(self):
        return self._k

    def sortAndReturnKLargest(self, list_):

        assert len(list_) >= self._k, "size of list can not be smaller than k"

        sorted_list_ = sorted(list_)

        return sorted_list_[-self._k:]

    def buildCompleteHeapAndReturnKLargest(self, list_):

        assert len(list_) >= self._k, "size of list can not be smaller than k"

        max_heap = Heap(list_, min_heap=False)

        return [max_heap.pop_top() for _ in range(self._k)]

    def buildHeapOfSizeKAndReturnKLargest(self, list_):

        assert len(list_) >= self._k, "size of list can not be smaller than k"

        min_heap = Heap(list_[:self._k], min_heap=True)

        cur_min = min_heap.get_top()

        for i in range(self._k, len(list_)):
            if list_[i] > cur_min:
                min_heap.pop_top()
                min_heap.insert(list_[i])
                cur_min = min_heap.get_top()

        return min_heap._arr

    def quick_select_partition(self, low, high, list_):

        pivot = list_[high]

        i = low - 1
        j = low

        while j <= high - 1:

            if list_[j] <= pivot:
                i += 1
                list_[i], list_[j] = list_[j], list_[i]

            j += 1

        i += 1
        list_[i], list_[high] = list_[high], list_[i]

        return i

    def quick_select_util(self, low, high, list_, k):

        num_elements = high - low + 1

        if num_elements <= k:
            return list_[low:high + 1]
        elif k == 0:
            return []
        else:

            pivot_pos = self.quick_select_partition(low, high, list_)

            num_in_right = high - pivot_pos

            if num_in_right >= k:
                return self.quick_select_util(pivot_pos + 1, high, list_, k)
            else:
                return self.quick_select_util(
                    low, pivot_pos - 1, list_,
                    k - num_in_right - 1) + list_[pivot_pos:high + 1]

    def quick_select_top_k(self, list_):

        list_copy = list_[:]

        return self.quick_select_util(0, len(list_) - 1, list_copy, self._k)


def iterate_heap(heap):

    heap_copy = copy.deepcopy(heap)

    ret = []

    while heap_copy.size != 0:
        ret.append(heap_copy.pop_top())

    print(ret)


import time
import numpy as np
from functools import partial

n = 2**20
random_seq = list(np.random.randint(0, 10000, size=n))

history = []

x_seq = [2**i for i in range(20)]

for k in x_seq:

    dummy = FindKLargest(k)

    func_list = [
        partial(dummy.sortAndReturnKLargest),
        partial(dummy.buildCompleteHeapAndReturnKLargest),
        partial(dummy.buildHeapOfSizeKAndReturnKLargest),
        partial(dummy.quick_select_top_k)
    ]

    k_history = []

    for func in func_list:

        start = time.time()

        _ = func(random_seq)

        k_history.append(time.time() - start)

    history.append(k_history)

history = np.array(history).reshape(4, -1)

plt.plot(x_seq, history[0], 'r', label='sorting')
plt.plot(x_seq, history[1], 'b', label='build large heap')
plt.plot(x_seq, history[2], 'g', label='build small heap')
plt.plot(x_seq, history[3], 'y', label='quick select')
plt.xticks(x_seq)

plt.legend()
plt.title("runtime of different method for finding k largest elements")

plt.savefig("figures/k_largest_runtime.png")
