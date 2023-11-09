import itertools
import operator
import random
import sys
from functools import reduce

from deap import algorithms, base, creator, tools


def optimize_mintime(pattern, data):
    def sig(x,down,up):
        if x >= down and x < up :
            return 1 
        else:
            return 0
    
    lst = list(range(data['mintasks'], data['totaltasks'], 2))
    root_available = data['totaltasks'] - data['mintasks']
    ice_root_available = data['totaltasks']-data['ice_procs'][0]
            
    def objective(individual):
       
        for constraint in constraints:
            if constraint['fun'](individual) < 0:
                return sys.maxsize,
        min_time = 0
        for i in range(data['models_num']):
            model = data['models'][i]
            p = individual[2*i+1]
            part = data[model][p]
            for j in range(data['models_num']):
                if i != j:
                    flag = sig(individual[2*i], individual[2*j], individual[2*j] + individual[2*j+1])
                    if flag:
                        model = data['models'][j]
                        p = individual[2*j+1]
                        part += data[model][p]
            min_time = max(min_time, part)
        return min_time,

    constraints = []
    for i in range(data['models_num']):
        constraints.append({'type': 'ineq', 'fun': lambda x, i=i : data['totaltasks'] - (x[2*i] + x[2*i+1])}) 
        if data['models'][i] == 'ice':
            constraints.append({'type': 'eq', 'fun': lambda x, i=i : (x[2*i+1] in data['ice_procs']) - 1})
            constraints.append({'type': 'eq', 'fun': lambda x, i=i : (0 <= x[2*i] <= ice_root_available) - 1})
            
        else: 
            constraints.append({'type': 'eq', 'fun': lambda x, i=i : (x[2*i+1] in lst) - 1})
            constraints.append({'type': 'eq', 'fun': lambda x, i=i : (0 <= x[2*i] <= root_available) - 1})
    for line in pattern:
        pairs_list = list(itertools.combinations(line, 2))
        for pair in pairs_list:
            a, b = pair[0]-1, pair[1]-1
            constraints.append({'type': 'ineq', 'fun': lambda x, a=a, b=b : (x[2*b] + x[2*b+1] - x[2*a])*(x[2*b] - x[2*a+1] - x[2*a])})
            constraints.append({'type': 'ineq', 'fun': lambda x, a=a, b=b : (x[2*b] - x[2*a])*(x[2*b] - x[2*a]) - 1})

    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)
    toolbox = base.Toolbox()

    toolbox.register("attr_root", random.randint, 0, root_available)
    toolbox.register("attr_task", random.choice, lst)
    toolbox.register("attr_ice_root", random.randint, 0, ice_root_available)
    toolbox.register("attr_ice_task", random.choice, data['ice_procs'])

    def create_individual():
        individual = creator.Individual()
        for model in data['models']:
            if model == 'ice':
                individual.append(toolbox.attr_ice_root())
                individual.append(toolbox.attr_ice_task())
            else:
                individual.append(toolbox.attr_root())
                individual.append(toolbox.attr_task())
        
        for constraint in constraints:
            if constraint['fun'](individual) < 0:
                return None
        
        return individual

    toolbox.register("individual", create_individual)

    def create_population(n):
        population = []
        while len(population) < n:
            individual = create_individual()
            if (individual is not None) and all(constraint['fun'](individual) >= 0 for constraint in constraints):
                population.append(individual)
        return population

    pop = create_population(50)

    toolbox.register("evaluate", objective)

    toolbox.register("mate", tools.cxTwoPoint)

    toolbox.register("mutate", tools.mutUniformInt, low=0, up=data['totaltasks'], indpb=0.1)

    toolbox.register("select", tools.selTournament, tournsize=3)


    result, log = algorithms.eaSimple(pop, toolbox, cxpb=0.3, mutpb=0.1, ngen=50, verbose=False)
    
    best_individual = tools.selBest(result, k=1)[0]

    
    del creator.FitnessMin
    del creator.Individual
    
    return best_individual, best_individual.fitness.values[0]

