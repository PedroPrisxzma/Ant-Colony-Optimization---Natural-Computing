import numpy as np
from copy import deepcopy

class Graph:
    def __init__(self, keys_num=None):
        """ Initialize a new Graph, needs to receive the number of nodes
            (keys_num), to start a new graph.
        """
        new_graph = {}
        if(keys_num == None):
            self.graph = new_graph
        else:
            for i in range(1, keys_num+1):
                new_graph[i] = {}
            self.graph = new_graph

    def add_vert(self, vertice):
        self.graph[vertice] = {}

    def vertices(self):
        """ returns the vertices of the graph """
        return list(self.graph.keys())

    def edges(self):
        """ returns the edges of the graph """
        return self.__gen_edges()

    def __gen_edges(self):
        """ A static method generating the edges of the
            graph. Edges are represented as tuples
            with one (a loop back to the vertex) or two
            vertices, weight and pheromone
        """
        edges = []
        for vertex in self.graph:
            for neighbour in self.graph[vertex]:
                """ Check if an edge is already on the list """
                if([vertex, neighbour, self.graph[vertex][neighbour][0], self.graph[vertex][neighbour][1]]) not in edges:
                    edges.append([vertex, neighbour, self.graph[vertex][neighbour][0], self.graph[vertex][neighbour][1]])
        return edges

    def add_edge(self, edge):
        """ assumes that edge is of type set, tuple;
            between two vertices can be multiple edges!
            must add the edge from one vertice to the neighbour and the same edge backwards
        """
        v = edge[0] # One vertice
        n = edge[1] # neighbour vertice
        w = edge[2] # Edge weight

        if(v in self.graph):
            self.graph[v][n] = [w, 1]
        else:
            print("Vertice not found in graph!")

    def add_pherom(self, vertice, neighbour, amount):
        '''Update pheromone level to amount'''
        for i in range(len(self.graph[vertice])):
            if(self.graph[vertice][i][0] == neighbour):
                self.graph[vertice][i] = (self.graph[vertice][i][0], self.graph[vertice][i][1], amount)

        for i in range(len(self.graph[neighbour])):
            if(self.graph[neighbour][i][0] == vertice):
                self.graph[neighbour][i] = (self.graph[neighbour][i][0], self.graph[neighbour][i][1], amount)

        print(self.graph)

    def __str__(self):
        """ Used for fast printing """
        g = "vertices: "
        for k in self.graph:
            g += str(k) + " "
        g += "\nedges: "
        for edge in self.__gen_edges():
            g += str(edge) + " "
        return g

class Ant:
    def __init__(self, gen, n, seed):
        self.atual = 1
        self.caminho = [1]
        self.peso = 0
        self.id = (gen, n, seed)

    def update_weight(self, amount):
        '''update weight'''
        self.peso = self.peso + amount

    def update_path(self, vert):
        '''update ant's path'''
        self.atual = vert
        self.caminho.append(vert)

class Aco:
    def __init__(self, graph, evaporation):
        self.aco_graph = graph
        self.evap_rate = evaporation

    def valid_ant(self, ant, valids):
        # appends valid ant to valid ants list
        valids.append(ant)

    def best_ants(self, valids, best):
        # appends best ant to best ants per 'caminhamento'
        sort = sorted(valids, key=lambda x: -x.peso)
        best.append(sort[0])

    def walk_ant(self, ant, valid_ants):
        #Checks if solution has been found
        while(1):
            vizinho = [i for i in self.aco_graph[ant.atual] if i not in ant.caminho]

            if(ant.atual == len(list(self.aco_graph.keys()))):
                self.valid_ant(ant, valid_ants)
                break
            elif((len(vizinho) == 0) or (vizinho == None) or (len(vizinho) < 0)):
                break
            # Checks for valid vertex
            elif(len(vizinho) > 0):
                chances = [0 for i in vizinho]
                total = 0
                for j in range(len(vizinho)):
                    total = total + (self.aco_graph[ant.atual][vizinho[j]][0] * self.aco_graph[ant.atual][vizinho[j]][1])
                    chances[j] = self.aco_graph[ant.atual][vizinho[j]][0] * self.aco_graph[ant.atual][vizinho[j]][1]
                for j in range(len(chances)):
                    # Checks division by 0
                    if(total != 0):
                        chances[j] = chances[j]/total
                    else:
                        chances[j] = chances[j] - chances[j]
                next_vert = np.random.choice(vizinho, 1, chances)[0]

                ant.update_weight(self.aco_graph[ant.atual][next_vert][0])
                ant.update_path(next_vert)

    def pherom_update(self, valid_ants):
        # (Pheromone *(1-evaporation) + weight of path )/total vertice cost
        # Note that first all pheromone must be deposited on path before normalizing
        total = self.weight_graph()

        # Evaporation on all vertices
        for i in self.aco_graph:
            for j in self.aco_graph[i]:
                self.aco_graph[i][j][1] = self.aco_graph[i][j][1]*(1-self.evap_rate)

        # Pheromone deposits on all the necessary edges
        for a in valid_ants:
            for i in range(len(a.caminho)-1):
                self.aco_graph[a.caminho[i]][a.caminho[i+1]][1] = (self.aco_graph[a.caminho[i]][a.caminho[i+1]][1] + a.peso)

        # Normalize
        for i in self.aco_graph:
            for j in self.aco_graph[i]:
                self.aco_graph[i][j][1] = self.aco_graph[i][j][1]/total

    def weight_graph(self):
        total = 0
        for i in self.aco_graph:
            for j in self.aco_graph[i]:
                total = total + self.aco_graph[i][j][1]
        return total
