import time
import functools
import numpy as np
import matplotlib.pyplot as plt


def interpolation_search(arr, low, high, key):
    while low <= high:

        if arr[low] == arr[high]:
            if arr[low] == key:
                return low
            elif arr[low] < key:
                return high + 1
            else:
                return low
        interp = low + int(
            (key - arr[low]) // (arr[high] - arr[low]) * (high - low))

        interp = interp if interp >= low else low
        interp = interp if interp <= high else high

        if arr[interp] < key:
            low = interp + 1
        elif arr[interp] > key:
            high = interp - 1
        else:
            return interp

    return low


def binary_search(arr, low, high, key):

    while low <= high:

        mid = (low + high) // 2

        if arr[mid] == key:
            return mid
        elif arr[mid] < key:
            low = mid + 1
        else:
            high = mid - 1

    return low


if __name__ == "__main__":

    exponent = 6
    repition = 30

    time_history = np.empty((2, exponent, repition), dtype=np.float64)
    ret_history = np.empty((2, exponent, repition), dtype=np.int64)

    for size_idx, size in enumerate([10**i for i in range(1, exponent + 1)]):

        low = 0
        high = size - 1
        arr = np.random.rand(repition, size)
        arr = np.sort(arr, axis=1)
        key = np.random.rand(repition)

        for rep_idx, rep in enumerate(range(repition)):

            for idx, search_type in enumerate(
                ["interpolation search", "binary search"]):
                handle = functools.partial(
                    interpolation_search
                ) if search_type == "interpolation_search" else functools.partial(
                    binary_search)

                start = time.time()

                ret = handle(arr[rep_idx], low, high, key[rep_idx])

                time_history[idx, size_idx, rep_idx] = time.time() - start
                ret_history[idx, size_idx, rep_idx] = arr[
                    rep_idx, ret] if ret <= high else -1

    assert np.all(ret_history[0].flatten() == ret_history[1]
                  .flatten()), "result of the two search does not aggree"

    interp_mean = np.mean(time_history[0], axis=1)
    binary_mean = np.mean(time_history[1], axis=1)
    interp_std = np.std(time_history[0], axis=1)
    binary_std = np.std(time_history[1], axis=1)

    xseq = np.arange(1, exponent + 1)

    plt.plot(xseq, interp_mean, '#CC4F1B', label="interpolation search")
    plt.fill_between(
        xseq,
        interp_mean - interp_std,
        interp_mean + interp_std,
        alpha=0.5,
        edgecolor='#CC4F1B',
        facecolor='#FF9848')
    plt.plot(xseq, binary_mean, '#1B2ACC', label="binary search")
    plt.fill_between(
        xseq,
        binary_mean - binary_std,
        binary_mean + binary_std,
        alpha=0.2,
        edgecolor='#1B2ACC',
        facecolor='#089FFF',
        linewidth=4,
        linestyle='dashdot',
        antialiased=True)
    plt.xticks(xseq)
    plt.legend()
    plt.xlabel("10 ** i")
    plt.ylabel("time (s)")
    plt.title("Search time comparison")
    plt.savefig("figures/search_comparison.png")
    plt.show()
