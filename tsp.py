import random

def randomSolution(tsp):
    customers = list(range(len(tsp)))
    solution = []

    for i in range(len(tsp)):
        Select_customer = customers[random.randint(0, len(customers) - 1)]
        solution.append(Select_customer)
        customers.remove(Select_customer)

    return solution

def routeLength(tsp, solution):
    routeLength = 0
    for i in range(len(solution)):
        routeLength += tsp[solution[i - 1]][solution[i]]
    return routeLength

def getNeighbours(solution):
    neighbours = []
    for i in range(len(solution)):
        for j in range(i + 1, len(solution)):
            neighbour = solution.copy()
            neighbour[i] = solution[j]
            neighbour[j] = solution[i]
            neighbours.append(neighbour)
    return neighbours

def getBestNeighbour(tsp, neighbours):
    bestRouteLength = routeLength(tsp, neighbours[0])
    bestNeighbour = neighbours[0]
    for neighbour in neighbours:
        currentRouteLength = routeLength(tsp, neighbour)
        if currentRouteLength < bestRouteLength:
            bestRouteLength = currentRouteLength
            bestNeighbour = neighbour
    return bestNeighbour, bestRouteLength

def hillClimbing(tsp):
    currentSolution = randomSolution(tsp)
    currentRouteLength = routeLength(tsp, currentSolution)
    neighbours = getNeighbours(currentSolution)
    bestNeighbour, bestNeighbourRouteLength = getBestNeighbour(tsp, neighbours)

    while bestNeighbourRouteLength < currentRouteLength:
        currentSolution = bestNeighbour
        currentRouteLength = bestNeighbourRouteLength
        neighbours = getNeighbours(currentSolution)
        bestNeighbour, bestNeighbourRouteLength = getBestNeighbour(tsp, neighbours)

    return currentSolution, currentRouteLength

def main():

    SS = 0
    SA = int(input("Please enter The distance between distribution center and customer A:\n"))
    SB = int(input("Please enter The distance between distribution center and customer B:\n"))
    SC = int(input("Please enter The distance between distribution center and customer C:\n"))
    SD = int(input("Please enter The distance between distribution center and customer D:\n"))
    SE = int(input("Please enter The distance between distribution center and customer E:\n"))

    AS = SA
    AA = 0
    AB = int(input("Please enter The distance between customer A and customer B:\n"))
    AC = int(input("Please enter The distance between customer A and customer C:\n"))
    AD = int(input("Please enter The distance between customer A and customer D:\n"))
    AE = int(input("Please enter The distance between customer A and customer E:\n"))

    BS = SB
    BA = AB
    BB = 0
    BC = int(input("Please enter The distance between customer B and customer C:\n"))
    BD = int(input("Please enter The distance between customer B and customer D:\n"))
    BE = int(input("Please enter The distance between customer B and customer E:\n"))

    CS = SC
    CA = AC
    CB = BC
    CC = 0
    CD = int(input("Please enter The distance between customer C and customer D:\n"))
    CE = int(input("Please enter The distance between customer C and customer E:\n"))

    DS =SD
    DA = AD
    DB = BD
    DC = CD
    DD = 0
    DE = int(input("Please enter The distance between customer D and customer E:\n"))

    ES=SE
    EA = AE
    EB = BE
    EC = CE
    ED = DE
    EE = 0

    tsp = [
        [SS,SA,SB,SC,SD,SE],
        [AS,AA,AB,AC,AD,AE],
        [BS,BA,BB,BC,BD,BE],
        [CS,CA,CB,CC,CD,CE],
        [DS,DA,DB,DC,DD,DE],
        [ES,EA,EB,EC,ED,EE]
    ]


    Result = hillClimbing(tsp)
    Optimal_PathLength = Result[1]
    Optimal_Route = Result[0]
    target_index = Optimal_Route.index(0)
    array_start = Optimal_Route[target_index:]
    array_end = Optimal_Route[:target_index + 1]

    Best_Route = array_start + array_end

    print("\n")
    print("The shortest possible length distance is : ", Optimal_PathLength)
    print("\n")
    print("The optimal path is : ", Best_Route)
    print("\n")
    print ("Please note : \n")
    print("0 indicates distribution center \n")
    print("1 indicates customer A \n")
    print("2 indicates customer B \n")
    print("3 indicates customer C \n")
    print("4 indicates customer D \n")
    print("5 indicates customer E \n")

if __name__ == "__main__":
    main()
