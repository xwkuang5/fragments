import math
import time
import numpy as np
import concurrent.futures
import matplotlib.pyplot as plt


def cpu_bound_func(l):
    return l.sort()


naive = []
parallel = []

x = [10**x for x in range(1, 4)]

for n_elements in x:

    list_of_random_lists = [np.random.randn(10000) for _ in range(n_elements)]
    list_of_random_lists_copy = [np.copy(l) for l in list_of_random_lists]
    """Naive single thread"""
    start = time.time()
    for l in list_of_random_lists:
        cpu_bound_func(l)
    naive.append(time.time() - start)
    """Parallel"""
    with concurrent.futures.ProcessPoolExecutor() as executor:
        start = time.time()
        executor.map(cpu_bound_func, list_of_random_lists_copy)
    parallel.append(time.time() - start)

plt.semilogy(x, naive, 'r')
plt.semilogy(x, parallel, 'b')
plt.grid()
plt.legend(["Naive", "Parallel"])
plt.title("Naive versus parallel implementation")

plt.savefig("figures/test_concurrent.png")
