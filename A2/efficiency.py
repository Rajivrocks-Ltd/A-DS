import time
import typing

import matplotlib.pyplot as plt
import numpy as np


def naive_linear_scan(grid, value):
    num_cells_searched = 0
    for y, row in enumerate(grid):
        for x, cell_value in enumerate(row):
            num_cells_searched += 1
            if cell_value == value:
                return num_cells_searched
    return num_cells_searched


def divconq_search(value: int, x_from: int, x_to: int, y_from: int, y_to: int, cells_searched: int,
                   search_grid: typing.List[typing.List[int]]) -> typing.Tuple[int, int, int]:

    # Check if the search range is valid
    if x_from > x_to or y_from > y_to:
        return None

    # Check if the range contains zero elements
    if x_from == x_to and y_from == y_to:
        cells_searched += 1
        if search_grid[y_from][x_from] == value:
            return (y_from, x_from, cells_searched)
        else:
            return None

    mid_x = (x_from + x_to) // 2
    mid_y = (y_from + y_to) // 2

    # Check if the middle element matches the search value
    mid_val = search_grid[mid_y][mid_x]
    if mid_val == value:
        cells_searched += 1
        return (mid_y, mid_x, cells_searched)

    if mid_val > value:
        # Recursively search the top-left quadrant
        top_left = divconq_search(value, x_from, mid_x, y_from, mid_y, cells_searched, search_grid)
        if top_left is not None:
            return top_left

        # Recursively search the top-right quadrant
        top_right = divconq_search(value, mid_x + 1, x_to, y_from, mid_y, cells_searched, search_grid)
        if top_right is not None:
            return top_right

        # Recursively search the bottom-left quadrant
        bottom_left = divconq_search(value, x_from, mid_x, mid_y + 1, y_to, cells_searched, search_grid)
        if bottom_left is not None:
            return bottom_left

    else:
        # Recursively search the top-right quadrant
        top_right = divconq_search(value, mid_x + 1, x_to, y_from, mid_y, cells_searched, search_grid)
        if top_right is not None:
            return top_right

        # Recursively search the bottom-left quadrant
        bottom_left = divconq_search(value, x_from, mid_x, mid_y + 1, y_to, cells_searched, search_grid)
        if bottom_left is not None:
            return bottom_left

        # Check if the search value is in the bottom-right quadrant
        bottom_right = divconq_search(value, mid_x + 1, x_to, mid_y + 1, y_to, cells_searched, search_grid)
        if bottom_right is not None:
            return bottom_right

    # If the search value is not found in any quadrant, return None
    return None


def generate_grid(size):
    grid = [[(i * size) + j + 1 for j in range(size)] for i in range(size)]
    return grid


grid_sizes = [3, 10, 50, 100, 200, 400, 800, 1600, 3200, 6400, 9600, 19200]
linear_scan_cells = []
divconq_cells = []
linear_scan_times = []
divconq_times = []

for size in grid_sizes:
    grid = generate_grid(size)
    search_value = grid[-1][-1]

    start_time = time.perf_counter()
    linear_scan_result = naive_linear_scan(grid, search_value)
    linear_scan_time = time.perf_counter() - start_time
    linear_scan_cells.append(linear_scan_result)
    linear_scan_times.append(linear_scan_time)

    start_time = time.perf_counter()
    divconq_result = divconq_search(search_value, 0, size - 1, 0, size - 1, 0, grid)
    divconq_time = time.perf_counter() - start_time
    divconq_cells.append(divconq_result[2])
    divconq_times.append(divconq_time)

print("-"*50)
for item in linear_scan_times:
    print(item)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

ax1.plot(grid_sizes, linear_scan_cells, 'r', label='Naive Linear Scan')
ax1.plot(grid_sizes, divconq_cells, 'b', label='Divide and Conquer')
ax1.set_xlabel('Grid Size')
ax1.set_ylabel('Cells Searched')
ax1.legend()

ax2.plot(grid_sizes, linear_scan_times, 'r', label='Naive Linear Scan')
ax2.plot(grid_sizes, divconq_times, 'b', label='Divide and Conquer')
ax2.set_xlabel('Grid Size')
ax2.set_ylabel('Time (s)')
ax2.legend()

plt.show()