##################################################################################
# It is not allowed to add imports here. Use these two packages and nothing else.
import numpy as np
import typing
##################################################################################


class CSP:
    def __init__(self, grid:np.ndarray, numbers: typing.Set[int], groups: typing.List[typing.List[typing.Tuple[int,int]]],
                 constraints: typing.List[typing.Tuple[int,int]]):
        
        """
        The CSP solver object, containing all information and functions required for the assignment. You do not need to change
        this function.

        :param grid: 2-d numpy array corresponding to the grid that we have to fill in. Empty squares are denoted with 0s.
        :param numbers: The set of numbers that we are allowed to use in order to fill the grid (can be any set of integers)
        :param groups: A list of cell groups (cell groups are lists of location tuples).
        :param constraints: The list of constraints for every group of cells. constraints[i] hold for groups[i]. Every
                            constraint is a tuple of the form (sum_of_elements, max_count_element) where sum_of_elements 
                            indicates what the sum must be of the elements of the given group, and max_count_element indicates
                            the maximum number of times that a number/element may occur in the given group
        """

        self.width = grid.shape[1]
        self.height = grid.shape[0]
        self.numbers = numbers
        self.groups = groups
        self.constraints = constraints

        self.grid = grid
        self.cell_to_groups = {(row_idx, col_idx): [] for row_idx in range(self.height) for col_idx in range(self.width)}


    def fill_cell_to_groups(self):
        """
        Function that fills in the self.cell_to_groups datastructure, which maps a cell location (row_idx, col_idx)
        to a list of groups of which it is a member. For example, suppose that cell (0,0) is member of groups 0, 1,
        and 2. Then, self.cell_to_groups[(0,0)] should be equal to [0,1,2]. This function should do this for every cell. 
        If a cell is not a member of any groups, self.cell_to_groups[cell] should be an empty list []. 
        The function does not return anything. 

        Before completing this function, make sure to read the assignment description and study the data structures created
        in the __init__ function above (self.groups and self.cell_to_groups).
        """

        # loop over each group
        for i in range(len(self.groups)):
            # loop over each cell in the group
            for cell in self.groups[i]:
                # if the cell has not been added to any group yet, add it to this one
                if cell not in self.cell_to_groups:
                    self.cell_to_groups[cell] = [i]
                # if the cell has been added to a group before, add this group to the list of groups for the cell
                else:
                    self.cell_to_groups[cell].append(i)



    def satisfies_sum_constraint(self, group: typing.List[typing.Tuple[int,int]], sum_constraint: int) -> bool:
        """
        Function that checks whether the given group satisfies the given sum constraint (group smaller or equal 
        than sum). Returns True if the current group satisfies the constraint and False otherwise. 

        :param group: The list of locations [loc1, loc2, loc3,...,locN] that specify the group. Here, every loc is 
                      a tuple (row_idx, col_idx) of indices, specifying the row and column of the cell. 
        :param sum_constraint: The sum_of_elements constraint specifying that the numbers in the given group must
                               sum up to this number. This is None if there is no sum constraint for the given group. 
        """
        # Adjust this a bit because this is probably an easy one which will always geenrate this block of code.

        # group_sum = sum(self.grid[row_idx][col_idx] for row_idx, col_idx in group)
        # return group_sum <= sum_constraint if sum_constraint is not None else True

        # Calculate the sum of the numbers in the group using a for loop
        group_sum = 0
        for row_idx, col_idx in group:
            group_sum += self.grid[row_idx][col_idx]

        # Check if the sum of the group satisfies the given sum_constraint
        if sum_constraint is not None:
            return group_sum <= sum_constraint
        else:
            return True

    
    def satisfies_count_constraint(self, group: typing.List[typing.Tuple[int,int]], count_constraint: int) -> bool:
        """
        Function that checks whether the given group satisfies the given count constraint.
        Returns True if the current group satisfies the constraint and False otherwise. 
        Recall that the value of 0 indicates an empty cell (0s should not count towards the count constraint).

        :param group: The list of locations [loc1, loc2, loc3,...,locN] that specify the group. Here, every loc is 
                      a tuple (row_idx, col_idx) of indices, specifying the row and column of the cell. 
        :param count_constraint: Integer specifying that a given number cannot occur more than this amount of times. 
                                 This is None if there is no count constraint for the given group. 
        """

        # Create an empty dictionary to store the count of each value in the group.
        counts = {}
        # Iterate over each cell in the group.
        for row_idx, col_idx in group:
            # Get the value of the current cell.
            value = self.grid[row_idx][col_idx]
            # If the value is not 0, increment its count in the dictionary.
            if value != 0:
                if value in counts:
                    counts[value] += 1
                else:
                    counts[value] = 1
        # If the dictionary is empty, then the group is vacuously true for any count constraint.
        if not counts:
            return True
        # If there is no count constraint, then the group satisfies any possible count.
        if count_constraint is None:
            return True
        # Check that the count of each value is less than or equal to the count constraint.
        return all(count <= count_constraint for count in counts.values())



    def satisfies_group_constraints(self, group_indices: typing.List[int]) -> bool:
        """
        Function that checks whether the constraints for the given group indices are satisfied.
        Returns True if all relevant constraints are satisfied, False otherwise. Make sure to use functions defined above. 

        :param group_indices: The indices of the groups for which we check all of the constraints 
        """

        # Loop over groups to check their constraints
        for group in group_indices:
            res = []
            # Get sum and count constraints for this group
            sum_const, count_const = self.constraints[group]
            # Check whether sum constraint is satisfied
            res.append(self.satisfies_sum_constraint(self.groups[group], sum_const))
            # Check whether count constraint is satisfied
            res.append(self.satisfies_count_constraint(self.groups[group], count_const))
            # If any of the constraints are not satisfied, return False
            if not all(res):
                return False

        # Everything passed
        return True

    def search(self, empty_locations: typing.List[typing.Tuple[int, int]]) -> np.ndarray:
        """
        Recursive exhaustive search function. It tries to fill in the empty_locations with permissible values
        in an attempt to find a valid solution that does not violate any of the constraints. Instead of checking all
        possible constraints after filling in a number, it checks only the relevant group constraints using the
        self.cell_to_groups data structure.

        Returns None if there is no solution. Returns the filled in solution (self.grid) otherwise if a solution is found.

        :param empty_locations: list of empty locations that still need a value from self.numbers
        """

        if not empty_locations:
            # Base case: all empty locations have been filled, check if the grid is valid
            if self.satisfies_group_constraints(list(range(len(self.groups)))):
                return self.grid
            else:
                return None

        row, col = empty_locations[0]
        for num in self.numbers:
            if self.grid[row, col] == 0:
                self.grid[row, col] = num
                # Continue the search with the remaining empty locations
                solution = self.search(empty_locations[1:])
                if solution is not None:
                    # If a solution is found, return it
                    return solution
                self.grid[row, col] = 0  # backtrack

        # If none of the permissible values leads to a solution, return None
        return None

    

    def start_search(self):
        """
        Non-recursive function that starts the recursive search function above. It first fills the cell_to_group
        data structure and computes the empty locations. Then, it starts the recursive search procedure. 
        The result is None if there is no solution possible. Otherwise, it returns the grid that is a solution.

        You do not need to change this function.
        """

        self.fill_cell_to_groups()
        empty_locations = [(row_idx, col_idx) for row_idx in range(self.height) for col_idx in range(self.width) if self.grid[row_idx,col_idx]==0]
        return self.search(empty_locations)
    
