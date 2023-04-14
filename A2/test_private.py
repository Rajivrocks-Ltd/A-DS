import typing
import unittest
import numpy as np

from divconq import IntelDevice


class TestIntelDevice(unittest.TestCase):


    def test_handle_empty_enc_codes(self):
        device = IntelDevice(2, 2, ['0000', '1111', '0000', '1111'], [], 0)
        self.assertEqual(device.loc_grid.tolist(), [[0, 0], [0, 0]])
        self.assertEqual(device.coordinate_to_location, {})

    def test_handle_empty_enc_location(self):
        device = IntelDevice(2, 2, [], ['0000', '1111', '0000', '1111'], 0)
        self.assertEqual(device.loc_grid.tolist(), [[0, 0], [0, 0]])
        self.assertEqual(device.coordinate_to_location, {})

    def test_search_solution_negative_grid(self):
        a = np.array([
            [-57, -47, -32],
            [-42, -20, -16],
            [-30, -10, -1]
        ])

        enc_locations = [
            "1101110 110010",  # l1
            "1101110 110011",  # l2
            "1101110 110100",  # l3
            "1101110 110101",  # etc
            "1101110 110110",
            "1101110 110111",
            "1101110 111000",
            "1101110 111001",
            "1101110 111010"
        ]

        enc_codes = [
            "101111 110111 111001",
            "101111 110110 111001",
            "101111 110101 110100",
            "101111 110110 110100",
            "101111 110100 110010",
            "101111 110011 111000",
            "101111 110101 110010",
            "101111 110011 110010",
            "101111 110011",
        ]

        solutions = [
            "1101110 110010",  # l1
            "1101110 110011",  # l2
            "1101110 110100",  # l3
            "1101110 110101",  # etc
            "1101110 110110",
            "1101110 110111",
            "1101110 111000",
            "1101110 111001",
            "1101110 111010"
        ]

        ob = IntelDevice(3, 3, enc_locations, enc_codes, 2)
        ob.fill_coordinate_to_loc()
        ob.fill_loc_grid()

        # values that occur in the 2d grid
        for vid, v in enumerate(a.reshape(-1)):
            result = ob.start_search(v)
            self.assertEqual(result, solutions[vid])

        # values that do not occur should lead to None
        for v in [0, 2, 14, 18, 31, 48, 60]:
            result = ob.start_search(v)
            self.assertIsNone(result)