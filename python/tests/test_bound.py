import unittest

from .context import src
from src.bound import lower_bound, upper_bound


class TestBound(unittest.TestCase):
    def test_lower_bound(self):

        arr = []
        lb = lower_bound(arr, 0, 0, len(arr))
        self.assertEqual(lb, 0)

        arr = [1]
        lb = lower_bound(arr, 0, 0, len(arr))
        self.assertEqual(lb, 0)

        lb = lower_bound(arr, 1, 0, len(arr))
        self.assertEqual(lb, 0)

        lb = lower_bound(arr, 2, 0, len(arr))
        self.assertEqual(lb, 1)

        arr = [1, 1, 2, 3]

        lb = lower_bound(arr, -1, 0, len(arr))
        self.assertEqual(lb, 0)

        lb = lower_bound(arr, 1, 0, len(arr))
        self.assertEqual(lb, 0)

        lb = lower_bound(arr, 1.5, 0, len(arr))
        self.assertEqual(lb, 2)

        lb = lower_bound(arr, 3, 0, len(arr))
        self.assertEqual(lb, 3)

        lb = lower_bound(arr, 4, 0, len(arr))
        self.assertEqual(lb, 4)

    def test_upper_bound(self):
        arr = []
        ub = upper_bound(arr, 0, 0, len(arr))
        self.assertEqual(ub, 0)

        arr = [1]
        ub = upper_bound(arr, 0, 0, len(arr))
        self.assertEqual(ub, 0)

        ub = upper_bound(arr, 1, 0, len(arr))
        self.assertEqual(ub, 1)

        ub = upper_bound(arr, 2, 0, len(arr))
        self.assertEqual(ub, 1)

        arr = [1, 1, 2, 3]

        ub = upper_bound(arr, -1, 0, len(arr))
        self.assertEqual(ub, 0)

        ub = upper_bound(arr, 1, 0, len(arr))
        self.assertEqual(ub, 2)

        ub = upper_bound(arr, 1.5, 0, len(arr))
        self.assertEqual(ub, 2)

        ub = upper_bound(arr, 3, 0, len(arr))
        self.assertEqual(ub, 4)

        ub = upper_bound(arr, 4, 0, len(arr))
        self.assertEqual(ub, 4)
