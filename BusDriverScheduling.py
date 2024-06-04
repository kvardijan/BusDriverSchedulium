import random
from collections import defaultdict
class BusTask:
    def __init__(self, bus_line_id, origin, destination, start_hour, start_minutes, duration, vehicle_id):
        self.bus_line_id = bus_line_id
        self.origin = origin
        self.destination = destination
        self.start_hour = start_hour
        self.start_minutes = start_minutes
        self.duration = duration
        self.vehicle_id = vehicle_id

    def __repr__(self):
        return f"BusTask({self.bus_line_id}, {self.origin}, {self.destination}, {self.start_hour}, {self.start_minutes}, {self.duration}, {self.vehicle_id})"

def read_input(input_str):
    lines = input_str.strip().split("\n")
    num_tasks = int(lines[0].strip())
    tasks = []
    for line in lines[1:num_tasks+1]:
        parts = line.strip().strip('"').split(',')
        bus_line_id = parts[0].strip('"')
        origin = parts[1].strip('"')
        destination = parts[2].strip('"')
        start_hour = int(parts[3])
        start_minutes = int(parts[4])
        duration = int(parts[5])
        vehicle_id = int(parts[6])
        tasks.append(BusTask(bus_line_id, origin, destination, start_hour, start_minutes, duration, vehicle_id))
    return tasks

def generate_random_schedule(tasks):
    schedule = tasks[:]
    random.shuffle(schedule)
    return schedule

def calculate_cost(schedule):
    cost = 0
    TimesDriven = defaultdict(int)
    for i in range(1, len(schedule)):
        prev_task = schedule[i - 1]
        curr_task = schedule[i]

        if prev_task.bus_line_id == curr_task.bus_line_id:
            prev_end_time = prev_task.start_hour * 60 + prev_task.start_minutes + prev_task.duration
            curr_start_time = curr_task.start_hour * 60 + curr_task.start_minutes
            if prev_end_time > curr_start_time:
                cost += (prev_end_time - curr_start_time) * 10
            
            idle_time = curr_start_time - prev_end_time
            if idle_time > 0:
                cost += idle_time

        if prev_task.vehicle_id == curr_task.vehicle_id:

            TimesDriven[prev_task.vehicle_id] += prev_task.duration
            
            if TimesDriven[prev_task.vehicle_id] > 240:
                excess_time = TimesDriven[prev_task.vehicle_id] - 240
                cost += excess_time * 5
        else:
            TimesDriven[prev_task.vehicle_id] += prev_task.duration
            if TimesDriven[prev_task.vehicle_id] > 240:
                excess_time = TimesDriven[prev_task.vehicle_id] - 240
                cost += excess_time * 5
            TimesDriven[curr_task.vehicle_id] = 0
    
    TimesDriven[schedule[-1].vehicle_id] += schedule[-1].duration
    if TimesDriven[schedule[-1].vehicle_id] > 240:
        excess_time = TimesDriven[schedule[-1].vehicle_id] - 240
        cost += excess_time * 5

    return cost

def selection(population, fitnesses):
    total_fitness = sum(fitnesses)
    pick = random.uniform(0, total_fitness)
    current = 0
    for individual, fitness in zip(population, fitnesses):
        current += fitness
        if current > pick:
            return individual

def check_dictionary_found_match(task_recieved, dictionary):
    for task, taskInDictionary in dictionary.items():
        if (task_recieved.bus_line_id == taskInDictionary.bus_line_id and task_recieved.origin == taskInDictionary.origin and task_recieved.destination == taskInDictionary.destination
            and task_recieved.start_hour == taskInDictionary.start_hour and task_recieved.start_minutes == taskInDictionary.start_minutes
            and task_recieved.duration == taskInDictionary.duration and task_recieved.vehicle_id == taskInDictionary.vehicle_id):
            return True
        
    return False

