import math

class LazySegmentTreeForKBooking:
    """An implementation of a lazy segment tree for the following problem:
        `
            Implement a MyCalendarThree class to store your events. A new event can always be added.

            Your class will have one method, book(int start, int end). Formally, this represents a 
            booking on the half open interval [start, end), the range of real numbers x such that 
            start <= x < end.

            A K-booking happens when K events have some non-empty intersection (ie., there is some 
            time that is common to all K events.)

            For each call to the method MyCalendar.book, return an integer K representing the largest 
            integer such that there exists a K-booking in the calendar.
        `
    """

    def __init__(self, RANGE):

        height = math.ceil(math.log2(RANGE))

        self._tree_size = 2 * pow(2, height) - 1
        self._arr_size = RANGE

        self._arr = [0] * self._tree_size
        self._laziness = [0] * self._tree_size
    
    def left(self, index):
        return 2 * index + 1

    def right(self, index):
        return 2 * index + 2

    def _query(self, root, ss, se, l, r):
        self._normalize(root, ss, se)
        if se < l or ss > r:
            return 0
        else:
            if l <= ss <= se <= r:
                return self._arr[root]
            else:
                mid = ss + (se - ss) // 2
                left_child = self.left(root)
                right_child = self.right(root)
                left_val = self._query(left_child, ss, mid, l, r)
                right_val = self._query(right_child, mid+1, se, l, r)
                self._arr[root] = max(left_val, right_val)
                return self._arr[root]
    
    def _update(self, root, ss, se, l, r, val):
        self._normalize(root, ss, se)
        if ss < l or ss > r:
            return
        else:
            if l <= ss <= se <= r:
                # this is the only branch where we are gaining by using laziness during range update
                self._laziness[root] += val
                # we do not directly set self._arr
                # instead we let _normalize push down the changes
                self._normalize(root, ss, se)
            else:
                mid = ss + (se - ss) // 2
                left_child = self.left(root)
                right_child = self.right(root)
                self._update(left_child, ss, mid, l, r, val)
                self._update(right_child, mid+1, se, l, r, val)
                self._arr[root] = max(self._arr[left_child], self._arr[right_child])
    
    def _normalize(self, root, ss, se):
        """Normalize the tree node by pushing down the laziness if possible

        simply return if laziness is zero
        otherwise, check if current node is leaf
            if yes => update value and reset
            if no  => update value, push down laziness and reset
        """
        if self._laziness[root] > 0:
            self._arr[root] += self._laziness[root]
            if ss != se:
                left_child = self.left(root)
                right_child = self.right(root)
                self._laziness[left_child] += self._laziness[root]
                self._laziness[right_child] += self._laziness[root]
            self._laziness[root] = 0
        
    def book(self, start, end):
        
        self._update(0, 0, self._arr_size-1, start, end-1, 1)

        return self._arr[0]

booking = LazySegmentTreeForKBooking(10)

print(booking.book(0, 1))
print(booking.book(0, 2))
print(booking.book(1, 2))
print(booking.book(0, 2))
print(booking.book(0, 4))
print(booking.book(2, 4))
print(booking.book(3, 4))
print(booking.book(0, 10))