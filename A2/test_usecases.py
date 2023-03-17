import typing
import unittest
import numpy as np

from divconq import IntelDevice


class TestIntelDevice(unittest.TestCase):

    def test_encode_message(self):
        # without caesar shift
        ob = IntelDevice(3,5,[],[],0)
        answers =[
            "1000011 1101100 1100001 1110011 1110011 1101001 1100110 1101001 1100101 1100100 100000 1101001 1101110 1100110 1101111 1110010 1101101 1100001 1110100 1101001 1101111 1101110",
            "1001100 1100101 1101001 1100100 1100101 1101110 100000 1010101 1101110 1101001 1110110 1100101 1110010 1110011 1101001 1110100 1111001",
            "1000001 1101100 1100111 1101111 1110010 1101001 1110100 1101000 1101101 1110011 100000 1100001 1101110 1100100 100000 1000100 1100001 1110100 1100001 100000 1010011 1110100 1110010 1110101 1100011 1110100 1110101 1110010 1100101 1110011"
        ] 
        queries = ["Classified information", "Leiden University", "Algorithms and Data Structures"]
        
        for query, answer in zip(queries, answers):
            self.assertEqual(ob.encode_message(query),answer)

        # with caesar shift 8
        ob = IntelDevice(3,5,[],[],8)
        answers =[
            "1001011 1110100 1101001 1111011 1111011 1110001 1101110 1110001 1101101 1101100 101000 1110001 1110110 1101110 1110111 1111010 1110101 1101001 1111100 1110001 1110111 1110110",
            "1010100 1101101 1110001 1101100 1101101 1110110 101000 1011101 1110110 1110001 1111110 1101101 1111010 1111011 1110001 1111100 10000001",
            "1001001 1110100 1101111 1110111 1111010 1110001 1111100 1110000 1110101 1111011 101000 1101001 1110110 1101100 101000 1001100 1101001 1111100 1101001 101000 1011011 1111100 1111010 1111101 1101011 1111100 1111101 1111010 1101101 1111011"
        ] 
        queries = ["Classified information", "Leiden University", "Algorithms and Data Structures"]
        
        for query, answer in zip(queries, answers):
            self.assertEqual(ob.encode_message(query),answer)

    
    def test_decode_message(self):
        # without caesar shift
        ob = IntelDevice(3,5,[],[],0)
        queries =[
            "1000011 1101100 1100001 1110011 1110011 1101001 1100110 1101001 1100101 1100100 100000 1101001 1101110 1100110 1101111 1110010 1101101 1100001 1110100 1101001 1101111 1101110",
            "1001100 1100101 1101001 1100100 1100101 1101110 100000 1010101 1101110 1101001 1110110 1100101 1110010 1110011 1101001 1110100 1111001",
            "1000001 1101100 1100111 1101111 1110010 1101001 1110100 1101000 1101101 1110011 100000 1100001 1101110 1100100 100000 1000100 1100001 1110100 1100001 100000 1010011 1110100 1110010 1110101 1100011 1110100 1110101 1110010 1100101 1110011"
        ] 
        answers = ["Classified information", "Leiden University", "Algorithms and Data Structures"]
        
        for query, answer in zip(queries, answers):
            self.assertEqual(ob.decode_message(query),answer)

        # with caesar shift 8
        ob = IntelDevice(3,5,[],[],8)
        queries =[
            "1001011 1110100 1101001 1111011 1111011 1110001 1101110 1110001 1101101 1101100 101000 1110001 1110110 1101110 1110111 1111010 1110101 1101001 1111100 1110001 1110111 1110110",
            "1010100 1101101 1110001 1101100 1101101 1110110 101000 1011101 1110110 1110001 1111110 1101101 1111010 1111011 1110001 1111100 10000001",
            "1001001 1110100 1101111 1110111 1111010 1110001 1111100 1110000 1110101 1111011 101000 1101001 1110110 1101100 101000 1001100 1101001 1111100 1101001 101000 1011011 1111100 1111010 1111101 1101011 1111100 1111101 1111010 1101101 1111011"
        ] 
        answers = ["Classified information", "Leiden University", "Algorithms and Data Structures"]
        
        for query, answer in zip(queries, answers):
            self.assertEqual(ob.decode_message(query),answer)

    def test_fill_coordinate_to_loc(self):
        enc_locations = [
            "1011010 1110111 1111100 1111100 1101101 1111010 1101100 1101001 1110101", # Rotterdam
            "1001100 1101101 1110100 1101110 1111100", # Delft
            "1010100 1101101 1110001 1101100 1101101 1110110", # Leiden
            "1001010 1101101 1111010 1110100 1110001 1110010 1110110", # Berlijn
            "1011000 1110111 1111010 1111100 1110111", # Porto
            "1010011 1110001 1101101 1111110" # Kiev
        ]

        ob = IntelDevice(3,2,enc_locations,[],8)

        ob.fill_coordinate_to_loc()

        solution = {
            (0,0): "Rotterdam",
            (0,1): "Delft",
            (0,2): "Leiden",
            (1,0): "Berlijn",
            (1,1): "Porto",
            (1,2): "Kiev"
        }

        for key, value in solution.items():
            self.assertTrue(ob.coordinate_to_location[key] == value)

    def test_fill_loc_grid(self):
        # the encoded codes are 1,4,7,2,5,8,3,6,9
        enc_codes = ['110110', '111001', '111100', '110111', '111010', '111101', '111000', '111011', '111110']
        ob = IntelDevice(3,3,[],enc_codes, 5)
        ob.fill_loc_grid()

        solution = np.array([
            [1,4,7],
            [2,5,8],
            [3,6,9]
        ])

        self.assertTrue(np.all(ob.loc_grid == solution))

    def test_search_solution(self):
        a = np.array([
            [1,10,30],
            [16,20,42],
            [32,47,57]
        ])


        raw_locations = [f"l{i}" for i in range(9)]
        raw_codes = [str(x) for x in a.reshape(-1)]

        enc_locations = [
            "1101110 110010", #l1
            "1101110 110011", #l2
            "1101110 110100", #l3
            "1101110 110101", #etc
            "1101110 110110",
            "1101110 110111",
            "1101110 111000",
            "1101110 111001",
            "1101110 111010"
        ]

        enc_codes = [
            "110011",
            "110011 110010",
            "110101 110010",
            "110011 111000",
            "110100 110010",
            "110110 110100",
            "110101 110100",
            "110110 111001",
            "110111 111001"
        ]

        solutions = [
            "1101110 110010", #l1
            "1101110 110011", #l2
            "1101110 110100", #l3
            "1101110 110101", #etc
            "1101110 110110",
            "1101110 110111",
            "1101110 111000",
            "1101110 111001",
            "1101110 111010"
        ]

        ob = IntelDevice(3,3, enc_locations, enc_codes, 2)
        ob.fill_coordinate_to_loc()
        ob.fill_loc_grid()

        # values that occur in the 2d grid
        for vid, v in enumerate(a.reshape(-1)):
            if v == 20:
                continue
            result = ob.start_search(v)
            self.assertEqual(result, solutions[vid])
        
        # values that do not occur should lead to None
        for v in [0,2,14,18,31,48,60]:
            result = ob.start_search(v)
            self.assertIsNone(result)


    def test_search_solution_even(self):
        a = np.array([
            [1, 10,30,51],
            [16,20,42,52],
            [32,47,57,80]
        ])

        raw_locations = [f"l{i}" for i in range(12)]
        raw_codes = [str(x) for x in a.reshape(-1)]

        shift = 2


        enc_locations = [
            "1101110 110010",
            "1101110 110011",
            "1101110 110100",
            "1101110 110101",
            "1101110 110110",
            "1101110 110111",
            "1101110 111000",
            "1101110 111001",
            "1101110 111010",
            "1101110 111011",
            "1101110 110011 110010",
            "1101110 110011 110011"
        ]

        enc_codes = [
            "110011",
            "110011 110010",
            "110101 110010",
            "110111 110011",
            "110011 111000",
            "110100 110010",
            "110110 110100",
            "110111 110100",
            "110101 110100",
            "110110 111001",
            "110111 111001",
            "111010 110010",
        ]

        solutions = [
            "1101110 110010",
            "1101110 110011",
            "1101110 110100",
            "1101110 110101",
            "1101110 110110",
            "1101110 110111",
            "1101110 111000",
            "1101110 111001",
            "1101110 111010",
            "1101110 111011",
            "1101110 110011 110010",
            "1101110 110011 110011"
        ]

        ob = IntelDevice(4,3, enc_locations, enc_codes, 2)
        ob.fill_coordinate_to_loc()
        ob.fill_loc_grid()

        # values that occur in the 2d grid
        for vid, v in enumerate(a.reshape(-1)):
            if v == 20:
                continue
            result = ob.start_search(v)
            self.assertEqual(result, solutions[vid])

        # values that do not occur should lead to None
        for v in [0,2,14,18,31,48,60]:
            result = ob.start_search(v)
            self.assertIsNone(result)

