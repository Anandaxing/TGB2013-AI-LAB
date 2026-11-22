from math import ceil
import random

# Fixed seed for randomization
random.seed(2026)
  
DEPOT = 'A'
DISTANCES = {
  'A': {'A': 0, 'B': 4, 'C': 8, 'D': 6, 'E': 7, 'F': 9, 'G': 5},
  'B': {'A': 4, 'B': 0, 'C': 5, 'D': 7, 'E': 3, 'F': 8, 'G': 6},
  'C': {'A': 8, 'B': 5, 'C': 0, 'D': 4, 'E': 6, 'F': 3, 'G': 7},
  'D': {'A': 6, 'B': 7, 'C': 4, 'D': 0, 'E': 5, 'F': 6, 'G': 8},
  'E': {'A': 7, 'B': 3, 'C': 6, 'D': 5, 'E': 0, 'F': 4, 'G': 6},
  'F': {'A': 9, 'B': 8, 'C': 3, 'D': 6, 'E': 4, 'F': 0, 'G': 5},
  'G': {'A': 5, 'B': 6, 'C': 7, 'D': 8, 'E': 6, 'F': 5, 'G': 0},
}

# Construct initial population
def construct_population(population_size, nodes):
  population = []
  for _ in range(population_size):
    route = nodes[:]
    random.shuffle(route)
    population.append(route)
  return population
  

def calculate_distance(route):
  # Distance from depot to the first node in the route
  total = DISTANCES[DEPOT][route[0]]
  route_length = len(route)
  # Measuring distance between nodes within the route
  for i in range(route_length-1):
    total += DISTANCES[route[i]][route[i+1]]
  # Distance from the last node of the route to depot
  total += DISTANCES[route[route_length-1]][DEPOT]
  return total

# Parent selection, using tournament selection by selecting 2 random routes to be compared with, one with the smallest distance wins
def tournament_selection(population):
  comparison = random.sample(population, 2)
  return min(comparison, key=calculate_distance)

# Order cross over combine both parents' routes to derive a better new route
def order_crossover(parent1, parent2):
  half = ceil(float(len(parent1))/2)
  new_list = parent1[0:half]
  for i in parent2: 
    if i not in new_list:
      new_list.append(i)
  return new_list

# Mutation provides small random changes to maintain route's diversity and prevent the algorithm from getting stuck in a suboptimal route
def swap_mutation(route):
  mutated = route[:]
  i, j = random.sample(range(len(mutated)), 2)
  mutated[i], mutated[j] = mutated[j], mutated[i]
  return mutated

# Elitism, storing best current path so that won't 
def perform_elitism(population): 
  best_route = min(population, key=calculate_distance)
  next_generation = [best_route[:]]
  return next_generation

def run_ga(population_size, generations, route):
  population = construct_population(population_size, route)
  for _ in range(generations):
    # Elitism, storing the best current route in the next_generation list without performing any changes
    next_generation = perform_elitism(population)
    
    while len(next_generation) < population_size:
      # Selecting 2 parents randomly
      parent1, parent2 = tournament_selection(population), tournament_selection(population)
      # Perform crossover
      new_child = order_crossover(parent1, parent2)
      # Swap between two nodes
      mutated_child = swap_mutation(new_child)
      # Push the mutated child route to the next generation list
      next_generation.append(mutated_child)
    population = next_generation

  best_route = min(population, key=calculate_distance)
  return best_route, calculate_distance(best_route)
    
def main(): 
  ROUTE = ['B', 'C', 'D', 'E', 'F', 'G']
  population_size = 20
  generations = 50

  distance = calculate_distance(ROUTE)
  print(f"The total distance is: {distance}")

  best_route, best_distance_route = run_ga(population_size, generations, ROUTE)
  full_route = [DEPOT] + best_route + [DEPOT]

  print(f"Best route, ", '->'.join(full_route))
  print(f"With distance of: {best_distance_route} unit")
  
if __name__ == "__main__":
  main()