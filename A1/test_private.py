import typing
import unittest
import numpy as np

from csp import CSP

class TestCSP(unittest.TestCase):

    '''
    Testcase to check if the code can handle the edge case of only one cell belonging to a group.
    '''
    def test_one_cell(self):
        group = [[(0,0)]]
        constraints = [(1, 1)]
        valid_grid = np.array([[0]])
        csp = CSP(valid_grid, numbers={1, 2}, groups=group, constraints=constraints)
        result = csp.start_search()
        self.assertEqual(result, [[1]])

    '''
    Testcase for the edge case of only one group existing in the matrix, so a few cells do not belong to any groups.
    Check if the code can handle this edge case.
    '''
    def test_one_group(self):
        group = [[(0,0),(0,1)]]
        constraints = [(3, 1)]
        valid_grid = np.array([[0,0],
                               [0,0]])
        csp = CSP(valid_grid, numbers={1, 2}, groups=group, constraints=constraints)
        result = csp.start_search()
        self.assertTrue(np.all(result == [[1,2],[1,1]]))


    '''
    Testcase to see if the code can handle a partially filled group constraint where either the sum or count constraint
    is filled with a None value.
    '''
    def test_partially_filled_constraint(self):
        horizontal_groups = [[(0, 0), (0, 1)], [(1, 0), (1, 1)]]
        vertical_groups = [[(0, 0), (1, 0)], [(0, 1), (1, 1)]]
        groups = horizontal_groups + vertical_groups
        constraints = [(3,None),(None,1),(3,None),(None,1)]
        valid_grid = np.array([[0, 0],
                               [0, 0]])
        solution_grid = np.array([[1, 1],
                                 [1, 2]])
        csp = CSP(valid_grid, numbers={1, 2}, groups=groups, constraints=constraints)
        result = csp.start_search()
        self.assertTrue(np.all(result == solution_grid))
