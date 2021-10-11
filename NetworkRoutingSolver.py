#!/usr/bin/python3


from CS312Graph import *
import time
import math

# Class that implements a priority queue as an array
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
                min_node = self.node_array[i]
                self.node_array.pop(i)
                return min_node
                break

    def decrease_key(self, node_id):
        pass


# Represents a node in the heap
class HeapNode:
    def __init__(self):
        pass

# Class that implements a priority queue as a heap
# See slides starting from 95/99 for implementation details
class HeapQueue:
    def __init__(self):
        pass

    def bubble_up(self, item):
        pass

    def sift_down(self, item):
        pass

    def min_child(self, item):
        pass

    def insert(self, item):
        pass

    def make_queue(self, nodes):
        pass

    def delete_min(self, node_id):
        pass

    def decrease_key(self, node_id):
        pass

class NetworkRoutingSolver:
    def __init__( self):
        global_distance_dictionary = {}
        global_previous_dictionary = {}
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

        # Use previous array to figure out path to destination node
        node_id_in_order = []
        current_node_id = self.global_previous_dictionary[self.network.nodes[destIndex].node_id]
        node_id_in_order.append(current_node_id)
        keep_going = True
        while keep_going:
            current_node_id = self.global_previous_dictionary[current_node_id]
            if current_node_id is None:
                keep_going = False
            else:
                keep_going = True
                node_id_in_order.append(current_node_id)

        node_id_in_order.reverse()

        # Add destination node to the array
        node_id_in_order.append(self.network.nodes[destIndex].node_id)

        path_edges = []
        total_length = 0
        node = self.network.nodes[self.source]
        edges_left = len(node_id_in_order) - 1 # Added - 1
        counter = 0
        while edges_left > 0:
            # Find index
            index_counter = 0
            for i in range(len(node.neighbors)):
                if node.neighbors[i].dest.node_id == node_id_in_order[counter + 1]: # Added + 1
                    index_counter = i

            # edge = node.neighbors[node.neighbors.index(node_id_in_order[counter + 1])]
            edge = node.neighbors[index_counter]
            counter += 1
            path_edges.append((edge.src.loc, edge.dest.loc, '{:.0f}'.format(edge.length)))
            total_length += edge.length
            node = edge.dest
            edges_left -= 1
        return {'cost': total_length, 'path': path_edges}

    # Finds the node with the highest priority
    def find_lowest_key(self, nodes, distance_dictionary):
        lowest_key = None
        node_id_to_go = None
        for i in range(len(nodes)):
            if i == 0:
                lowest_key = distance_dictionary[nodes[i].node_id]
                node_id_to_go = nodes[i].node_id
            else:
                if distance_dictionary[nodes[i].node_id] < lowest_key:
                    lowest_key = distance_dictionary[nodes[i].node_id]
                    node_id_to_go = nodes[i].node_id
        return node_id_to_go

    def computeShortestPaths( self, srcIndex, use_heap=False ):
        self.source = srcIndex

        queue = None
        if use_heap:
            queue = ArrayQueue()
        else:
            queue = HeapQueue()

        # Array holds all nodes in the graph
        nodes = self.network.nodes

        distance_dictionary = {}
        previous_dictionary = {}

        # Algorithm Setup
        for i in range(len(nodes)):
            distance_dictionary[nodes[i].node_id] = math.inf
            previous_dictionary[nodes[i].node_id] = None
        distance_dictionary[nodes[srcIndex].node_id] = 0

        queue.make_queue(nodes)

        while len(queue.node_array) != 0:
            u = queue.delete_min(self.find_lowest_key(queue.node_array, distance_dictionary))
            if u is None:
                continue
            for i in range(len(u.neighbors)):
                neighbor_node_id = u.neighbors[i].dest.node_id
                edge_weight_of_neighbor = u.neighbors[i].length
                if distance_dictionary[neighbor_node_id] > distance_dictionary[u.node_id] + edge_weight_of_neighbor:
                    distance_dictionary[neighbor_node_id] = distance_dictionary[u.node_id] + edge_weight_of_neighbor
                    previous_dictionary[neighbor_node_id] = u.node_id
                    queue.decrease_key(neighbor_node_id)

        self.global_distance_dictionary = distance_dictionary
        self.global_previous_dictionary = previous_dictionary

        t1 = time.time()
        # TODO: RUN DIJKSTRA'S TO DETERMINE SHORTEST PATHS.
        #       ALSO, STORE THE RESULTS FOR THE SUBSEQUENT
        #       CALL TO getShortestPath(dest_index)
        t2 = time.time()
        return (t2-t1)

