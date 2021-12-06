import random
import numpy as np
import sys
from collections import defaultdict

class Ant:
    def __init__(self, items):
        self.path = np.zeros(items)
        self.fitness=-1

    def addTo(self, nextBin, i):
      self.path[i] = nextBin

    def getFitness(self):
        return self.fitness
    
    def getBin(self,i):
        return self.path[i]
    
    def updateFitness(self, b, BPP1):
        temp_bins = np.zeros(b)
      
        for i in range(0, len(self.path)):
            if BPP1:
                temp_bins[int(self.path[i])] = temp_bins[int(self.path[i])] + (i+1)
            else:
                weight=((i+1)**2)/2
                temp_bins[int(self.path[i])] = temp_bins[int(self.path[i])] + weight

        temp_bins=np.sort(temp_bins)
        heaviest = temp_bins[-1]
        lightest = temp_bins[0]
        '''
        lightest=sys.maxsize
        heaviest=-lightest-1 

        for i in range(0, len(temp_bins)):
            if(temp_bins[i] > heaviest):
                heaviest=temp_bins[i]

            if (temp_bins[i] < lightest):
                lightest = temp_bins[i]
        '''
        self.fitness = heaviest - lightest

    def toString(self, bins, items):
        
        bin_dict = {}
        for i in range(0,bins):
            bin = []
            for j in range(0,items):
                if int(self.path[j]) == i:
                    bin.append(j+1)
            bin_dict['Bin '+str(i+1)] = bin
        return bin_dict
            
        '''bin_dict = defaultdict(list)
        output=""
        for i in range(0,len(self.path)):
            self.path[i]+1
            output+= "item: " + str(i+1) + " in bin: " + str(int(self.path[i]+1)) + "\n"
        output+="Total fitness is" + str(self.fitness) + "\n"
        output+="\n"
        return output'''
        

class Matrix:
    #number of rows = bins
    #number of columns = items
  
    def __init__(self, bins, items):
        self.bins=bins
        self.items=items
        self.adjMatrix = np.zeros((bins, items))


        #print(self.adjMartrix)
        #for b in range(0, bins):
        #self.adjMatrix.append([0 for i in range(0, items)])


    def randomPheromones(self):
        for b in range(0,self.bins):
            for i in range(0,self.items):
                self.adjMatrix[b][i]= random.random()
        

    def getBins(self):
        return self.bins

    def getItems(self):
        return self.items

    def get(self, bins, items):
        return self.adjMatrix[bins][items]

    def multiply(self, x):
        result = Matrix(self.bins, self.items)
        for b in range(0,self.bins):
            for i in range(0,self.items):
                result.set(b, i, x)
        return result

    def set(self,bins, items, value):
        self.adjMatrix[bins][items] = value

    def toString(self):
        bins = self.getBins()
        items = self.getItems()
        
        matrixString = ""
        i=0
        j=0

        for i in range(0, bins):
            for j in range(0, items):
                if (j == bins-1):
                    matrixString += str(round(self.adjMatrix[i][j],3))
                else:
                    matrixString += str(round(self.adjMatrix[i][j],3)) + ","
            matrixString += "\n"
        return matrixString

'''
def binary_search_recursive(array, element, start, end):
    if start > end:
        return -1

    mid = (start + end) // 2
    if element == array[mid]:
        return mid

    if element < array[mid]:
        return binary_search_recursive(array, element, start, mid-1)
    else:
        return binary_search_recursive(array, element, mid+1, end)
'''    


def chooseBin(curItem, conGraph):
    bins = conGraph.getBins()

    fitness = np.zeros(bins)
    #fitness = [0.0 for x in range(0,bins)]

    fitness[0] = conGraph.get(0, curItem)

    for i in range(1, bins):
        fitness[i] = fitness[i-1] + conGraph.get(i, curItem)

    randomV = random.random() * fitness[bins-1]
    binNum=np.searchsorted(fitness, randomV)
    #binNum = binary_search_recursive(fitness, randomV, 0, len(fitness))

    if (binNum < 0):
        binNum = abs(binNum)
    return binNum



def antColony(graph, p, e, b, k):

    #array of ants
    antPopulation = []
    
    #fitness evaluations
    count = 0
    #begin
    while(True):
        #create p ants
        for a in range(0, p):
            #create ant
            tempAnt = Ant(k)

            #for each item, choose the bin
            for i in range(0, k):
                nextBin = chooseBin(i, graph)
                tempAnt.addTo(nextBin, i)


            #update fitness and increase count
            tempAnt.updateFitness(b, True)
            count+=1


            #Add the ant's solution to the population of solutions
            antPopulation.append(tempAnt)


        pop_it = antPopulation.copy()
        while len(pop_it)>0:
            tempAnt = pop_it.pop(0)
            phmUpdate = 100/tempAnt.getFitness()

            for c in range(0,k):
                graph.set(int(tempAnt.getBin(c)), c, graph.get(int(tempAnt.getBin(c)), c) + phmUpdate)

      
        graph = graph.multiply(e)

        

        if count >= 10000:
            antPopulation.sort(key=lambda x: x.getFitness(), reverse=False)
            print("best solution is "+ str(antPopulation[0].getFitness()))
            return antPopulation[0]

        
        '''
        antPopulation.sort(key=lambda x: x.getFitness(), reverse=False)
        if antPopulation[0].getFitness() < best:
            best = antPopulation[0].getFitness()#
        '''

        antPopulation=[]


        
population = 10
evaporation = 0.6
bins = 50
items = 500
conGraph = Matrix(bins, items)
conGraph.randomPheromones()
#print('TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT')
#print(conGraph.multiply(1000))

result = antColony(conGraph, population, evaporation, bins, items)
bin_assigment = result.toString(bins, items)
for i in range(0,bins):
    print('Bin '+str(i+1)+str(bin_assigment['Bin '+str(i+1)]))