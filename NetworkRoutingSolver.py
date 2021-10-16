#!/usr/bin/python3


from CS312Graph import *
import time

distance_dictionary = {}
previous_dictionary = {}

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

    def decrease_key(self, node):
        pass


# Class that implements a priority queue as a heap
class HeapQueue:
    def __init__(self):
        self.pointer_dictionary = {}
        self.node_array = []

    def bubble_up(self, node):
        self.node_array.append(node)
        index = self.node_array.index(node)
        p = (index // 2)
        while index != 0 and distance_dictionary[self.node_array[p].node_id] > distance_dictionary[node.node_id]:
            # Put parent node where child was
            self.node_array[index] = self.node_array[p]
            # Update pointer dictionary here, too
            self.pointer_dictionary[self.node_array[p].node_id] = index
            index = p
            p = (index // 2)

        # Put child node where parent was
        self.node_array[index] = node
        self.pointer_dictionary[node.node_id] = index

    def sift_down(self, item, i):
        # Add last element to root position
        self.node_array[i] = item

        # Delete the last element
        self.node_array.pop()

        c = self.min_child(i)
        while c != -1 and distance_dictionary[self.node_array[c].node_id] < distance_dictionary[item.node_id]:
            self.node_array[i] = self.node_array[c]
            self.node_array[c] = item
            i = c
            c = self.min_child(i)

    def min_child(self, i):
        # Node has no children
        if (2 * i) >= len(self.node_array) - 1:
            return -1
        else:
            # If node has one child
            if (2 * i) + 2 >= len(self.node_array):
                return (2 * i) + 1

            # If node has two children, return the index of the child node that has the smallest distance/key
            else:
                if distance_dictionary[self.node_array[(2*i)+1].node_id] < distance_dictionary[self.node_array[(2*i)+2].node_id]:
                    return (2 * i) + 1
                else:
                    return (2 * i) + 2

    def insert(self, node):
        self.bubble_up(node)

    def make_queue(self, nodes):
        # Initialize the pointer_dictionary, and insert to binary_heap_array
        for i in range(len(nodes)):
            self.insert(nodes[i])
            self.pointer_dictionary[nodes[i].node_id] = self.node_array.index(nodes[i])

    def delete_min(self, node_id):
        if len(self.node_array) == 0:
            return None
        else:
            x = self.node_array[0]
            self.sift_down(self.node_array[len(self.node_array) - 1], 0)
            return x

    def another_bubble_up(self, node, index):
        p = -(-index // 2) - 1
        while index != 0 and distance_dictionary[self.node_array[p].node_id] > distance_dictionary[node.node_id]:
            # Put parent node where child was
            self.node_array[index] = self.node_array[p]
            # Update pointer dictionary here, too
            self.pointer_dictionary[self.node_array[p].node_id] = index
            index = p
            p = (index // 2)

        # Put child node where parent was
        self.node_array[index] = node
        self.pointer_dictionary[node.node_id] = index

    def decrease_key(self, node):
        if node in self.node_array:
            self.another_bubble_up(node, self.node_array.index(node))

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
        print(self.global_previous_dictionary)
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
        edges_left = len(node_id_in_order) - 1
        counter = 0
        while edges_left > 0:
            # Find index
            index_counter = 0
            for i in range(len(node.neighbors)):
                if node.neighbors[i].dest.node_id == node_id_in_order[counter + 1]:
                    index_counter = i

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
            queue = HeapQueue()
        else:
            queue = ArrayQueue()

        # Array holds all nodes in the graph
        nodes = self.network.nodes

        # Algorithm Setup
        for i in range(len(nodes)):
            distance_dictionary[nodes[i].node_id] = float('inf')
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
                    queue.decrease_key(u.neighbors[i].dest)

        self.global_distance_dictionary = distance_dictionary
        self.global_previous_dictionary = previous_dictionary

        t1 = time.time()
        # TODO: RUN DIJKSTRA'S TO DETERMINE SHORTEST PATHS.
        #       ALSO, STORE THE RESULTS FOR THE SUBSEQUENT
        #       CALL TO getShortestPath(dest_index)
        t2 = time.time()
        return (t2-t1)

