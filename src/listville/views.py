from django.shortcuts import render
from listville.forms import CountryForm
import random
from itertools import combinations
import pandas as pd
import numpy as np
import json
# import googlemaps
# from itertools import combinations
#librerary 
# Create your views here.

def webpage1(request):
	if request.method == "POST":
		form = CountryForm(request.POST)
		if form.is_valid():
			countries = form.cleaned_data.get('countries')
            # do something with your results
	else:
		form = CountryForm
	return render(request,'page2.html', {'form': form})
	##return render(request,"")

def webpage2(request):
	if request.method == "POST":
		form = CountryForm(request.POST)
		if form.is_valid():
			countries = form.cleaned_data.get('countries')
			# preparation_data()
			# lire_data()
			mylist = []
			mylist = run_genetic_algorithm(generations=5000, population_size=100)
			#json_cities = json.dumps(mylist)
			# with open('bestpath.txt', 'w') as f:
			# 	for item in mylist:
			# 		f.write("%s\n" % item)
	else:
		form = CountryForm
	return render(request,"page1.html",{'form': form,'countries':countries,'mylist':mylist})

##### tsp ga algorithme
# waypoint_distances = {}
# waypoint_durations = {}
# def preparation_data():
# 	gmaps = googlemaps.Client(key="")
# 	waypoint_distances = {}
# 	waypoint_durations = {}
# 	for (waypoint1, waypoint2) in combinations(countries[0], 2):
# 		route = gmaps.distance_matrix(origins=[waypoint1],
#                                       destinations=[waypoint2],
#                                       mode="driving", # Change this to "walking" for walking directions,
#                                                       # "bicycling" for biking directions, etc.
#                                       language="English",
#                                       units="metric")

# 		distance = route["rows"][0]["elements"][0]["distance"]["value"]
# 		duration = route["rows"][0]["elements"][0]["duration"]["value"]
# 		waypoint_distances[frozenset([waypoint1, waypoint2])] = distance
# 		waypoint_durations[frozenset([waypoint1, waypoint2])] = duration

# 	with open("my-waypoints-dist-dur.tsv", "w") as out_file:
# 		out_file.write("\t".join(["waypoint1",
#                               "waypoint2",
#                               "distance_m",
#                               "duration_s"]))
# 		for (waypoint1, waypoint2) in waypoint_distances.keys():
# 			out_file.write("\n" +
#                        "\t".join([waypoint1,
#                                   waypoint2,
#                                   str(waypoint_distances[frozenset([waypoint1, waypoint2])]),
#                                   str(waypoint_durations[frozenset([waypoint1, waypoint2])])]))

# def lire_data():
#     waypoint_distances = {}
#     waypoint_durations = {}
#     countries[0] = set()
#     waypoint_data = pd.read_csv("my-waypoints-dist-dur.tsv", sep="\t")
    
#     for i, row in waypoint_data.iterrows():
#         waypoint_distances[frozenset([row.waypoint1, row.waypoint2])] = row.distance_m
#         waypoint_durations[frozenset([row.waypoint1, row.waypoint2])] = row.duration_s
        # countries[0].update([row.waypoint1, row.waypoint2])
# waypoint_distances = {}
# waypoint_durations = {}

# for (waypoint1, waypoint2) in combinations(countries, 2):
#         route = gmaps.distance_matrix(origins=[waypoint1],
#                                       destinations=[waypoint2],
#                                       mode="driving", # Change this to "walking" for walking directions,
#                                                       # "bicycling" for biking directions, etc.
#                                       language="English",
#                                       units="metric")

#         # "distance" is in meters
#         distance = route["rows"][0]["elements"][0]["distance"]["value"]

#         # "duration" is in seconds
#         duration = route["rows"][0]["elements"][0]["duration"]["value"]

#         waypoint_distances[frozenset([waypoint1, waypoint2])] = distance
#         waypoint_durations[frozenset([waypoint1, waypoint2])] = duration


# with open("my-waypoints-dist-dur.tsv", "w") as out_file:
#     out_file.write("\t".join(["waypoint1",
#                               "waypoint2",
#                               "distance_m",
#                               "duration_s"]))
    
#     for (waypoint1, waypoint2) in waypoint_distances.keys():
#         out_file.write("\n" +
#                        "\t".join([waypoint1,
#                                   waypoint2,
#                                   str(waypoint_distances[frozenset([waypoint1, waypoint2])]),
#                                   str(waypoint_durations[frozenset([waypoint1, waypoint2])])]))



