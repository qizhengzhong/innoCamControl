from typing import List, Dict
#import networkx as nx
#from networkx.algorithms.shortest_paths.weighted import dijkstra_path, dijkstra_path_length
#from repast.simphony.engine.environment import RunEnvironment

from multiAgent.sharedInformation import ProductState, PhysicalProperty, ResourceEvent
#from intelligentProduct import ProductAgent
from multiAgent.helper.Graph import *

from multiAgent.Buffer.BufferAgent import *
from multiAgent.Buffer.Buffer import *
from multiAgent.Buffer.BufferLLC import *

class ResourceAgentHelper:

    def teamQuery(self, desiredProperty: PhysicalProperty,
                  bidPartState: ProductState, maxTimeAllowed: int,
                  existingBid, existingBidTime: int, 
                  resourceAgent,
                  neighbors: List, tableNeighborNode,
                  RAcapabilities,
                  weightTransformer):
        # Copy graphs to not mess with pointers
        updatedCapabilities = RAcapabilities#.copy() # need to update based on current schedule
        bid = existingBid.copy()
        searchGraph = existingBid.copy()

        # Update events in capabilities based on current schedule and create new full graph (capabilities + bid)
        for edge in updatedCapabilities.edges:
            # Find the edge and update it based on current schedule
            bidOffset = resourceAgent.getSchedule().getNextFreeTime(existingBidTime, edge.getEventTime()) - existingBidTime
            edge.setWeight(edge.getEventTime() + bidOffset)

            # Add to entire graph
            searchGraph.addEdge(edge, edge.getParent(), edge.getChild())

        shortestPathGetter = DijkstraShortestPath(searchGraph,weightTransformer)
        
        # Check if a node in the capabilities graph satisfies a desired property
        flag = False
        desiredVertex = None
        for vertex in updatedCapabilities.vertices:
            if desiredProperty in vertex.getPhysicalProperties():
                flag = True
                desiredVertex = vertex[0]
                break

        #schedule = RunEnvironment.getInstance().getCurrentSchedule()
        #currentTime = schedule.getTickCount()

        # If a vertex satisfied a desired property

        print('flag',flag)
        if flag:
            shortestPathCandidateList = shortestPathGetter.getPath(bidPartState, desiredVertex)
            bidTime = existingBidTime
            for path in shortestPathCandidateList:
                bidTime = bidTime + path.getEventTime()
                bid.addEdge(path, path.getParent(), path.getChild())
                bidPartState = path.getChild()
            
            if bidTime < currentTime + maxTimeAllowed:
                productAgent.submitBid(bid)
        else:

            print('neighbors',neighbors)
            for neighbor in neighbors:

                print('neighbor',neighbor)

                neighborNode = tableNeighborNode.get(neighbor)
                shortestPathCandidateList = shortestPathGetter.getPath(bidPartState, neighborNode)
                
                if shortestPathCandidateList.isEmpty() and bid.getEdgeCount() == 0:
                    selfEdge = ResourceEvent(resourceAgent, neighborNode, neighborNode, "Hold", 0)
                    bid.addEdge(selfEdge, selfEdge.getParent(), selfEdge.getChild())
                    neighbor.teamQuery(productAgent, desiredProperty, bidPartState, maxTimeAllowed, bid, existingBidTime)
                elif not bid.getEdges().containsAll(shortestPathCandidateList):
                    bidTime = existingBidTime
                    for path in shortestPathCandidateList:
                        bidTime = bidTime + path.getEventTime()
                        bid.addEdge(path, path.getParent(), path.getChild())
                    
                    newBidPartState = shortestPathCandidateList.get(shortestPathCandidateList.size()-1).getChild()
                    
                    if bidTime < currentTime + maxTimeAllowed and bidTime >= existingBidTime:
                        neighbor.teamQuery(productAgent, desiredProperty, newBidPartState, maxTimeAllowed, bid, bidTime)

        
        self.clearGraph(updatedCapabilities)
        updatedCapabilities = None
        self.clearGraph(bid)
        bid = None
        self.clearGraph(searchGraph)
        searchGraph = None

    def copyGraph(self, oldgraph):
        graph = DirectedSparseGraph()
        for e in oldgraph.edges():
            new_edge = e.copy()
            graph.addEdge(new_edge[0], new_edge[1], **new_edge.attr_dict)
        return graph

    def clearGraph(self, graph):
        graph.clear()