import math
import numpy as np
import typing


class DroneExtinguisher:
    def __init__(self, forest_location: typing.Tuple[float, float], bags: typing.List[int],
                 bag_locations: typing.List[typing.Tuple[float, float]],
                 liter_cost_per_km: float, liter_budget_per_day: int, usage_cost: np.ndarray):
        """
        The DroneExtinguisher object. This object contains all functions necessary to compute the most optimal way of saving the forest
        from the fire using dynamic programming. Note that all costs that we use in this object will be measured in liters. 

        :param forest_location: the location (x,y) of the forest 
        :param bags: list of the contents of the water bags in liters
        :param bag_locations: list of the locations of the water bags
        :param liter_cost_per_km: the cost of traveling a kilometer with drones, measured in liters of waters 
        :param liter_budget_per_day: the maximum amount of work (in liters) that we can do per day 
                                     (sum of liter contents transported on the day + travel cost in liters)
        :param usage_cost: a 2D array. usage_cost[i,k] is the cost of flying water bag i with drone k from the water bag location to the forest
        """

        self.forest_location = forest_location
        self.bags = bags
        self.bag_locations = bag_locations
        self.liter_cost_per_km = liter_cost_per_km
        self.liter_budget_per_day = liter_budget_per_day
        self.usage_cost = usage_cost # usage_cost[i,k] = additional cost to use drone k to for bag i

        # the number of bags and drones that we have in the problem
        self.num_bags = len(self.bags)
        self.num_drones = self.usage_cost.shape[1] if not usage_cost is None else 1

        # list of the travel costs measured in the amount of liters of water
        # that could have been emptied in the forest (measured in integers)
        self.travel_costs_in_liters = []

        # idle_cost[i,j] is the amount of time measured in liters that we are idle on a day if we 
        # decide to empty bags[i:j+1] on that day
        self.idle_cost = -1*np.ones((self.num_bags, self.num_bags))

        # optimal_cost[i,k] is the optimal cost of emptying water bags[:i] with drones[:k+1]
        # this has to be filled in using the dynamic programming function
        self.optimal_cost = np.zeros((self.num_bags + 1, self.num_drones))

        # Data structure that can be used for the backtracing method (NOT backtracking):
        # reconstructing what bags we empty on every day in the forest
        self.backtrace_memory = dict()

    @staticmethod
    def compute_euclidean_distance(point1: typing.Tuple[float, float], point2: typing.Tuple[float, float]) -> float:
        """
        A static method (as it does not have access to the self. object) that computes the Euclidean
        distance between two points

        :param point1: an (x,y) tuple indicating the location of point 1
        :param point2: idem for point2

        Returns 
          float: the Euclidean distance between the two points
        """

        dx = point1[0] - point2[0]
        dy = point1[1] - point2[1]
        return math.sqrt(dx ** 2 + dy ** 2)


    def fill_travel_costs_in_liters(self):
        """
        Function that fills in the self.travel_costs_in_liters data structure such that
        self.travel_costs_in_liters[i] is the cost of traveling from the forest/drone housing
        to the bag AND back to the forest, measured in liters of waters (using liter_cost_per_km)
        Note: the cost in liters should be rounded up (with, e.g., np.ceil)
                
        The function does not return anything.  
        """
        for i in range(len(self.bag_locations)):
            # calculate distance between forest/drone housing and bag location
            distance = self.compute_euclidean_distance(self.forest_location, self.bag_locations[i])

            # calculate cost in liters using liter_cost_per_km
            cost_in_liters = np.ceil(distance * self.liter_cost_per_km * 2)

            # add cost to travel_costs_in_liters
            self.travel_costs_in_liters.append(cost_in_liters)


    def compute_sequence_idle_time_in_liters(self, i, j):
        """
        Function that computes the idle time (time not spent traveling to/from bags or emptying bags in the forest)
        in terms of liters. This function assumes that self.travel_costs_in_liters has already been filled with the
        correct values using the function above, as it makes use of that data structure.
        More specifically, this function computes the idle time on a day if we decide to empty self.bags[i:j+1] 
        (bag 0, bag 1, ..., bag j) on that day.

        Note: the returned idle time can be negative (if transporting the bags is not possible within a day) 

        :param i: integer index 
        :param j: integer index

        Returns:
          int: the amount of time (measured in liters) that we are idle on the day   
        """

        if self.idle_cost[i, j] != -1:
            return self.idle_cost[i, j]

        # Compute the amount of water in the bags
        total_water = sum(self.bags[i:j + 1])

        # Compute the total cost of transporting the bags to the forest and back
        total_cost = sum(self.travel_costs_in_liters[i:j + 1])

        # Compute the idle time
        idle_time = self.liter_budget_per_day - (total_water + total_cost)

        # Store the idle cost for later use
        # self.idle_cost[i, j] = idle_time

        return idle_time


    def compute_idle_cost(self, i, j, idle_time_in_liters):
        """
        Function that transforms the amount of time that we are idle on a day if we empty self.bags[i:j+1]
        on a day (idle_time_in_liters) into a quantity that we want to directly optimize using the formula
        in the assignment description.
        If transporting self.bags[i:j+1] is not possible within a day, we should return np.inf as cost.
        Moreover, if self.bags[i:j+1] are the last bags that are transported on the final day, the idle cost is 0
        as the operation has been completed. In all other cases, we use the formula from the assignment text.

        You may not need to use every argument of this function

        :param i: integer index
        :param j: integer index
        :param idle_time_in_liters: the amount of time that we are idle on a day measured in liters

        Returns
          - integer: the cost of being idle on a day corresponding to idle_time_in_liters
        """

        # Compute the total amount of water that needs to be transported
        total_liters = np.sum(self.bags[i:j+1])

        # If the bags are the last ones to be transported on the final day, the idle cost is 0
        if j == len(self.bags) - 1 and idle_time_in_liters > 0:
            return 0

        # If the amount of water is larger than the maximum amount that can be transported in a day,
        # return np.inf as cost (it is not possible to transport the water in a single day)
        if total_liters > self.liter_budget_per_day:
            return np.inf

        # if the total amount of liters = the daily budget there is no idle cost.
        if total_liters == self.liter_budget_per_day:
            return 0

        idle_cost = idle_time_in_liters ** len(self.bags)

        return idle_cost

        # ToDo

    def compute_sequence_usage_cost(self, i: int, j: int, k: int) -> float:
        """
        Function that computes and returns the cost of using drone k for self.bags[i:j+1], making use of
        self.usage_cost, which gives the cost for every bag-drone pair. 
        Note: the usage cost is independent of the distance to the forest. This is purely the operational cost
        to use drone k for bags[i:j+1].

        :param i: integer index
        :param j: integer index
        :param k: integer index

        Returns
          - float: the cost of usign drone k for bags[i:j+1] 
        """

        usage_cost = 0.0
        for bag_idx in range(i, j + 1):
            usage_cost += self.usage_cost[bag_idx][k]
        return usage_cost


    def dynamic_programming(self):
        """
        The function that uses dynamic programming to solve the problem: compute the optimal way of emptying bags in the forest
        per day and store a solution that can be used in the backtracing function below (if you want to do that assignment part). 
        In this function, we fill the memory structures self.idle_cost and self.optimal_cost making use of functions defined above. 
        This function does not return anything. 
        """

        # compute the idle time (time not spent traveling to/from bags or emptying bags in the forest)
        for i in range(self.num_bags):
            for j in range(i, self.num_bags):
                idle_time_in_liters = self.compute_sequence_idle_time_in_liters(i, j)
                idle_cost = self.compute_idle_cost(i, j, idle_time_in_liters)
                self.idle_cost[i, j] = idle_cost

        print("-"*20)
        print(self.idle_cost)
        print("-"*20 + "\n")


        # compute the optimal cost of emptying water bags[:i] with drones[:k+1]
        for i in range(1, self.num_bags):
            for k in range(self.num_drones):
                if i == 1:
                    self.optimal_cost[i, k] = self.idle_cost[0, 0] + self.usage_cost[0, k]
                else:
                    self.optimal_cost[i, k] = np.inf
                    for j in range(i):
                        if i <= self.num_bags:
                            cost = self.optimal_cost[j, k - 1] + self.idle_cost[j, i - 1] + self.usage_cost[i - 1, k]
                        else:
                            cost = np.inf
                        if cost < self.optimal_cost[i, k]:
                            self.optimal_cost[i, k] = cost
                            self.backtrace_memory[(i, k)] = j


        # TODO

    def lowest_cost(self) -> float:
        """
        Returns the lowest cost at which we can empty the water bags to extinguish to forest fire. Inside of this function,
        you can assume that self.dynamic_progrmaming() has been called so that in this function, you can simply extract and return
        the answer from the filled in memory structure.

        Returns:
          - float: the lowest cost
        """
        print(self.optimal_cost)
        return self.optimal_cost[-1][-1]

        # TODO


    def backtrace_solution(self) -> typing.List[int]:
        """
        Returns the solution of how the lowest cost was obtained by using, for example, self.backtrace_memory (but feel free to do it your own way). 
        The solution is a tuple (leftmost indices, drone list) as described in the assignment text. Here, leftmost indices is a list 
        [idx(1), idx(2), ..., idx(T)] where idx(i) is the index of the water bag that is emptied left-most (at the start of the day) on day i. 
        Drone list is a list [d(0), d(1), ..., d(num_bags-1)] where d(j) tells us which drone was used in the optimal
        solution to transport water bag j.  
        See the assignment description for an example solution. 

        This function does not have to be made - you can still pass the assignment if you do not hand this in,
        however it will cost a full point if you do not do this (and the corresponding question in the report).  
            
        :return: A tuple (leftmost indices, drone list) as described above
        """

        # TODO
        raise NotImplementedError()
