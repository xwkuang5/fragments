def randomized_partition(arr, low, high):
    """Partition the array into two halfs according to the last element (pivot)

    loop invariant:
        [low, i] <= pivot
        [i+1, j) > pivot
    """

    i = low - 1
    j = low

    pivot = arr[high]

    while j < high:
        if arr[j] <= pivot:
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]
        j = j + 1
    i = i + 1
    arr[i], arr[high] = pivot, arr[i]

    return i


def qsort(arr, low, high):
    if low < high:
        pivot_loc = randomized_partition(arr, low, high)
        qsort(arr, low, pivot_loc - 1)
        qsort(arr, pivot_loc + 1, high)


def merge(arr, low, mid, high):
    left = arr[low:mid + 1]
    right = arr[mid + 1:high + 1]

    i = 0
    j = 0
    k = low

    while i <= mid - low and j <= high - mid - 1:
        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1

    while i <= mid - low:
        arr[k] = left[i]
        i += 1
        k += 1

    while j <= high - mid - 1:
        arr[k] = right[j]
        j += 1
        k += 1


def merge_sort(arr, low, high):
    if low < high:
        mid = int((low + high) / 2)
        merge_sort(arr, low, mid)
        merge_sort(arr, mid + 1, high)
        merge(arr, low, mid, high)


def left_child(index):
    return 2 * index + 1


def right_child(index):
    return 2 * index + 2


def min_heapify(arr, index, size):

    left = left_child(index)
    right = right_child(index)

    # find smallest among children, swap and heapify children
    if left < size and arr[left] < arr[index]:
        smallest_idx = left
    else:
        smallest_idx = index
    if right < size and arr[right] < arr[smallest_idx]:
        smallest_idx = right
    if smallest_idx != index:
        arr[index], arr[smallest_idx] = arr[smallest_idx], arr[index]
        min_heapify(arr, smallest_idx, size)


def build_heap(arr, size):
    for i in reversed(range(int(size / 2))):
        min_heapify(arr, i, size)


def heap_sort(arr, low, high):
    copy = arr[low:high + 1]
    size = high - low + 1

    build_heap(copy, size)

    for i in reversed(range(1, size)):
        copy[0], copy[i] = copy[i], copy[0]
        size = size - 1
        min_heapify(copy, 0, size)

    arr[low:high + 1] = [x for x in reversed(copy)]


def radix_sort(arr, low, high, digit, base=10):
    def sort_digit(arr, low, high, pos, base):
        buckets = [[] for _ in range(base)]

        for val in arr[low:high + 1]:

            digit = (val // base**pos) % base

            buckets[digit].append(val)

        return [item for digit_list in buckets for item in digit_list]

    for i in range(digit):

        arr[low:high + 1] = sort_digit(arr, low, high, i, base)


arr = [2, 1, 2, 4, 7, 5, 2, 6, 10, 8]
size = len(arr)
# qsort(arr, 0, size-1)
# heap_sort(arr, 0, size - 1)
radix_sort(arr, 0, size - 1, 1, 10)
print(arr)
