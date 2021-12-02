import random

class Ant:
    # Class attribute
    path=[]
    fitness=-1

    def __init__(self, items):
        self.path = [x for x in range(0,items)]
        self.fitness=-1

    def addTo(self, nextBin, i):
      self.path[i]=nextBin


    def getFitness(self):
        return self.fitness
    
    def getBin(self,i):
        return self.path[i]
    
    def updateFitness(self, b):
        temp_bins = [x for x in range(0,len(b))]

        for i in range(0,len(self.path)-1):
            temp_bins[self.path[i]] = temp_bins[self.path[i]] +(i+1)

        heaviest=0
        lightest=0

        for i in range(0, len(temp_bins)):
            if(temp_bins[i]> heaviest):
                heaviest=temp_bins[i]

            if (temp_bins[i] < lightest):
                lightest = temp_bins[i]

        self.fitness = heaviest - lightest

    def toString(self):
        output=""
        for i in range(0,len(self.path)):
            output+= "item: " + str(i+1) + " in bin: " + str(self.path[i]+1) + "\n"
        output+="Total fitness is" + str(self.fitness) + "\n"
        output+="\n"
        return output

class Matrix:
    #number of rows = bins
    #number of columns = items
    rows=0
    columns=0
    adjMatrix=[]

    def __init__(self, bins, items):
        self.rows=bins
        self.columns=items
        for b in range(0, bins):
            self.adjMatrix.append([0 for i in range(0, items)])


    def randomPheromones(self):
        for r in range(0,self.rows-1):
            for c in range(0,self.columns-1):
                self.adjMatrix[r][c]= random.randint(0,1)

    def getRows(self):
        return self.rows

    def getColumns(self):
        return self.columns

    def get(self, r, c):
        return self.adjMatrix[r][c]

    def multiply(self, x):
        result=Matrix(self.rows, self.columns)
        for r in range(0,self.rows-1):
            for c in range(0,self.columns-1):
                result.adjMatrix[r][c] = x * self.adjMatrix[r][c]
        return result

    def toString(self):
        thisRow = self.getRows()
        thisCol = self.getColumns()
        
        matrixString = ""
        i=0
        j=0

        for i in range(0, thisRow-1):
            for j in range(0, thisCol-1):
                if (j== thisCol-1):
                    matrixString += str(round(float(self.adjMatrix[i][j]),3))
                else:
                    matrixString += str(round(float(self.adjMatrix[i][j]),3)) + ","
            matrixString += "\n"

        return matrixString

    



population = 10
evaporation = 0.8
bins = 10
items = 500
conGraph = Matrix(bins, items)
conGraph.randomPheromones()


def antColony(graph, p, e, b, k):

    #array of ants
    antPopulation = []
    
    #fitness evaluations
    count = 0

    while(True):
        for a in range(0, len(p)-1):
            tempAnt = Ant(k)
            for i in range(0,k-1):
                





        
