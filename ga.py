#!/usr/bin/env python
import capitals
import numpy as np
import random
import time

N_GENES = 5
DF = 2

def initialize_population(n):
    population = []
    for i in range(0,n):
        population.append(np.random.standard_t(DF,N_GENES))
    return population

def breed(population, fitness):
    # keep best individual
    # select two parents (probability ~ 1/cost)
    # two-point crossover to create children
    # mutate w/ 4% probability
    # create 90% of children this way, initialize 10% randomly

    newpop = []

    # elitism: keep best individual
    newpop.append(population[fitness.argmax()])

    # Create 90% of children by two-point crossover
    probs = fitness / sum(fitness)
    choices = [(population[i], prob) for i,prob in enumerate(probs)]
    while (len(newpop) < 0.9*len(population)):
        # Select two parents
        parent1 = weighted_choice(choices)
        parent2 = weighted_choice(choices)

        child = xover(parent1, parent2)
        newpop.append(child)

    # randomly mutate 4% of genes
    for i in range(1,len(newpop)):
        for k in range(0,len(newpop[i])):
            if (random.uniform(0,1) < 0.04):
                newpop[i][k] += random.uniform(-0.4,0.4)

    # Create remaining children randomly
    while (len(newpop) < len(population)):
        newpop.append(np.random.standard_t(DF,N_GENES))

    assert (len(newpop) == len(population)), "Population size"
    return newpop

def xover(p1,p2):
    x1 = random.randrange(0,N_GENES)
    x2 = random.randrange(x1,N_GENES)
    child = np.concatenate((p1[0:x1], p2[x1:x2], p1[x2:]))
    return child

# http://stackoverflow.com/questions/3679694/
def weighted_choice(choices):
   total = sum(w for c, w in choices)
   r = random.uniform(0, total)
   upto = 0
   for c, w in choices:
      if upto + w > r:
         return c
      upto += w
   assert False, "Shouldn't get here"

def train_ga():
    # Initialize population
    # generation:
        # play each individual against every other individual 3 times
        # breed new population

    N = 40
    population = initialize_population(N)

    games_per_generation = 4 * ((N-1)*(N) / 2)
    generation = 0

    while (1):
        tic = time.time()
        generation += 1
        wins = np.array([0.]*N)
        losses = np.array([0.]*N)
        ties = np.array([0.]*N)

        game = 1

        for q in range(0,4):    # four games each
            for i in range(0,N):
                for k in range(i+1,N):
                    result = capitals.capitals(population[i], population[k])
                    print("    game %d / %d, (i/k %d/%d), res: %s" % (game, games_per_generation, i,k,result))
                    if (result == 'none'):
                        ties[k] += 1
                        ties[i] += 1
                    elif (result == 'red'):
                        wins[i] += 1
                        losses[k] += 1
                    elif (result == 'blue'):
                        wins[k] += 1
                        losses[i] += 1
                    game += 1

        fitness = 3*wins + 1*ties # + 0*losses

        bidx = fitness.argmax()
        wr = wins[bidx] / (wins[bidx] + losses[bidx] + ties[bidx])
        lr = losses[bidx] / (wins[bidx] + losses[bidx] + ties[bidx])
        tr = ties[bidx] / (wins[bidx] + losses[bidx] + ties[bidx])

        toc = time.time()
        print("Elapsed: %d s" % int(toc-tic))
        print("Generation %d best individual %d fitness %d (w%.2f l%.2f t%.2f)" % \
            (generation, bidx, fitness[bidx], wr, lr, tr))
        print(population[bidx])
        print("Entire population:")
        for i,individual in enumerate(population):
            print("    %s (%d)" % (individual, fitness[i]))

        population = breed(population, fitness)

if __name__ == '__main__':
    train_ga()
