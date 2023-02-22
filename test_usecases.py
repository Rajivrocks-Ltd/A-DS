import typing
import unittest
import numpy as np

from csp import CSP

##############################################################################################
# Note that in the test cases below, we always use an increasing set of numbers for simplicity
# (e.g., {1,2} or {1,2,3}) but it can be any arbitrary set of numbers, such as {2,1} or 
# {900, 50,1}
##############################################################################################

class TestCSP(unittest.TestCase):

    def test_fill_cell_to_groups(self):
        horizontal_groups = [[(0,0),(0,1)], [(1,0), (1,1)]]
        vertical_groups = [[(0,0), (1,0)], [(0,1), (1,1)]]
        groups = horizontal_groups + vertical_groups
        # every constraint is of the form (sum, count). so every group must sum to 3 and every number may only occur once per group
        constraints = [(3, 1), (3, 1), (3, 1), (3, 1)]
        csp = CSP(np.array([[0,0],[0,0]]), numbers=set([1,2]), groups=groups, constraints=constraints)
        csp.fill_cell_to_groups()
        result = csp.cell_to_groups

        cell_to_groups = {(0, 0): [0, 2], (0, 1): [0, 3], (1, 0): [1, 2], (1, 1): [1, 3]}
        for row_idx in range(2):
            for col_idx in range(2):
                for sol_group in cell_to_groups[(row_idx, col_idx)]:
                    self.assertTrue(sol_group in result[(row_idx, col_idx)])


    def test_satisfies_sum_constraint(self):
        horizontal_groups = [[(0,0),(0,1)], [(1,0), (1,1)]]
        vertical_groups = [[(0,0), (1,0)], [(0,1), (1,1)]]
        groups = horizontal_groups + vertical_groups
        # every constraint is of the form (sum, count). so every group must sum to 3 and every number may only occur once per group
        constraints = [(3, 1), (3, 1), (3, 1), (3, 1)]

        valid_grid = np.array([[1,2],
                               [2,1]])
        csp = CSP(valid_grid, numbers=set([1,2]), groups=groups, constraints=constraints)
        for group_idx in range(len(groups)):
            result = csp.satisfies_sum_constraint(groups[group_idx], 3)
            self.assertTrue(result)


        invalid_grid = np.array([[1,4],
                                 [5,1]])
        csp = CSP(invalid_grid, numbers=set([1,2]), groups=groups, constraints=constraints)
        for group_idx in range(len(groups)):
            result = csp.satisfies_sum_constraint(groups[group_idx], 3)
            self.assertFalse(result)


    def test_satisfies_count_constraint(self):
        horizontal_groups = [[(0,0),(0,1)], [(1,0), (1,1)]]
        vertical_groups = [[(0,0), (1,0)], [(0,1), (1,1)]]
        groups = horizontal_groups + vertical_groups
        # every constraint is of the form (sum, count). so every group must sum to 3 and every number may only occur once per group
        constraints = [(3, 1), (3, 1), (3, 1), (3, 1)]

        # note that not every cell belongs to a group
        valid_grid = np.array([[1,2,0],
                               [2,1,0]])
        csp = CSP(valid_grid, numbers=set([1,2]), groups=groups, constraints=constraints)
        for group_idx in range(len(groups)):
            result = csp.satisfies_count_constraint(groups[group_idx], 1)
            self.assertTrue(result)


        invalid_grid = np.array([[1,1],
                                 [1,1]])
        csp = CSP(invalid_grid, numbers=set([1,2]), groups=groups, constraints=constraints)
        for group_idx in range(len(groups)):
            result = csp.satisfies_count_constraint(groups[group_idx], 1)
            self.assertFalse(result)




    def test_satisfies_group_constraints(self):
        horizontal_groups = [[(0,0),(0,1)], [(1,0), (1,1)]]
        vertical_groups = [[(0,0), (1,0)], [(0,1), (1,1)]]
        groups = horizontal_groups + vertical_groups
        # every constraint is of the form (sum, count). so every group must sum to 3 and every number may only occur once per group
        constraints = [(3, 1), (3, 1), (3, 1), (3, 1)]

        valid_grid = np.array([[1,2],
                               [2,1]])
        csp = CSP(valid_grid, numbers=set([1,2]), groups=groups, constraints=constraints)
        self.assertTrue(csp.satisfies_group_constraints(list(range(len(groups)))))


        invalid_grid = np.array([[1,1],
                                 [0,1]])
        csp = CSP(invalid_grid, numbers=set([1,2]), groups=groups, constraints=constraints)
        self.assertFalse(csp.satisfies_group_constraints(list(range(len(groups)))))



    def test_search_simple(self):
        horizontal_groups = [[(0,0),(0,1)], [(1,0), (1,1)]]
        vertical_groups = [[(0,0), (1,0)], [(0,1), (1,1)]]
        groups = horizontal_groups + vertical_groups
        # every constraint is of the form (sum, count). so every group must sum to 3 and every number may only occur once per group
        constraints = [(3, 1), (3, 1), (3, 1), (3, 1)]

        valid_grid = np.array([[1,0],
                               [0,0]])
        csp = CSP(valid_grid, numbers=set([1,2]), groups=groups, constraints=constraints)
        result = csp.start_search()

        solution_grid = np.array([[1,2],
                                  [2,1]])

        self.assertTrue(np.all(solution_grid == result))

        # same but starting value is 2
        valid_grid = np.array([[2,0],
                               [0,0]])
        csp = CSP(valid_grid, numbers=set([1,2]), groups=groups, constraints=constraints)
        result = csp.start_search()

        solution_grid = np.array([[2,1],
                                  [1,2]])

        self.assertTrue(np.all(solution_grid == result))
        

    def test_search_simple_cells_not_in_groups(self):
        horizontal_groups = [[(0,0),(0,1)], [(1,0), (1,1)]]
        vertical_groups = [[(0,0), (1,0)], [(0,1), (1,1)]]
        groups = horizontal_groups + vertical_groups
        # every constraint is of the form (sum, count). so every group must sum to 3 and every number may only occur once per group
        constraints = [(3, 1), (3, 1), (3, 1), (3, 1)]

        valid_grid = np.array([[1,0,0],
                               [0,0,0]])
        csp = CSP(valid_grid, numbers=set([1,2]), groups=groups, constraints=constraints)
        result = csp.start_search()

        solution_grid = np.array([[1,2,0],
                                  [2,1,0]])

        self.assertTrue(np.all(solution_grid[:2,:2] == result[:2,:2]))

        # same but starting value is 2
        valid_grid = np.array([[2,0,0],
                               [0,0,0]])
        csp = CSP(valid_grid, numbers=set([1,2]), groups=groups, constraints=constraints)
        result = csp.start_search()

        solution_grid = np.array([[2,1,0],
                                  [1,2,0]])

        self.assertTrue(np.all(solution_grid[:2,:2] == result[:2,:2]))
    

    def test_search_medium(self):
        grid = np.array([
            [1,0,0],
            [3,0,0],
            [0,0,3],
        ])

        solution = np.array([
            [1,3,2],
            [3,2,1],
            [2,1,3],
        ])

        horizontal_groups = []
        for row_idx in range(3):
            groups = [(row_idx, j) for j in range(3)]
            horizontal_groups.append(groups)

        vertical_groups = []
        for col_idx in range(3):
            groups = [(j, col_idx) for j in range(3)]
            vertical_groups.append(groups)


        groups = horizontal_groups + vertical_groups
        constraints = [(sum([1,2,3]),1) for j in range(len(groups))]

        csp = CSP(grid, numbers=set([1,2,3]), groups=groups, constraints=constraints)
        result = csp.start_search()

        self.assertTrue(np.all(result == solution))


    def test_search_no_solution_no_overwriting(self):
        horizontal_groups = [[(0,0),(0,1)], [(1,0), (1,1)]]
        vertical_groups = [[(0,0), (1,0)], [(0,1), (1,1)]]
        groups = horizontal_groups + vertical_groups
        # every constraint is of the form (sum, count). so every group must sum to 3 and every number may only occur once per group
        constraints = [(3, 1), (3, 1), (3, 1), (3, 1)]

        valid_grid = np.array([[5,0],
                               [0,0]])
        csp = CSP(valid_grid, numbers=set([1,2]), groups=groups, constraints=constraints)
        result = csp.start_search()
        self.assertIsNone(result)