def optimize_mincost(pattern, data):
    def sig(x,down,up):
        if x >= down and x < up :
            return 1 
        else:
            return 0

    lst = list(range(data['mintasks'], data['totaltasks'], 2))
    root_available = data['totaltasks'] - data['mintasks']
    ice_root_available = data['totaltasks']-data['ice_procs'][0]
            
    def objective(individual):
        for constraint in constraints:
            if constraint['fun'](individual) < 0:
                return sys.maxsize,
        min_time = 0
        left_procs = data['totaltasks']
        right_procs = 0
        for i in range(data['models_num']):
            left_procs = min(left_procs, individual[2*i])
            right_procs = max(right_procs, individual[2*i] + individual[2*i+1])
        used_procs = right_procs - left_procs
        
        for i in range(data['models_num']):
            model = data['models'][i]
            p = individual[2*i+1]
            part = data[model][p]
            for j in range(data['models_num']):
                if i != j:
                    flag = sig(individual[2*i], individual[2*j], individual[2*j] + individual[2*j+1])
                    if flag:
                        model = data['models'][j]
                        p = individual[2*j+1]
                        part += data[model][p] 
            part *= used_procs
            min_time = max(min_time, part)
        return min_time,

    constraints = []

    for i in range(data['models_num']):
        constraints.append({'type': 'ineq', 'fun': lambda x, i=i : data['totaltasks'] - (x[2*i] + x[2*i+1])}) 
        if data['models'][i] == 'ice':
            constraints.append({'type': 'eq', 'fun': lambda x, i=i : (x[2*i+1] in data['ice_procs']) - 1})
            constraints.append({'type': 'eq', 'fun': lambda x, i=i : (0 <= x[2*i] <= ice_root_available) - 1})
            
        else: 
            constraints.append({'type': 'eq', 'fun': lambda x, i=i : (x[2*i+1] in lst) - 1})
            constraints.append({'type': 'eq', 'fun': lambda x, i=i : (0 <= x[2*i] <= root_available) - 1})
        
    for line in pattern:
        pairs_list = list(itertools.combinations(line, 2))
        for pair in pairs_list:
            a, b = pair[0]-1, pair[1]-1
            constraints.append({'type': 'ineq', 'fun': lambda x, a=a, b=b : (x[2*b] + x[2*b+1] - x[2*a])*(x[2*b] - x[2*a+1] - x[2*a])})
            constraints.append({'type': 'ineq', 'fun': lambda x, a=a, b=b : (x[2*b] - x[2*a])*(x[2*b] - x[2*a]) - 1})

    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()

    toolbox.register("attr_root", random.randint, 0, root_available)
    toolbox.register("attr_task", random.choice, lst)
    toolbox.register("attr_ice_root", random.randint, 0, ice_root_available)
    toolbox.register("attr_ice_task", random.choice, data['ice_procs'])

    def create_individual():
        individual = creator.Individual()
        for model in data['models']:
            if model == 'ice':
                individual.append(toolbox.attr_ice_root())
                individual.append(toolbox.attr_ice_task())
            else:
                individual.append(toolbox.attr_root())
                individual.append(toolbox.attr_task())
        
        for constraint in constraints:
            if constraint['fun'](individual) < 0:
                return None
        
        return individual

    toolbox.register("individual", create_individual)

    def create_population(n):
        population = []
        while len(population) < n:
            individual = create_individual()
            if (individual is not None) and all(constraint['fun'](individual) >= 0 for constraint in constraints):
                population.append(individual)
        return population

    pop = create_population(50)

    toolbox.register("evaluate", objective)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutUniformInt, low=0, up=data['totaltasks'], indpb=0.1)
    toolbox.register("select", tools.selTournament, tournsize=3)

    result, log = algorithms.eaSimple(pop, toolbox, cxpb=0.3, mutpb=0.1, ngen=50, verbose=False)
    
    best_individual = tools.selBest(result, k=1)[0]
    
    del creator.FitnessMin
    del creator.Individual
    
    return best_individual, best_individual.fitness.values[0]