def crossover(parent1, parent2):
    crossover_point1 = random.randint(1, len(parent1) - 2)
    crossover_point2 = random.randint(crossover_point1+1, len(parent1) - 1)
    child1_locations = defaultdict(BusTask)
    child2_locations = defaultdict(BusTask)
    brojac = crossover_point1
    for location in parent1[crossover_point1:crossover_point2+1]:
        child2_locations[brojac] = location
        brojac+=1
    brojac = crossover_point1
    for location in parent2[crossover_point1:crossover_point2+1]:
        child1_locations[brojac] = location
        brojac+=1
    
    child1 = []
    brojacZaRoditelj1 = 0
    for element in parent1[:crossover_point1]:
        if check_dictionary_found_match(element, child1_locations):
            child1.append(parent2[brojacZaRoditelj1])
            brojacZaRoditelj1+=1
        else:
            child1.append(parent1[brojacZaRoditelj1])
            brojacZaRoditelj1+=1
    
    for route, taskindictionary in child1_locations.items():
        child1.append(taskindictionary)

    brojacZaRoditelj1 = crossover_point2+1
    for element in parent1[crossover_point2+1:]:
        if check_dictionary_found_match(element, child1_locations):
            child1.append(parent2[brojacZaRoditelj1])
            brojacZaRoditelj1+=1
        else:
            child1.append(parent1[brojacZaRoditelj1])
            brojacZaRoditelj1+=1

    child2 = []
    brojaczaroditelj2 = 0
    for element in parent2[:crossover_point1]:
        if check_dictionary_found_match(element, child2_locations):
            child2.append(parent1[brojaczaroditelj2])
            brojaczaroditelj2+=1
        else:
            child2.append(parent2[brojaczaroditelj2])
            brojaczaroditelj2+=1
    
    for route, taskindictionary in child2_locations.items():
        child2.append(taskindictionary)

    brojaczaroditelj2 = crossover_point2+1
    for element in parent2[crossover_point2+1:]:
        if check_dictionary_found_match(element, child2_locations):
            child2.append(parent1[brojaczaroditelj2])
            brojaczaroditelj2+=1
        else:
            child2.append(parent2[brojaczaroditelj2])
            brojaczaroditelj2+=1

    return child1, child2

def provjeri_podudaranje(element, trazena_vrijednost):
    if (element.bus_line_id == trazena_vrijednost.bus_line_id and element.origin == trazena_vrijednost.origin and element.destination == trazena_vrijednost.destination
            and element.start_hour == trazena_vrijednost.start_hour and element.start_minutes == trazena_vrijednost.start_minutes
            and element.duration == trazena_vrijednost.duration and element.vehicle_id == trazena_vrijednost.vehicle_id):
            return True
    return False

def nadi_sljedeci_index(roditelj, trazena_vrijednost):
    brojac = 0
    for element in roditelj:
        if provjeri_podudaranje(element, trazena_vrijednost):
            return brojac
        brojac+=1
    return -1

def provjeri_index_ciklusa(ciklus_indexi, index):
    for i in ciklus_indexi:
        if i == index:
            return True
    return False

def nadi_prvi_slobodni_index(iskoristeni_indexi, parent1):
    i = 0
    for e in parent1:
        iskoristeni = False
        for i_x in iskoristeni_indexi:
            if i == i_x:
                iskoristeni = True
                break
        if iskoristeni:
            i+=1
        else:
            return i
    return -1

def cycle_crossover(parent1, parent2):
    child1_locations = defaultdict(BusTask)
    child2_locations = defaultdict(BusTask)

    iskoristeni_indexi = []
    parni_ciklus = False
    while len(iskoristeni_indexi) < len(parent1):  # cjelo krizanje
        index = nadi_prvi_slobodni_index(iskoristeni_indexi, parent1)
        ciklus_indexi = []
        while True:
            ciklus_indexi.append(index)
            iskoristeni_indexi.append(index)
            if parni_ciklus:
                child1_locations[index] = parent2[index]
                child2_locations[index] = parent1[index]
            else:
                child1_locations[index] = parent1[index]
                child2_locations[index] = parent2[index]
            index = nadi_sljedeci_index(parent1, parent2[index])
            if provjeri_index_ciklusa(ciklus_indexi, index):
                break
        parni_ciklus = not parni_ciklus

    child1 = [None] * len(parent1)
    child2 = [None] * len(parent1)
    for route, taskindictionary in child1_locations.items():
        child1[route] = taskindictionary
    for route, taskindictionary in child2_locations.items():
        child2[route] = taskindictionary

    return child1, child2

def mutate(individual, mutation_rate):
    if random.random() < mutation_rate:
        mutation_point1 = random.randint(0, len(individual) - 1)
        mutation_point2 = random.randint(0, len(individual) - 1)
        individual[mutation_point1], individual[mutation_point2] = individual[mutation_point2], individual[mutation_point1]
    return individual

def genetic_algorithm(tasks, population_size=10, mutation_rate=0.01, num_generations=1000):
    population = [generate_random_schedule(tasks) for _ in range(population_size)]

    for generation in range(num_generations):
        fitnesses = [1 / (calculate_cost(individual) + 1) for individual in population]  # Avoid division by zero
        new_population = []

        for _ in range(population_size // 2):
            parent1 = selection(population, fitnesses)
            parent2 = selection(population, fitnesses)
            child1, child2 = cycle_crossover(parent1, parent2)
            new_population.append(mutate(child1, mutation_rate))
            new_population.append(mutate(child2, mutation_rate))

        population = new_population
    best_schedule = min(population, key=calculate_cost)
    return best_schedule

file_path = 'V_TCCC2313.txt'
with open(file_path, 'r') as file:
    input_str = file.read()

tasks = read_input(input_str)
tasks_by_bus_line_id = defaultdict(list)
for task in tasks:
    tasks_by_bus_line_id[task.bus_line_id].append(task)
for bus_line_id, tasks_array in tasks_by_bus_line_id.items():
    for task in genetic_algorithm(tasks_array):
        print(task)