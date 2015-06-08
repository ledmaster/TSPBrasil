#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
from collections import namedtuple
from random import randint,uniform,shuffle,choice,seed

town = namedtuple("town", ['id','name','lat', 'long'])

def length(town1, town2):
    R = 6371.
    x = (town2.long - town1.long) * math.cos((town2.lat + town1.lat)/2.)
    y = town2.lat - town1.lat
    return math.sqrt(x**2 + y**2) * R


def selectNextTour2Opt(solution, townCount):
    first = randint(0,townCount)
    last = randint(first,townCount)
    
    slice = solution[first:last+1]
    slice.reverse()
    new_solution = solution[:first] + slice + solution[last+1:]

    return new_solution


def costSolution(new_solution,town_list,townCount):
    new_obj = length(town_list[new_solution[-1]], town_list[new_solution[0]])
    for index in range(0, townCount-1):
        new_obj += length(town_list[new_solution[index]], town_list[new_solution[index+1]])

    return new_obj

def expCoinFlip(newCost,obj,T):
    p = math.exp( -(newCost - obj) / T )
    u = uniform(0,1)

    if u < p:
        return True
    return False

def greedy(sol, townCount,town_list):
    
    for i in xrange(townCount-1):
        cost = length(town_list[sol[i]], town_list[sol[i+1]])
        for j in xrange(i+2,townCount):
            cost2 = length(town_list[sol[i]], town_list[sol[j]])
            
            if cost2 < cost:
                old = sol[i+1]
                sol[i+1] = sol[j]
                sol[j] = old
                cost = cost2

    return sol


def parseInput():
    
    with open('MunicipiosBrasil.csv','r') as input_data_file:
        town_list = [l.split(';')[:4] for l in input_data_file.read().split('\r')[1:]]
        
        town_list = [town(int(t[0])-1,t[3] ,math.radians(float(t[1].replace(',','.'))), math.radians(float(t[2].replace(',','.')))) for t in town_list]
        
        townCount = int(len(town_list))

        return town_list, townCount


def solve_it(town_list):

    solution = range(0, townCount)
    solution = greedy(solution,townCount,town_list)


    # 2 - opt

    obj = costSolution(solution,town_list,townCount)
    print 'Initial', obj

    init_T = 1.
    final_T = 1e-10
    T = init_T


    min_obj = obj

    for i in xrange(1000000):

        new_solution = selectNextTour2Opt(solution,townCount)
        
        
        newCost = costSolution(new_solution,town_list,townCount)
        if newCost < obj:
            obj = newCost
            solution = new_solution[:]
        elif expCoinFlip(newCost,obj,T):
            solution = new_solution[:]
            obj = newCost


        if obj < min_obj:
            
            min_obj = obj
            print 'Epoch',i,'Objective', min_obj

        T = 0.999 * T



        if T <= final_T:
            T = init_T


#   output_data = str(obj) + ' ' + str(0) + '\n'
#   output_data += ' '.join(map(str, solution))

#return output_data


import sys

if __name__ == '__main__':
    town_list,townCount = parseInput()
    solve_it(town_list)

