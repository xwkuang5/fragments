def lower_bound(arr, value, first, last):
    """Find the lower bound of the value in the array

    lower bound: the first element in arr that is larger than or equal
    to value

    Args:
        arr         : input array
        value       : target value
        first       : starting point of the search, inclusive
        last        : ending point of the search, exclusive

    Return
        index       : integer
                        if index == last => lower bound does not exist
                        else => arr[index] >= value

    Note:
        1. use first + (last - first) // 2 to avoid overflow in old language
        2. invariant:
            1. all values in the range [initial_first, first) is smaller 
            than value
            2. all values in the range [last, initial_last) is greater than 
            or equal to value
            3. first < last
            
            at the end of the iteration, first = last
                if a value greter than or equal to value exists, we simply
                return the first element in the range [last, initial_last)
                else we can return anything (last, -1, etc) to denote that
                such a value does not exist
            
            note also that at the end first and last will always be the same
            so it does not matter which one we return
    """

    while first < last:

        mid = first + (last - first) // 2

        if arr[mid] < value:
            first = mid + 1
        else:
            last = mid

    return first


def upper_bound(arr, value, first, last):
    """Find the upper bound of the value in the array

    upper bound: the first element in arr that is larger than value

    Args:
        arr         : input array
        value       : target value
        first       : starting point of the search, inclusive
        last        : ending point of the search, exclusive

    Return
        index       : integer
                        if index == last => upper bound does not exist
                        else => arr[index] > value
    """

    while first < last:

        mid = first + (last - first) // 2

        if arr[mid] <= value:
            first = mid + 1
        else:
            last = mid

    return first
