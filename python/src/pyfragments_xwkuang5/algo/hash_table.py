class HashTableChaining:
    """Hashtable with separate chaining
    """

    def __init__(self, size, alpha_low, alpha_high):
        self._size = size
        self._arr = [[] for _ in range(self._size)]
        self._hash_function = lambda x: (3 * x + 1) % self._size

        self.num_occupied = 0
        self._alpha_low = alpha_low
        self._alpha_high = alpha_high

    def _resize(self, size):
        tmp = self._arr

        self.__init__(size, self._alpha_low, self._alpha_high)

        for val in [key for key in chain for chain in tmp]:
            self.insert(val)

    def insert(self, key):
        hash_val = self._hash_function(key)

        # for linkedlist, we insert at front
        # for array, we insert at the back
        self._arr[hash_val].append(key)
        self.num_occupied += 1

        if self.num_occupied / self._size > self._alpha_high:
            self._resize(self._size * 2)

    def search(self, key):

        hash_val = self._hash_function(key)

        return key in self._arr[hash_val]

    def remove(self, key):

        hash_val = self._hash_function(key)

        if key in self._arr[hash_val]:
            # this is costly
            self._arr[hash_val].remove(key)
            self.num_occupied -= 1

            if self.num_occupied / self._size < self._alpha_low:
                self._resize(self._size // 2)


class HashtableOpenAddressing:
    """Hashtable with open addressing (linear probing)
    
    Assume keys are positive

    Use lazy deletion, use -1 to denote deleted
    """

    def __init__(self, size, alpha_low, alpha_high):
        self._size = size
        self._arr = [None] * size
        self._hash_function = lambda x: (3 * x + 1) % self._size

        self.num_occupied = 0
        self._alpha_low = alpha_low
        self._alpha_high = alpha_high

    def _resize(self, size):

        tmp = self._arr

        self.__init__(size, self._alpha_low, self._alpha_high)

        for key in tmp:
            if key is None or key == -1:
                continue

            hash_val = self._hash_function(key)

            while self._arr[hash_val] is not None:
                hash_val += 1

            self._arr[hash_val] = key

    def insert(self, key):

        hash_val = self._hash_function(key)

        while True:

            val = self._arr[hash_val]

            if val is not None and val != -1:
                hash_val += 1
            else:
                break

        self._arr[hash_val] = key
        self.num_occupied += 1

        if self.num_occupied / self._size > self._alpha_high:
            self._resize(self._size * 2)

    def search(self, key):

        hash_val = self._hash_function(key)

        while self._arr[hash_val] is not None:
            if self._arr[hash_val] == key:
                return True

        return False

    def remove(self, key):

        hash_val = self._hash_function(key)

        while self._arr[hash_val] is not None:
            if self._arr[hash_val] == key:
                self._arr[hash_val] = -1

                self.num_occupied -= 1

                if self.num_occupied / self._size < self._alpha_low:
                    self._resize(self._size // 2)
