import numpy as np
import random as rd
from random import randint


string = open('knapsack_instances/instances_small/instance_small_0.txt').read()

file_vars = {}
values = [x.strip() for x in string.split('\n')]
for value in values:
    if '=' not in value:
        continue
    pair = [x.strip() for x in value.split('=')]
    pair[1] = pair[1].replace('\\n', ' ')
    while '  ' in pair[1] and ' ' in pair[1]:
        pair[1] = pair[1].replace('  ', '')
        pair[1] = pair[1].replace(' ', '')
    pair[1] = pair[1].replace(' ', ', ')
    file_vars[pair[0]] = eval(pair[1])

l_no_objects = file_vars['no_objects']
l_max_weight = file_vars['max_weight']
l_weights = file_vars['weights']
l_objects = file_vars['objects']

item_number = l_no_objects
weight = l_weights
value = l_objects
knapsack_threshold = l_max_weight


solutions_per_pop = l_no_objects
pop_size = (solutions_per_pop, item_number)
print('Population size = {}'.format(pop_size))
initial_population = np.random.randint(2, size=pop_size)
initial_population = initial_population.astype(int)
num_generations = 500
print('Initial population: \n{}'.format(initial_population))


def cal_fitness(weight, value, population, threshold):
    fitness = np.empty(population.shape[0])
    for i in range(population.shape[0]):
        S1 = np.sum(population[i] * value)
        S2 = np.sum(population[i] * weight)
        if S2 <= threshold:
            fitness[i] = S1
        else:
            fitness[i] = 0
    return fitness.astype(int)


def selection(fitness, num_parents, population):
    fitness = list(fitness)
    parents = np.empty((num_parents, population.shape[1]))
    for i in range(num_parents):
        max_fitness_idx = np.where(fitness == np.max(fitness))
        parents[i, :] = population[max_fitness_idx[0][0], :]
        fitness[max_fitness_idx[0][0]] = -999999
    return parents


#one point crossover
def crossover(parents, num_offsprings):
    offsprings = np.empty((num_offsprings, parents.shape[1]))
    crossover_point = int(parents.shape[1] / 2)
    crossover_rate = 0.8
    i = 0
    while parents.shape[0] < num_offsprings:
        parent1_index = i % parents.shape[0]
        parent2_index = (i + 1) % parents.shape[0]
        x = rd.random()
        if x > crossover_rate:
            continue
        parent1_index = i % parents.shape[0]
        parent2_index = (i + 1) % parents.shape[0]
        offsprings[i, 0:crossover_point] = parents[parent1_index, 0:crossover_point]
        offsprings[i, crossover_point:] = parents[parent2_index, crossover_point:]
        i = +1
    return offsprings



# tehnica bit-flip
def mutation(offsprings):
    mutants = np.empty(offsprings.shape)
    mutation_rate = 0.4
    for i in range(mutants.shape[0]):
        random_value = rd.random()
        mutants[i, :] = offsprings[i, :]
        if random_value > mutation_rate:
            continue
        int_random_value = randint(0, offsprings.shape[1] - 1)
        if mutants[i, int_random_value] == 0:
            mutants[i, int_random_value] = 1
        else:
            mutants[i, int_random_value] = 0
    return mutants


def optimize(weight, value, population, pop_size, num_generations, threshold):
    parameters, fitness_history = [], []
    num_parents = int(pop_size[0] / 2)
    num_offsprings = pop_size[0] - num_parents
    for i in range(num_generations):
        fitness = cal_fitness(weight, value, population, threshold)
        fitness_history.append(fitness)
        parents = selection(fitness, num_parents, population)
        offsprings = crossover(parents, num_offsprings)
        mutants = mutation(offsprings)
        population[0:parents.shape[0], :] = parents
        population[parents.shape[0]:, :] = mutants

    print('Last generation: \n{}\n'.format(population))
    fitness_last_gen = cal_fitness(weight, value, population, threshold)
    print('Fitness of the last generation: \n{}\n'.format(fitness_last_gen))
    max_fitness = np.where(fitness_last_gen == np.max(fitness_last_gen))
    parameters.append(population[max_fitness[0][0], :])
    return parameters, fitness_history


if __name__ == '__main__':
    parameters, fitness_history = optimize(weight, value, initial_population, pop_size, num_generations,
                                           knapsack_threshold)
    print('The optimized parameters for the given inputs are: \n{}'.format(parameters))
    selected_items = item_number * parameters


