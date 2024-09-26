import sys
import math
import random
from copy import deepcopy

# Parsing the input file
def parse_input(file_path):
    loads = []
    with open(file_path, 'r') as f:
        next(f)
        for line in f:
            parts = line.strip().split()
            load_id = int(parts[0])
            pickup = tuple(map(float, parts[1].strip('()').split(',')))
            dropoff = tuple(map(float, parts[2].strip('()').split(',')))
            loads.append((load_id, pickup, dropoff))
    return loads

# Cache for distance calculations
distance_cache = {}

# Euclidean distance function with caching
def cached_euclidean_distance(x1, y1, x2, y2):
    key = (x1, y1, x2, y2)
    if key not in distance_cache:
        distance_cache[key] = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance_cache[key]

# Calculate the total travel time for a driver
def calculate_route_time(driver):
    total_time = 0
    last_x, last_y = 0, 0
    for load in driver:
        pickup, dropoff = load[1], load[2]
        total_time += cached_euclidean_distance(last_x, last_y, *pickup)
        total_time += cached_euclidean_distance(*pickup, *dropoff)
        last_x, last_y = dropoff
    total_time += cached_euclidean_distance(last_x, last_y, 0, 0)
    return total_time

# Calculate total cost of the solution
def calculate_total_cost(drivers):
    total_minutes = sum(calculate_route_time(driver) for driver in drivers)
    return 500 * len(drivers) + total_minutes

# Check if each driver's route stays within 720 minutes
def is_solution_feasible(drivers, time_limit=720):
    for driver in drivers:
        if calculate_route_time(driver) > time_limit:
            return False
    return True

# Greedy Savings Heuristic for initial solution
def greedy_savings_heuristic(loads, depot=(0, 0), time_limit=720):
    routes = [[load] for load in loads]
    savings = []
    
    # Calculate savings for each pair of loads
    for i in range(len(loads)):
        for j in range(i + 1, len(loads)):
            load1 = loads[i]
            load2 = loads[j]
            savings_value = calculate_savings(depot, load1, load2)
            savings.append((savings_value, load1, load2))
    
    savings.sort(reverse=True, key=lambda x: x[0])
    
    # Merge routes based on savings
    for saving in savings:
        _, load1, load2 = saving
        route1, route2 = None, None
        
        for route in routes:
            if load1 in route:
                route1 = route
            if load2 in route:
                route2 = route
        
        if route1 != route2 and route1 and route2:
            best_merge, best_time = try_merge(route1, route2, time_limit)
            if best_merge:
                routes.remove(route1)
                routes.remove(route2)
                routes.append(best_merge)
    
    return routes

# Calculate savings for two loads
def calculate_savings(depot, load1, load2):
    dist_depot_1 = cached_euclidean_distance(*depot, *load1[1])
    dist_depot_2 = cached_euclidean_distance(*depot, *load2[1])
    dist_1_2 = cached_euclidean_distance(*load1[2], *load2[1])
    return dist_depot_1 + dist_depot_2 - dist_1_2

# Function to calculate the best way to merge two routes
def try_merge(route1, route2, time_limit):
    best_merge = None
    best_time = float('inf')

    limit = 10
    for i in range(min(limit, len(route1) + 1)):
        for j in range(min(limit, len(route2) + 1)):
            merged_route = route1[:i] + route2 + route1[i:]
            route_time = calculate_route_time(merged_route)
            
            if route_time <= time_limit and route_time < best_time:
                best_merge = merged_route
                best_time = route_time
    
    return best_merge, best_time

# Simulated Annealing with adaptive neighborhood exploration
def simulated_annealing(drivers, time_limit, initial_temp=8000, cooling_rate=0.9995, max_iters=20000):
    current_solution = drivers
    current_cost = calculate_total_cost(drivers)
    best_solution = deepcopy(current_solution)
    best_cost = current_cost

    temperature = initial_temp

    iteration = 0
    
    while iteration < max_iters and temperature > 1e-4:
        new_solution = generate_adaptive_neighbor(current_solution, iteration, max_iters)
        
        if is_solution_feasible(new_solution, time_limit):
            new_cost = calculate_total_cost(new_solution)
            
            if new_cost < current_cost or random.random() < math.exp((current_cost - new_cost) / temperature):
                current_solution = new_solution
                current_cost = new_cost

            if current_cost < best_cost:
                best_solution = deepcopy(current_solution)
                best_cost = current_cost
        
        temperature *= cooling_rate
        iteration += 1

    return best_solution

# Adaptive neighborhood generation based on iteration count
def generate_adaptive_neighbor(drivers, iteration, max_iters):
    new_drivers = deepcopy(drivers)
    
    if iteration < max_iters * 0.5:
        if random.random() < 0.5:
            # Swap 2-4 loads between two drivers
            driver1, driver2 = random.sample(new_drivers, 2)
            if driver1 and driver2 and len(driver1) > 3 and len(driver2) > 3:
                loads1 = random.sample(driver1, random.randint(2, 4))
                loads2 = random.sample(driver2, random.randint(2, 4))
                for load1, load2 in zip(loads1, loads2):
                    driver1[driver1.index(load1)], driver2[driver2.index(load2)] = load2, load1
        else:
            # Move 2-4 loads from one driver to another
            driver1, driver2 = random.sample(new_drivers, 2)
            if driver1 and len(driver1) > 3:
                loads_to_move = random.sample(driver1, random.randint(2, 4))
                for load in loads_to_move:
                    driver1.remove(load)
                    driver2.append(load)
    else:
        if random.random() < 0.5:
            # Swap 1-2 loads between two drivers
            driver1, driver2 = random.sample(new_drivers, 2)
            if driver1 and driver2 and len(driver1) > 1 and len(driver2) > 1:
                load1 = random.choice(driver1)
                load2 = random.choice(driver2)
                driver1[driver1.index(load1)], driver2[driver2.index(load2)] = load2, load1
        else:
            # Move 1-2 loads from one driver to another
            driver1, driver2 = random.sample(new_drivers, 2)
            if driver1 and len(driver1) > 1:
                load_to_move = random.choice(driver1)
                driver1.remove(load_to_move)
                driver2.append(load_to_move)
    
    return new_drivers

# Post-Optimization
def post_optimization_cleanup(drivers, time_limit):
    improved = True
    while improved:
        improved = False
        for i in range(len(drivers)):
            for j in range(i + 1, len(drivers)):
                driver1, driver2 = drivers[i], drivers[j]
                if driver1 and driver2:
                    best_merge, best_time = try_merge(driver1, driver2, time_limit)
                    if best_merge and calculate_route_time(best_merge) < calculate_route_time(driver1) + calculate_route_time(driver2):
                        drivers[i] = best_merge
                        drivers[j] = []
                        improved = True

    drivers = [driver for driver in drivers if driver]
    return drivers

# VRP solution
def vrp_solver(input_file):
    loads = parse_input(input_file)

    time_limit = 720
    
    drivers = greedy_savings_heuristic(loads, time_limit=time_limit)
    
    optimized_drivers = simulated_annealing(drivers, time_limit, initial_temp=8000, cooling_rate=0.9995, max_iters=20000)
    
    final_drivers = post_optimization_cleanup(optimized_drivers, time_limit)
    
    for driver in final_drivers:
        print([load[0] for load in driver])

# Main function
if __name__ == "__main__":
    input_file = sys.argv[1]
    vrp_solver(input_file)