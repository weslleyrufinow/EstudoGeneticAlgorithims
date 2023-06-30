# Implemente o algoritmo genético clássico para resolver instâncias do problema de TSP (Caixeiro-Viajante). Uma instância do problema é dada como uma lista de caminhos que conectam cidades representadas por um rótulo. Uma instância pode ser representada em um arquivo de entrada. A primeira linha deste arquivo contém um par de  inteiros que diz a quantidade de cidades e a quantidade de conexões (rodovias) entre cidades. As linhas seguintes (uma para cada rodovia) contém dois inteiros e um número real separados por vírgula. Os dois primeiros números indicam as cidades conectadas pela rodovia cujo tamaho, em km, é o terceiro valor da linha.  Para simplificar, cada conexão é bidirecional (todas as rodovidas são de mão-dupla). 

import numpy as np
import random

# Classe representando um indivíduo na população
class Individual:
    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.fitness = 0
    def calculate_fitness(self, distance_matrix):
        total_distance = 0
        num_cities = len(self.chromosome)
        for i in range(num_cities - 1):
            city_a = self.chromosome[i]
            city_b = self.chromosome[i + 1]
            total_distance += distance_matrix[city_a][city_b]
        self.fitness = total_distance

# Função para inicializar uma população de indivíduos randomicamente
def initialize_population(num_individuals, num_cities):
    population = []
    for _ in range(num_individuals):
        # Cria uma lista de cidades [1, 2, ..., num_cities] para criar os cromossomos
        chromosome = list(range(1, num_cities + 1))  
        random.shuffle(chromosome)  # Embaralha as cidades
        individual = Individual(chromosome)
        population.append(individual)
    return population

# Função para calcular a matriz de distâncias entre as cidades
def calculate_distance_matrix(connections, num_cities):
    distance_matrix = np.zeros((num_cities + 1, num_cities + 1))
    for connection in connections:
        city_a, city_b, distance = connection
        distance_matrix[city_a][city_b] = distance
        distance_matrix[city_b][city_a] = distance
    return distance_matrix

# Função para avaliar a aptidão (fitness) de todos os indivíduos na população
def evaluate_population(population, distance_matrix):
    for individual in population:
    # Essa função calcula a aptidão de um indivíduo com base na soma das distâncias percorridas ao visitar todas as cidades em seu cromossomo.
      individual.calculate_fitness(distance_matrix)

# Função para selecionar dois pais com base na roleta viciada
def selection(population):
    fitness_sum = sum(individual.fitness for individual in population)
    probabilities = [individual.fitness / fitness_sum for individual in population]
    selected_parents = random.choices(population, probabilities,k=2)
    return selected_parents

# Função para realizar o crossover de dois pais e gerar um filho
def crossover(parent1, parent2):
    num_cities = len(parent1.chromosome)
    start = random.randint(0, num_cities - 1)
    end = random.randint(start + 1, num_cities)
    child_chromosome = [None] * num_cities
    for i in range(start, end):
        child_chromosome[i] = parent1.chromosome[i]
    j = 0
    for i in range(num_cities):
        if child_chromosome[i] is None:
            while parent2.chromosome[j] in child_chromosome:
                j += 1
            child_chromosome[i] = parent2.chromosome[j]
    return Individual(child_chromosome)

# Função para realizar a mutação em um indivíduo
def mutate(individual):
    num_cities = len(individual.chromosome)
    if random.random() <= 0.01:  # Probabilidade de mutação = 1%
        index_a = random.randint(0, num_cities - 1)
        index_b = random.randint(0, num_cities - 1)
        individual.chromosome[index_a], individual.chromosome[index_b] = individual.chromosome[index_b], individual.chromosome[index_a]

# Função para encontrar a melhor solução (rota) após a execução do algoritmo genético
def find_best_solution(population):
    best_individual = min(population, key=lambda individual: individual.fitness)
    return best_individual

# Função principal que implementa o algoritmo genético
def genetic_algorithm(connections, num_individuals, num_generations):
    # Minha matriz de distancia
    distance_matrix = calculate_distance_matrix(connections, num_cities)
    # Inicializando a população aleatoriamente
    population = initialize_population(num_individuals, num_cities)

    for _ in range(num_generations):
        evaluate_population(population, distance_matrix)
        new_population = [find_best_solution(population)]

        while len(new_population) < num_individuals:
            parent1, parent2 = selection(population)
            child = crossover(parent1, parent2)
            mutate(child)
            new_population.append(child)

        population = new_population

    best_solution = find_best_solution(population)
    return best_solution

# Função para ler as conexões a partir de um arquivo de entrada
def read_connections_from_file(filename):
    with open(filename, 'r') as file:
        global num_cities
        num_cities, num_connections = map(int, file.readline().strip().split(','))
        connections = []
        for _ in range(num_connections):
            city_a, city_b, distance = map(int, file.readline().strip().split(','))
            connections.append((city_a, city_b, distance))
    return connections

# Função para imprimir a rota encontrada
def print_route(individual):
    route = '-'.join(map(str, individual.chromosome))
    print(route)

# Exemplo de uso
connections = read_connections_from_file('dados.txt')

best_individual = genetic_algorithm(connections, num_individuals=100, num_generations=1000)

print_route(best_individual)
