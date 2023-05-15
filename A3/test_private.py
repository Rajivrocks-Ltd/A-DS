import typing
import unittest
import numpy as np

from dynprog import DroneExtinguisher


class TestDroneExtinguisher(unittest.TestCase):

    def test_dyanmic_programming_no_solution(self):
        forest_location = (0, 0)
        bags = [2, 7, 20, 5, 2, 40]
        bag_locations = [(0, 0) for _ in range(len(bags))]  # no travel distance
        liter_cost_per_km = 1  # doesn't matter as there is no travel distance
        liter_budget_per_day = 30
        usage_cost = np.array([[1, 1, 0],
                               [1, 1, 0],
                               [1, 1, 0],
                               [1, 1, 0],
                               [1, 1, 0],
                               [1, 1, 0]])

        solution = np.inf

        de = DroneExtinguisher(
            forest_location=forest_location,
            bags=bags,
            bag_locations=bag_locations,
            liter_cost_per_km=liter_cost_per_km,
            liter_budget_per_day=liter_budget_per_day,
            usage_cost=usage_cost
        )

        de.fill_travel_costs_in_liters()
        de.dynamic_programming()
        lowest_cost = de.lowest_cost()
        # print(de.backtrace_solution())
        # for v in enumerate(de.backtrace_memory):
        #     print(v)
        self.assertEqual(lowest_cost, solution)

    def test_compute_sequence_usage_cost_invalid_i_j_range(self):
        forest_location = (0, 0)
        bags = [100, 200, 150, 120]
        bag_locations = [(1, 2), (3, 4), (5, 6), (7, 8)]
        liter_cost_per_km = 10
        liter_budget_per_day = 500
        usage_cost = np.array([[10, 20], [30, 40], [50, 60], [70, 80]])

        de = DroneExtinguisher(
            forest_location=forest_location,
            bags=bags,
            bag_locations=bag_locations,
            liter_cost_per_km=liter_cost_per_km,
            liter_budget_per_day=liter_budget_per_day,
            usage_cost=usage_cost
        )

        # Test case where i > j
        self.assertEqual(de.compute_sequence_usage_cost(2, 1, 0), 0.0)

        # Test case where i or j is out of range
        self.assertEqual(de.compute_sequence_usage_cost(5, 6, 0), 0.0)

        # Test case where k is out of range
        self.assertEqual(de.compute_sequence_usage_cost(2, 3, 5), 0.0)

    def test_compute_sequence_idle_time_in_liters_i_j_out_of_bounds(self):
        forest_location = (0, 0)
        bags = [100, 200, 150, 120]
        bag_locations = [(1, 2), (3, 4), (5, 6), (7, 8)]
        liter_cost_per_km = 10
        liter_budget_per_day = 500
        usage_cost = np.array([[10, 20], [30, 40], [50, 60], [70, 80]])

        de = DroneExtinguisher(
            forest_location=forest_location,
            bags=bags,
            bag_locations=bag_locations,
            liter_cost_per_km=liter_cost_per_km,
            liter_budget_per_day=liter_budget_per_day,
            usage_cost=usage_cost
        )

        # Test case where i or j is out of range
        self.assertEqual(de.compute_sequence_idle_time_in_liters(5,6), np.inf)
