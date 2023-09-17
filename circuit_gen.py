import schemdraw as sch
import schemdraw.elements as elm


def generateDiagram(circuitGraph, vcc: str):
    # Checks if circuit is complete
    if not isPath(circuitGraph, "POW", "GND"):
        print("Invalid circuit: power and ground not connected")
        return None

    with sch.Drawing(show=False,file="circuit_out.svg") as d:
        # create a vertical line from Vcc to ground using the shortest circuit path
        shortestPath = findShortestPath(circuitGraph, "POW", "GND")
        for node in shortestPath:
            # Each node should be a component name (RES, CAP, RAIL, etc) followed by a unique identifier
            # followed by a value (if the node is a component with a resistance or other value to be labeled)
            args = node.split(" ")
            if args[0] == "POW":
                d += elm.Vdd().right().label(vcc)
                d.push()

            elif args[0] == "RAIL":
                d += elm.Line().down()
                d.push()

            elif args[0] == "RES":
                if not len(args) == 3:
                    print("Invalid Resistor node:", node)
                    return None
                d += elm.Resistor().down().label(args[2])
                d.push()

            elif args[0] == "CAP":
                if not len(args) == 3:
                    print("Invalid Capacitor node:", node)
                    return None
                d += elm.Capacitor().down().label(args[2])
                d.push()

            elif args[0] == "IND":
                if not len(args) == 3:
                    print("Invalid Inductor node:", node)
                    return None
                d += elm.Inductor().down().label(args[2])
                d.push()

            elif args[0] == 'GND':
                    d += elm.Ground().right()

            else:
                print("Unknown node:", node)
                return None

        # now to handle all of the branches of this main line :D
        # tracker variables for farthest left and right distance from main line
        right = 0
        left = 0
        # tracker for how far from ground you are
        height = 0
        reversePath = reversed(shortestPath)
        for node in reversePath:
            d.pop()
            pathsTaken = 0
            paths = findAllPaths(circuitGraph, node, "GND")
            if len(paths) > 1:
                for path in paths:
                    if not path[1] in shortestPath:
                        d += elm.Dot()
                        if pathsTaken == 0:
                            right = rightBranch(
                                right,
                                height,
                                d,
                                findAllPaths(circuitGraph, path[1], "GND"),
                                path[0],
                            )
                            pathsTaken += 1
                        elif pathsTaken == 1:
                            left = leftBranch(
                                left,
                                height,
                                d,
                                findAllPaths(circuitGraph, path[1], "GND"),
                                path[0],
                            )
                            pathsTaken += 1

            height += 1
    return


# the drawing will have been popped to the correct location
# l: required lateral distance from center to avoid other branches
def leftBranch(l: int, h: int, d: sch.Drawing, paths, parent):
    d.push()
    numPaths = len(paths)
    lDist = 0  # current distance from center
    # go to furthest point away from center
    while lDist < l:
        d += elm.Line().left()
        lDist += 1
    if numPaths <= 3:
        for path in paths:
            if path[1] != parent:
                d += elm.Line().left()
                lDist += 1
                for node in path:
                    if node.split(" ")[0] in "RES CAP IND":
                        drawComp("d", node, d)
                        h -= 1
    for path in paths:
        break

    if lDist > l:
        l = lDist
    while h > 0:
        d += elm.Line().down()
        h -= 1
    while lDist > 0:
        d += elm.Line().right()
        lDist -= 1
        d.pop()
    return l


# the drawing will have been popped to the correct location
# r: required lateral distance from center to avoid other branches
def rightBranch(r: int, h: int, d: sch.Drawing, paths, parent):
    d.push()
    numPaths = len(paths)
    rDist = 0  # current distance from center
    # go to furthest point away from center
    while rDist < r:
        d += elm.Line().right()
        rDist += 1
    if numPaths <= 3:
        for path in paths:
            if path[1] != parent:
                d += elm.Line().right()
                rDist += 1
                for node in path:
                    if node.split(" ")[0] in "RES CAP IND":
                        drawComp("d", node, d)
                        h -= 1
    for path in paths:
        break

    if rDist > r:
        r = rDist
    while h > 0:
        d += elm.Line().down()
        h -= 1
    while rDist > 0:
        d += elm.Line().left()
        rDist -= 1
        d.pop()
    return r


# returns the number of non-wire components in a given path
def numComps(path):
    i = 0
    for node in path:
        if node.split(" ")[0] in "RES CAP IND":
            i += 1
    return i


# draws a single circuit component in a given direction
def drawComp(dir: str, comp: str, d: sch.Drawing):
    args = comp.split(" ")
    if dir == "l":
        if args[0] == "RES":
            d += elm.Resistor().left().label(args[2])
        elif args[0] == "CAP":
            d += elm.Capacitor().left().label(args[2])
        elif args[0] == "IND":
            d += elm.Inductor().left().label(args[2])
    elif dir == "r":
        if args[0] == "RES":
            d += elm.Resistor().right().label(args[2])
        elif args[0] == "CAP":
            d += elm.Capacitor().right().label(args[2])
        elif args[0] == "IND":
            d += elm.Inductor().right().label(args[2])
    elif dir == "d":
        if args[0] == "RES":
            d += elm.Resistor().down().label(args[2])
        elif args[0] == "CAP":
            d += elm.Capacitor().down().label(args[2])
        elif args[0] == "IND":
            d += elm.Inductor().down().label(args[2])


graph = {
    "POW": ["RAIL 1"],
    "RAIL 1": ["POW", "RES 1 100Ω"],
    "RES 1 100Ω": ["RAIL 1", "RAIL 2"],
    "RAIL 2": ["RES 1 100Ω", "CAP 1 0.1μF"],
    "CAP 1 0.1μF": ["RAIL 2", "RAIL 3"],
    "RAIL 3": ["CAP 1 0.1μF", "GND"],
    "GND": ["RAIL 3"],
}

graph2 = {
    "POW": ["RAIL 1"],
    "RAIL 1": ["POW", "RES 1 1.35KΩ"],
    "RES 1 1.35KΩ": ["RAIL 1", "RAIL 2"],
    "RAIL 2": ["RES 1 1.35KΩ", "RES 2 2KΩ", "CAP 3 15nF", "IND 1 1H"],
    "RES 2 2KΩ": ["RAIL 2", "RAIL 3"],
    "CAP 1 10nF": ["RAIL 4", "RAIL 5"],
    "CAP 2 1.5μF": ["RAIL 6", "RAIL 7"],
    "CAP 3 15nF": ["RAIL 2", "RAIL 3"],
    "IND 1 1H": ["RAIL 2", "RAIL 3"],
    "RAIL 3": ["RES 2 2KΩ", "GND", "CAP 3 15nF", "IND 1 1H"],
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
