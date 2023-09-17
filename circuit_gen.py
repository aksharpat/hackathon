import schemdraw as sch
import schemdraw.elements as elm


def generateDiagram(circuitGraph, vcc: str):
    # Checks if circuit is complete
    if not isPath(circuitGraph, "POW", "GND"):
        print("Invalid circuit: power and ground not connected")
        return None

    with sch.Drawing(file="circuit_out.svg") as d:
        # create a vertical line from Vcc to ground using the shortest circuit path
        shortestPath = findShortestPath(circuitGraph, "POW", "GND")
        for node in shortestPath:
            # Each node should be a component name (RES, CAP, RAIL, etc) followed by a unique identifier
            # followed by a value (if the node is a component with a resistance or other value to be labeled)
            args = node.split(" ")

            if args[0] == "POW":
                d += elm.Vdd().label(vcc)
                d.push()

            elif args[0] == "GND":
                d += elm.Ground().right()

            elif args[0] == "RAIL":
                if "POW" in circuitGraph[node]:
                    d += elm.Line().down()
                d.push()

            elif args[0] == "RES":
                if not len(args) == 3:
                    print("Invalid Resistor node:", node)
                    return None
                d += elm.Resistor().down().label(args[2])

            elif args[0] == "CAP":
                if not len(args) == 3:
                    print("Invalid Capacitor node:", node)
                    return None
                d += elm.Capacitor().down().label(args[2])

            elif args[0] == "IND":
                if not len(args) == 3:
                    print("Invalid Inductor node:", node)
                    return None
                d += elm.Inductor().down().label(args[2])

            else:
                print("Unknown node:", node)
                return None

    return


graph = {
    "POW": ["RAIL 1"],
    "RAIL 1": ["POW", "RES 1 100Ω"],
    "RES 1 100Ω": ["RAIL 1", "RAIL 2"],
    "RAIL 2": ["RES 1 100Ω", "CAP 1 0.1μF"],
    "CAP 1 0.1μF": ["RAIL 2", "RAIL 3"],
    "RAIL 3": ["CAP 1 0.1μF", "GND"],
    "GND": ["RAIL 3"],
}

# returns a boolean of whether a path exists between two graph nodes
def isPath(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    if not start in graph:
        return False
    for node in graph[start]:
        if node not in path:
            newpath = isPath(graph, node, end, path)
            if newpath:
                return True
    return False


# returns the first path found between two nodes in a graph
def findPath(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    if not start in graph:
        return None
    for node in graph[start]:
        if node not in path:
            newpath = findPath(graph, node, end, path)
            if newpath:
                return newpath
    return None


# finds all paths between two nodes in a graph
def findAllPaths(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    if not start in graph:
        return []
    paths = []
    for node in graph[start]:
        if node not in path:
            newpaths = findAllPaths(graph, node, end, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths


# finds the shortest path between two nodes in a graph
def findShortestPath(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    if not start in graph:
        return None
    shortest = None
    for node in graph[start]:
        if node not in path:
            newpath = findShortestPath(graph, node, end, path)
            if newpath:
                if not shortest or len(newpath) < len(shortest):
                    shortest = newpath
    return shortest


# print(findShortestPath(graph, "POW", "GND"))
# print(isPath(graph, "POW", "GND"))
# print(isPath(graph, "GND", "POW"))
# print(findAllPaths(graph, "POW", "GND"))
# generateDiagram(graph, "3.3V")
