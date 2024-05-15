from math import sqrt

def add_node(node):
    global graph
    global node_num
    if node in graph:
        raise IndexError('Node exists')
    else:
        node_num += 1
        graph[node] = []

def add_edge(n1, n2, weight):
    global graph
    if n1 not in graph:
        print('Node 1 ', n1, ' does not exist')
    elif n2 not in graph:
        print('Node 2 ', n2, ' does not exist')
    else:
        temp = [n2, weight]
        graph[n1].append(temp)

def print_graph(n):
    global graph
    if n == 'all':
        for node in graph:
            for edges in graph[node]:
                print(node, ' -> ', edges[0], 'edge weight: ', edges[1])
    else:
        print(graph[n])

def make_graph(frets, strings):
    global graph
    global node_num
    graph = {}
    node_num = 0
    nodeList = []
    for x in range(strings):
        for y in range(frets):
            name = f'[{str(x)}, {str(y)}]'
            nodeList.append([name, x, y])
            add_node(name)

    for i in range(0, len(nodeList)):
        for s in range(0, strings):
            for f in range(0, frets):
                name = f'[{str(s)}, {str(f)}]'
                if f == nodeList[i][2] and s == nodeList[i][1]:
                    weight = 0
                elif f == nodeList[i][2]:
                    weight = 1
                elif f == 0:
                    weight = 3
                else:
                    diffS = abs(s - nodeList[i][1])
                    diffF = abs(f - nodeList[i][2])
                    weight = round(sqrt(diffS ** 2 + diffF ** 2))
                add_edge(nodeList[i][0], name, weight)

def findWeight(n1,n2):
    global graph
    for i in graph[n1]:
        if i[0] == n2:
            return i[1]
    return 99999999999

def returnGraph():
    global graph
    return graph

if __name__ == '__main__':
    make_graph(20,6)
    # print_graph('[0, 0]')