import schemdraw as sch
import schemdraw.elements as elm

def generateDiagram(circuitGraph):


    return

graph = {'POW': ['RAIL1'],
         'RAIL 1': ['POW', 'RES 1 100Ω'],
         'RES 1 100Ω': ['RAIL 1', 'RAIL 2'],
         'RAIL 2': ['RES 1 100Ω', 'CAP 1 0.1μF'],
         'CAP 1 0.1μF': ['RAIL 2', 'RAIL 3'],
         'RAIL 3': ['CAP 1 0.1μF', 'GND'],
         'GND': ['RAIL 3']}

def isPath(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    if not start in graph:
        return False
    for node in graph[start]:
        if node not in path:
            newpath = isPath(graph, node, end, path)
            if newpath: return True
    return False
def findPath(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    if not start in graph:
        return None
    for node in graph[start]:
        if node not in path:
            newpath = findPath(graph, node, end, path)
            if newpath: return newpath
    return None
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
def findShortestPath(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    if not graph.has_key(start):
        return None
    shortest = None
    for node in graph[start]:
        if node not in path:
            newpath = findShortestPath(graph, node, end, path)
            if newpath:
                if not shortest or len(newpath) < len(shortest):
                    shortest = newpath
    return shortest

print(findPath(graph, 'POW', 'GND'))
print(isPath(graph, 'POW', 'GND'))
print(isPath(graph, 'GND', 'POW'))
print(findAllPaths(graph, 'POW', 'GND'))