waypoint_distances = {}
waypoint_durations = {}
countries = set()

waypoint_data = pd.read_csv("my-waypoints-dist-dur.tsv", sep="\t")

for i, row in waypoint_data.iterrows():
    waypoint_distances[frozenset([row.waypoint1, row.waypoint2])] = row.distance_m
    waypoint_durations[frozenset([row.waypoint1, row.waypoint2])] = row.duration_s
    countries.update([row.waypoint1, row.waypoint2])
def compute_fitness(solution):
    """
        This function returns the total distance traveled on the current road trip.
        
        The genetic algorithm will favor road trips that have shorter
        total distances traveled.
    """
    
    solution_fitness = 0.0
    
    for index in range(len(solution)):
        waypoint1 = solution[index - 1]
        waypoint2 = solution[index]
        solution_fitness += waypoint_distances[frozenset([waypoint1, waypoint2])]
        
    return solution_fitness

def generate_random_agent():
    """
        Creates a random road trip from the waypoints.
    """
    
    new_random_agent = list(countries)
    random.shuffle(new_random_agent)
    return tuple(new_random_agent)

def mutate_agent(agent_genome, max_mutations=3):
    """
        Applies 1 - `max_mutations` point mutations to the given road trip.
        
        A point mutation swaps the order of two waypoints in the road trip.
    """
    
    agent_genome = list(agent_genome)
    num_mutations = random.randint(1, max_mutations)
    
    for mutation in range(num_mutations):
        swap_index1 = random.randint(0, len(agent_genome) - 1)
        swap_index2 = swap_index1

        while swap_index1 == swap_index2:
            swap_index2 = random.randint(0, len(agent_genome) - 1)

        agent_genome[swap_index1], agent_genome[swap_index2] = agent_genome[swap_index2], agent_genome[swap_index1]
            
    return tuple(agent_genome)

def shuffle_mutation(agent_genome):
    """
        Applies a single shuffle mutation to the given road trip.
        
        A shuffle mutation takes a random sub-section of the road trip
        and moves it to another location in the road trip.
    """
    
    agent_genome = list(agent_genome)
    
    start_index = random.randint(0, len(agent_genome) - 1)
    length = random.randint(2, 20)
    
    genome_subset = agent_genome[start_index:start_index + length]
    agent_genome = agent_genome[:start_index] + agent_genome[start_index + length:]
    
    insert_index = random.randint(0, len(agent_genome) + len(genome_subset) - 1)
    agent_genome = agent_genome[:insert_index] + genome_subset + agent_genome[insert_index:]
    
    return tuple(agent_genome)

def generate_random_population(pop_size):
    """
        Generates a list with `pop_size` number of random road trips.
    """
    
    random_population = []
    for agent in range(pop_size):
        random_population.append(generate_random_agent())
    return random_population
def run_genetic_algorithm(generations=5000, population_size=100):
    """
        The core of the Genetic Algorithm.
        
        `generations` and `population_size` must be a multiple of 10.
    """
    
    population_subset_size = int(population_size / 10.)
    generations_10pct = int(generations / 10.)
    
    # Create a random population of `population_size` number of solutions.
    population = generate_random_population(population_size)

    # For `generations` number of repetitions...
    for generation in range(generations):
        
        # Compute the fitness of the entire current population
        population_fitness = {}

        for agent_genome in population:
            if agent_genome in population_fitness:
                continue

            population_fitness[agent_genome] = compute_fitness(agent_genome)

        # Take the top 10% shortest road trips and produce offspring each from them
        new_population = []
        for rank, agent_genome in enumerate(sorted(population_fitness,
                                                   key=population_fitness.get)[:population_subset_size]):
            
            if (generation % generations_10pct == 0 or generation == generations - 1) and rank == 0:
                print("Generation %d best: %d | Unique genomes: %d" % (generation,
                                                                       population_fitness[agent_genome],
                                                                       len(population_fitness)))
                print(agent_genome)
                print("######")

            # Create 1 exact copy of each of the top road trips
            new_population.append(agent_genome)

            # Create 2 offspring with 1-3 point mutations
            for offspring in range(2):
                new_population.append(mutate_agent(agent_genome, 3))
                
            # Create 7 offspring with a single shuffle mutation
            for offspring in range(7):
                new_population.append(shuffle_mutation(agent_genome))

        # Replace the old population with the new population of offspring 
        for i in range(len(population))[::-1]:
            del population[i]

        population = new_population
    print("final: ")
    print(agent_genome)
    finallist = list(agent_genome)
    return finallist