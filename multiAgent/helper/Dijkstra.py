#https://gist.github.com/PyBagheri/fc9724e06cbfc046e9ee0874a1147eaa
# Author: Mohammadhossein Bagheri (@PyBagheri)
# License: MIT

import math

class Dijkstra:
    def __init__(self, graph, start_vertex):
        self.graph = graph;
        self.start_vertex = start_vertex
        self.vertices = list(graph.keys())

        # distance: minimum distance from start vertex
        self.vertex_labels = {vertex: {'distance': math.inf, 'prev': '-'} for vertex in self.vertices}

        # Obviously, the start vertex has no distance from itself
        self.vertex_labels[start_vertex]['distance'] = 0


    def _get_edge_weight(self, vertex1, vertex2):
        try:
            return self.graph[vertex1][vertex2]
        except KeyError:
            return math.inf


    def _set_label(self, vertex, weight, prev=''):
        self.vertex_labels[vertex]['distance'] = weight

        if prev:
            self.vertex_labels[vertex]['prev'] = prev


    def _get_label(self, vertex):
        return self.vertex_labels[vertex]


    def dijkstra(self):
        interiors = [self.start_vertex]
        max_interior_vertices = len(self.vertices)

        while True:
            exteriors = [vertex for vertex in self.vertices if vertex not in interiors]

            # Nearest vertex to start vertex
            nearest_vertex = '-'

            # Distance from start index
            nearest_vertex_distance = math.inf

            for exterior in exteriors:
                exterior_label = self._get_label(exterior)

                # Shortest discovered distance of current outerior from start vertex
                shortest_discovered_distance = exterior_label['distance']

                # Last vertex through which we reached current exterior with shortest distance
                choosen_prev = exterior_label['prev']

                for interior in interiors:
                    # Shortest discovered distance of current interior from start vertex + distance of current interior from current exterior
                    distance_from_exterior = self._get_label(interior)['distance'] + self._get_edge_weight(interior, exterior)

                    if distance_from_exterior < shortest_discovered_distance:
                        shortest_discovered_distance = distance_from_exterior
                        choosen_prev = interior
            
                self._set_label(exterior, shortest_discovered_distance, choosen_prev)

                # Attempt to find the nearest exterior to start vertex
                if shortest_discovered_distance < nearest_vertex_distance:
                    nearest_vertex_distance = shortest_discovered_distance
                    nearest_vertex = exterior
            
            interiors.append(nearest_vertex)

            if len(interiors) == max_interior_vertices:
                break


    def build_path(self, vertex):
        if vertex == '-':
            return []
        
        return self.build_path(self.vertex_labels[vertex]['prev']) + [vertex]


import pprint

graph = {'A': {'B': 5, 'C': 6, 'G': 17},
         'B': {'A': 3, 'C': 4, 'H': 7},
         'C': {'F': 6, 'H': 11},
         'F': {'A': 11, 'C': 7, 'G': 9, 'H': 4},
         'G': {'H': 5},
         'H': {'A': 11, 'F': 9, 'G': 4}}

dijkstra = Dijkstra(graph, start_vertex='C')

# Run the algorithm
dijkstra.dijkstra()

# Print new labels assigned to each vertex (distance from start point, last point through which we reached the vertex)
pprint.pprint(dijkstra.vertex_labels)

# Build and print shortest path from start vertex to each vertex
for vertex in dijkstra.vertices:
    print('C ->', vertex + ':', dijkstra.build_path(vertex))

# Output:
#
#  {'A': {'distance': 17, 'prev': 'F'},
#   'B': {'distance': 22, 'prev': 'A'},
#   'C': {'distance': 0, 'prev': '-'},
#   'F': {'distance': 6, 'prev': 'C'},
#   'G': {'distance': 14, 'prev': 'H'},
#   'H': {'distance': 10, 'prev': 'F'}}
#
#  C -> A: ['C', 'F', 'A']
#  C -> B: ['C', 'F', 'A', 'B']
#  C -> C: ['C']
#  C -> F: ['C', 'F']
#  C -> G: ['C', 'F', 'H', 'G']
#  C -> H: ['C', 'F', 'H']


import matplotlib.pyplot as plt

# Define the positions of the vertices on the plot
positions = {'A': (0, 1), 'B': (1, 2), 'C': (0, 0), 'F': (2, 2), 'G': (3, 1), 'H': (2, 0)}

# Create a new plot
fig, ax = plt.subplots()

# Draw the edges of the graph
for vertex1, edges in graph.items():
    for vertex2, weight in edges.items():
        ax.plot([positions[vertex1][0], positions[vertex2][0]], [positions[vertex1][1], positions[vertex2][1]], color='gray', linewidth=1)

# Draw the vertices of the graph
for vertex, pos in positions.items():
    ax.plot(pos[0], pos[1], 'o', color='white', linewidth=1, markersize=10)
    ax.text(pos[0], pos[1], vertex, ha='center', va='center')

# Draw the shortest path from the start vertex to each vertex
for vertex in dijkstra.vertices:
    path = dijkstra.build_path(vertex)
    if path:
        for i in range(len(path) - 1):
            ax.plot([positions[path[i]][0], positions[path[i+1]][0]], [positions[path[i]][1], positions[path[i+1]][1]], color='red', linewidth=2)

# Set the axis limits and remove the ticks
ax.set_xlim([-1, 4])
ax.set_ylim([-1, 3])
ax.set_xticks([])
ax.set_yticks([])

# Show the plot
plt.show()
