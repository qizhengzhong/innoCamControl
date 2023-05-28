import sys
from multiAgent.sharedInformation.PhysicalProperty import PhysicalProperty
from multiAgent.sharedInformation.ProductState import ProductState
from multiAgent.sharedInformation.ResourceEvent import ResourceEvent


class DirectedSparseGraph(dict):
    def __init__(self):
        self.name = 'graph'
        self.vertices = []
        self.edges = []

    def addEdge(self, event, start_vertex, end_vertex):
        #self.edges.append(ResourceEvent(start_vertex, end_vertex, None, event.eventTime))

        self.edges.append(event)

        self.addVertex(start_vertex)
        self.addVertex(end_vertex)
        
        if start_vertex not in self.keys():
            self[start_vertex] = {}
        self[start_vertex][end_vertex] = event.eventTime

    def addVertex(self, vertex):
        if vertex not in self.vertices:
            self.vertices.append(vertex)

    def getEdges(self):
        return self.edges

    def getVertices(self):
        return self.vertices

    def copy(self):
        new_graph = DirectedSparseGraph()
        for vertex in self.vertices:
            new_graph.addVertex(vertex)
        for vertex1, vertex2 in self.edges:
            new_graph.addEdge(vertex1, vertex2)
        return new_graph

    def clean(self):
        pass


class DijkstraShortestPath():
    def __init__(self, environmentModel, weightTransformer):
        self.name = 'DijkstraShortestPath'
        self.graph = environmentModel

    def reset(self):
        pass

    def get_outgoing_edges(self, node):
        "Returns the neighbors of a node."
        connections = []
        if node in self.graph.keys():
            for out_node in self.graph[node]:
                connections.append(out_node)
        return connections

    def getPath(self, start_vertex: ProductState, end_vertex: ProductState):
        g = self.graph
        unvisited_nodes = list(g.getVertices())
        # We'll use this dict to save the cost of visiting each node and update it as we move along the graph
        shortest_path = {}

        # We'll use this dict to save the shortest known path to a node found so far
        previous_nodes = {}

        # We'll use max_value to initialize the "infinity" value of the unvisited nodes
        max_value = sys.maxsize
        for node in unvisited_nodes:
            shortest_path[node] = max_value
        # However, we initialize the starting node's value with 0
        shortest_path[start_vertex] = 0

        # The algorithm executes until we visit all nodes
        while unvisited_nodes:
            # The code block below finds the node with the lowest score
            current_min_node = None
            for node in unvisited_nodes:  # Iterate over the nodes
                if current_min_node == None:
                    current_min_node = node
                elif shortest_path[node] < shortest_path[current_min_node]:
                    current_min_node = node

            # The code block below retrieves the current node's neighbors and updates their distances
            neighbors = self.get_outgoing_edges(current_min_node)
            for neighbor in neighbors:
                tentative_value = shortest_path[current_min_node] + g[current_min_node].get(neighbor)
                if tentative_value < shortest_path[neighbor]:
                    shortest_path[neighbor] = tentative_value
                    # We also update the best path to the current node
                    previous_nodes[neighbor] = current_min_node

            # After visiting its neighbors, we mark the node as "visited"
            unvisited_nodes.remove(current_min_node)

        return previous_nodes, shortest_path[end_vertex]

    def getWeightTransformer(self):
        pass

if __name__ == '__main__':

    startingBuffer = "EnterBuffer"
    startingBufferPosition = [0, 0]
    endBufferPosition = [0, 1]

    # Initialize nodes and edges
    vertex1 = ProductState(startingBuffer, None, PhysicalProperty([0, 0]))
    vertex2 = ProductState(startingBuffer, None, PhysicalProperty([1, 1]))
    vertex3 = ProductState(startingBuffer, None, PhysicalProperty([1, 2]))
    vertex4 = ProductState(startingBuffer, None, PhysicalProperty([2, 2]))

    event1 = ResourceEvent(vertex1, vertex2, None, 1)
    event2 = ResourceEvent(vertex1, vertex3, None, 2)
    event3 = ResourceEvent(vertex2, vertex3, None, 3)
    event4 = ResourceEvent(vertex2, vertex4, None, 4)
    event5 = ResourceEvent(vertex3, vertex4, None, 5)

    # Add nodes and edges to graph
    bid = DirectedSparseGraph()
    bid.addVertex(vertex1)
    bid.addVertex(vertex2)
    bid.addVertex(vertex3)
    bid.addVertex(vertex4)
    bid.addEdge(event1, event1.getParent(), event1.getChild())
    bid.addEdge(event2, event2.getParent(), event2.getChild())
    bid.addEdge(event3, event3.getParent(), event3.getChild())
    bid.addEdge(event4, event4.getParent(), event4.getChild())
    bid.addEdge(event5, event5.getParent(), event5.getChild())

    previous_nodes, shortest_time = DijkstraShortestPath(bid, vertex1).getPath(vertex1, vertex4)
    print("The shortest time it spent for moving from the start_vertex to the end_vertex is " + shortest_time)
