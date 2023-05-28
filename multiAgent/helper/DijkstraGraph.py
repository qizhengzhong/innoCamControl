# Python3 implementation to find the
# shortest path in a directed
# graph from source vertex to
# the destination vertex
class Pair:
    def __init__(self, first, second):
        self.first = first
        self.second = second
infi = 1000000000;
   
# Class of the node
class Node:
   
    # Adjacency list that shows the
    # vertexNumber of child vertex
    # and the weight of the edge   
    def __init__(self, vertexNumber):       
        self.vertexNumber = vertexNumber
        self.children = []
   
    # Function to add the child for
    # the given node
    def Add_child(self, vNumber, length):   
        p = Pair(vNumber, length);
        self.children.append(p);
       
# Function to find the distance of
# the node from the given source
# vertex to the destination vertex
def dijkstraDist(g, s, path):
       
    # Stores distance of each
    # vertex from source vertex
    dist = [infi for i in range(len(g))]
   
    # bool array that shows
    # whether the vertex 'i'
    # is visited or not
    visited = [False for i in range(len(g))]
     
    for i in range(len(g)):       
        path[i] = -1
    dist[s] = 0;
    path[s] = -1;
    current = s;
   
    # Set of vertices that has
    # a parent (one or more)
    # marked as visited
    sett = set()    
    while (True):
           
        # Mark current as visited
        visited[current] = True;
        for i in range(len(g[current].children)): 
            v = g[current].children[i].first;           
            if (visited[v]):
                continue;
   
            # Inserting into the
            # visited vertex
            sett.add(v);
            alt = dist[current] + g[current].children[i].second;
   
            # Condition to check the distance
            # is correct and update it
            # if it is minimum from the previous
            # computed distance
            if (alt < dist[v]):      
                dist[v] = alt;
                path[v] = current;       
        if current in sett:           
            sett.remove(current);       
        if (len(sett) == 0):
            break;
   
        # The new current
        minDist = infi;
        index = 0;
   
        # Loop to update the distance
        # of the vertices of the graph
        for a in sett:       
            if (dist[a] < minDist):          
                minDist = dist[a];
                index = a;          
        current = index;  
    return dist;
   
# Function to print the path
# from the source vertex to
# the destination vertex
def printPath(path, i, s):
    if (i != s):
           
        # Condition to check if
        # there is no path between
        # the vertices
        if (path[i] == -1):       
            print("Path not found!!");
            return;       
        printPath(path, path[i], s);
        print(path[i] + " ");
      
# Driver Code
if __name__=='__main__':
     
    v = []
    n = 4
    s = 0;
   
    # Loop to create the nodes
    for i in range(n):
        a = Node(i);
        v.append(a);
   
    # Creating directed
    # weighted edges
    v[0].Add_child(1, 1);
    v[0].Add_child(2, 4);
    v[1].Add_child(2, 2);
    v[1].Add_child(3, 6);
    v[2].Add_child(3, 3);
    path = [0 for i in range(len(v))];
    dist = dijkstraDist(v, s, path);
   
    # Loop to print the distance of
    # every node from source vertex
    for i in range(len(dist)):
        if (dist[i] == infi):
         
            print("{0} and {1} are not " +
                              "connected".format(i, s));
            continue;       
        print("Distance of {}th vertex from source vertex {} is: {}".format(
                          i, s, dist[i]));


    import matplotlib.pyplot as plt

    # Loop through the nodes to create a list of edges
    import matplotlib.pyplot as plt
    import numpy as np

    # Assign random positions to the nodes
    node_positions = np.random.rand(len(v), 2)

    print(node_positions)

    # Draw edges
    for i in range(len(v)):
        for j in range(len(v[i].children)):
            child = v[i].children[j].first
            weight = v[i].children[j].second
            plt.plot([node_positions[i][0], node_positions[child][0]],
                     [node_positions[i][1], node_positions[child][1]],
                     'b-', alpha=0.5, linewidth=2, label=f'{weight}')

    # Draw nodes
    for i in range(len(v)):
        plt.plot(node_positions[i][0], node_positions[i][1], 'ro')
        plt.text(node_positions[i][0]+0.02, node_positions[i][1]+0.02, str(i), fontsize=12)

    # Set axis limits and title
    plt.xlim([-0.1, 1.1])
    plt.ylim([-0.1, 1.1])
    plt.title('Weighted Graph')

    # Show legend
    plt.legend()

    # Show the plot
    plt.show()