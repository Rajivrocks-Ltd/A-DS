import time
import typing

import matplotlib.pyplot as plt
import numpy as np

counter = 0
def naive_linear_scan(grid, value):
    num_cells_searched = 0
    for y, row in enumerate(grid):
        for x, cell_value in enumerate(row):
            num_cells_searched += 1
            if cell_value == value:
                return num_cells_searched
    return num_cells_searched


def div_con_search(value: int, x_from: int, x_to: int, y_from: int, y_to: int,
                   search_grid: typing.List[typing.List[int]], countvar: int) -> typing.Tuple[int, int, int]:

    # Check if the search range is valid
    if x_from > x_to or y_from > y_to:
        return None, None, countvar

    # Check if the range contains zero elements
    if x_from == x_to and y_from == y_to:
        countvar += 1
        if search_grid[y_from][x_from] == value:
            return (y_from, x_from, countvar)
        else:
            return None, None, countvar

    mid_x = (x_from + x_to) // 2
    mid_y = (y_from + y_to) // 2

    # Check if the middle element matches the search value
    mid_val = search_grid[mid_y][mid_x]
    countvar += 1
    if mid_val == value:
        return (mid_y, mid_x, countvar)

    if mid_val > value:
        # Recursively search the top-left quadrant
        y, x, count_tl = div_con_search(value, x_from, mid_x, y_from, mid_y, search_grid, countvar)
        if all(item is not None for item in (y, x)):
            return (y , x, count_tl + 1)

        # Recursively search the top-right quadrant
        y, x, count_tr = div_con_search(value, mid_x + 1, x_to, y_from, mid_y, search_grid, countvar)
        if all(item is not None for item in (y, x)):
            return (y, x, count_tr + 1)

        # Recursively search the bottom-left quadrant
        y, x, count_bl = div_con_search(value, x_from, mid_x, mid_y + 1, y_to, search_grid, countvar)
        if all(item is not None for item in (y, x)):
            return (y, x, count_bl + 1)

        countvar += count_tl
        countvar += count_tr
        # countvar += count_bl

    else:
        # Recursively search the top-right quadrant
        y, x, count_tr = div_con_search(value, mid_x + 1, x_to, y_from, mid_y, search_grid, countvar)
        if all(item is not None for item in (y, x)):
            return (y, x, count_tr + 1)

        # Recursively search the bottom-left quadrant
        y, x, count_bl = div_con_search(value, x_from, mid_x, mid_y + 1, y_to, search_grid, countvar)
        if all(item is not None for item in (y, x)):
            return (y, x, count_bl + 1)

        # Check if the search value is in the bottom-right quadrant
        y, x, count_br = div_con_search(value, mid_x + 1, x_to, mid_y + 1, y_to, search_grid, countvar)
        if all(item is not None for item in (y, x)):
            return (y, x, count_br + 1)

        # countvar += count_br
        countvar += count_bl
        countvar += count_tr

    # If the search value is not found in any quadrant, return None
    return None, None, countvar


def generate_grid(size):
    two_d_grid = np.arange(1, size*size+1).reshape(size, size)
    return two_d_grid

grid_sizes = [5]
linear_scan_cells = []
divconq_cells = []
linear_scan_times = []
divconq_times = []

res = np.array([[1,2,3],
                [4,5,6],
               [7,8,9]])

x = res.reshape(-1)

for num in x:
    search_value = num

    start_time = time.perf_counter()
    divconq_result = div_con_search(search_value, 0, 4 - 1, 0, 3 - 1, res, 0)
    divconq_time = time.perf_counter() - start_time
    divconq_cells.append(divconq_result)
    divconq_times.append(divconq_time)

print(divconq_cells)

# for size in grid_sizes:
#     counter = 0
#     grid = generate_grid(size)
#     search_value = grid[-1][-1]
#
#     start_time = time.perf_counter()
#     linear_scan_result = naive_linear_scan(grid, search_value)
#     linear_scan_time = time.perf_counter() - start_time
#     linear_scan_cells.append(linear_scan_result)
#     linear_scan_times.append(linear_scan_time)
#
#     start_time = time.perf_counter()
#     divconq_result = div_con_search(search_value, 0, size - 1, 0, size - 1, grid, 0)
#     divconq_time = time.perf_counter() - start_time
#     divconq_cells.append(divconq_result[2])
#     divconq_times.append(divconq_time)

# for item in divconq_cells:
#     print(item)
#
# print("-"*50)
# for item in divconq_times:
#     print(item)
#
# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
#
# ax1.plot(grid_sizes, linear_scan_cells, 'r', label='Naive Linear Scan')
# ax1.plot(grid_sizes, divconq_cells, 'b', label='Divide and Conquer')
# ax1.set_xlabel('Grid Size')
# ax1.set_ylabel('Cells Searched')
# ax1.legend()
#
# ax2.plot(grid_sizes, linear_scan_times, 'r', label='Naive Linear Scan')
# ax2.plot(grid_sizes, divconq_times, 'b', label='Divide and Conquer')
# ax2.set_xlabel('Grid Size')
# ax2.set_ylabel('Time (s)')
# ax2.legend()

plt.show()
