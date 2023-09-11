def permute(obj_list, l, r, level):
    """Helper function to implement the nAr permutation operation

    Arguments:
    obj_list    -- the list of objects from which the permutation should be generated
    l           -- left end point of current permutation
    r           -- right end point (exclusive) of current permutation
    level       -- used to stop the recursion prematruely according to r
    """

    if level == 0:
        print(obj_list[:l])
    else:
        for i in range(l, r):
            obj_list[l], obj_list[i] = obj_list[i], obj_list[l]
            permute(obj_list, l + 1, r, level - 1)
            obj_list[l], obj_list[i] = obj_list[i], obj_list[l]


def nAr(obj_list, n, r):
    """Implement the nAr permutation operation

    Arguments:
    obj_list    -- the list of objects from which the permutation should be generated
    n           -- number of elements in object list
    r           -- number of chosen elements
    """

    assert len(obj_list) == n and r <= n, "incorrect input!"

    permute(obj_list, 0, n, r)


obj_list = [1, 2, 3]
nAr(obj_list, len(obj_list), 2)
