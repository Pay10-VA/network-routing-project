#!/usr/bin/python3


from CS312Graph import *
import time


class ArrayQueue:
    def __init__(self):
        self.node_array = []

    def insert(self, item):
        self.node_array.append(item)

    def make_queue(self, nodes):
        for i in range(len(nodes)):
            self.node_array.append(nodes[i])

    def delete_min(self, node_id):
        for i in range(len(self.node_array)):
            if self.node_array[i].node_id == node_id:
                self.node_array.pop(i)
                break

    def decrease_key(self):
        pass


class NetworkRoutingSolver:
    def __init__( self):
        pass

    def initializeNetwork( self, network ):
        assert( type(network) == CS312Graph )
        self.network = network

    # Returns the path
    def getShortestPath( self, destIndex ):
        self.dest = destIndex
        # TODO: RETURN THE SHORTEST PATH FOR destIndex
        #       INSTEAD OF THE DUMMY SET OF EDGES BELOW
        #       IT'S JUST AN EXAMPLE OF THE FORMAT YOU'LL 
        #       NEED TO USE
        path_edges = []
        total_length = 0
        node = self.network.nodes[self.source]
        edges_left = 3
        while edges_left > 0:
            edge = node.neighbors[2]
            path_edges.append( (edge.src.loc, edge.dest.loc, '{:.0f}'.format(edge.length)) )
            total_length += edge.length
            node = edge.dest
            edges_left -= 1
        return {'cost':total_length, 'path':path_edges}

    def computeShortestPaths( self, srcIndex, use_heap=False ):
        self.source = srcIndex

        queue = None
        if use_heap:
            queue = ArrayQueue()
        # Dijkstra's algorithm implementation here

        my_array = self.network.nodes
        for i in range(len(my_array)):
            print(my_array[i].node_id)


        t1 = time.time()
        # TODO: RUN DIJKSTRA'S TO DETERMINE SHORTEST PATHS.
        #       ALSO, STORE THE RESULTS FOR THE SUBSEQUENT
        #       CALL TO getShortestPath(dest_index)
        t2 = time.time()
        return (t2-t1)

