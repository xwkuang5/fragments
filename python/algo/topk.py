import numpy as np


def swap(arr, i, j):
    """Swap two elements in an array"""

    arr[i], arr[j] = arr[j], arr[i]


def randomized_partition(arr, low, high):

    pivot = arr[high]

    i = low - 1
    j = low

    while j < high:

        if arr[j] <= pivot:
            i += 1
            swap(arr, i, j)

        j += 1

    swap(arr, i + 1, j)
    return i + 1


def topk(arr, low, high, k):
    """Implement the top k selection algorithm

    Note that the resulting array may not be sorted
    """

    size = high - low + 1

    if size <= k:
        return arr[low:high + 1]

    pivot_idx = randomized_partition(arr, low, high)

    right_size = high - pivot_idx + 1

    if right_size > k:
        return topk(arr, pivot_idx + 1, high, k)
    elif right_size < k:
        return np.concatenate((arr[pivot_idx:high + 1],
                               topk(arr, low, pivot_idx - 1, k - right_size)))
    else:
        return arr[pivot_idx:high + 1]


arr = np.array([1, 5, 4, 3, 8, 9, 1, 2, 32, 4, 5])

print(topk(arr, 0, len(arr) - 1, 2))
