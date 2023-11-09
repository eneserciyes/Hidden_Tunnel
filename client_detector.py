import socket
import sys
from typing import Set, Tuple

host = "127.0.0.1"
port = 4000

class detector():
    def __init__(self, n, p, k) -> None:
        self.n = n # grid size - grid is n by n, indices range [0, n-1]
        self.p = p # number of phases range [1, p] inclusive
        self.k = k # max length of tunnel
        self.edges_found_so_far: Set[Tuple[int, int, int, int]] = set()

    def detect(self, edges_found, phase_number):
        '''
        Given:
        (edges_found -> list of edges discovered from the previous phase)
        note that if this is the first phase, edges_found is the empty list [] since you have yet to probe anything.
        an edge is an integer tuple of the form (x1, y1, x2, y2) indicating a directed edge from point (x1, y1) -> (x2, y2) on the grid.
        e.g. an edge (0, 1, 1, 1) means that the tunnel path has an edge going from (0, 1) to (1, 1).
        In other words, (0, 1, 1, 1) is not the same as (1, 1, 0, 1) because the order of the coordinates determines the direction of the edge.

        (phase_number -> a counter indicating which phase you are on, phase_number = 1 for the first phase)
        
        Return:
        (str -> string of the form "x1 y1 x2 y2 x3 y3 x4 y4 ..." where each pair (x, y) is an intersection you would like to probe)
        e.g. str -> "1 1 2 2" means that you are probing two intersections with x, y coordinates (1, 1) and (2, 2)

        If after last phase, then return:
        (str -> string of the form "x1 y1 x2 y2 x3 y3 ..." where (x1, y1) -> (x2, y2) is a directed edge along the path, same format as the output of tunneler)
        
        
        Note:
        if you did not find any edges given the probes from the previous phase, edges_found will be an empty list [].

        the output strings probes and path should have a multiple of 2 int values in the string since we are representing x, y coordinates
        '''
        for edge in edges_found:
            self.edges_found_so_far.add(edge)

        if phase_number == 1: # first phase
            probes = ""
            for i in range(n):
                for j in range(n):
                    probes += "{} {} ".format(i, j)
        else:
            probes = "none"

        if phase_number == self.p + 1: # additional phase after the last phase should return your guess of the tunnel path
            print("edges found so far: ", self.edges_found_so_far)

            start_points = []
            end_points = []
            for edge in self.edges_found_so_far:
                start_points.append((edge[0], edge[1]))
                end_points.append((edge[2], edge[3]))
                
            
            for point in start_points:
                if point not in end_points:
                    start = point
                    break


            for point in end_points:
                if point not in start_points:
                    end = point
                    break
            
            print("start:", start, "end:", end)

            # trace path
            prev_point = start
            path = "{} {}".format(prev_point[0], prev_point[1])
            while prev_point != end:
                for edge in self.edges_found_so_far:
                    if edge[0:2] == prev_point:
                        path += " {} {}".format(edge[2], edge[3])
                        prev_point = (edge[2], edge[3])
                        break
            return path
        return probes


if __name__ == "__main__":

    if len(sys.argv) == 2:
        port = int(sys.argv[1])

    # connect with the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        info = s.recv(1024).decode()
        print("info recieved: ", info)

        # convert info string to n, p, k, phase_number
        temp = info.split(' ')
        temp = [i for i in temp if i]
        temp = list(map(int, temp))

        n = temp[0]
        p = temp[1]
        k = temp[2]
        #print(f"n: {n}, p: {p}, k: {k}")
        phase_number = temp[3]
        player_D = detector(n, p, k)
        probes = player_D.detect([], phase_number)
        s.sendall(probes.encode())

        # loop for the remaining phases after the first phase
        while phase_number <= p:
            info = s.recv(1024).decode()
            print("info recieved: ", info)
            # convert info string to n, p, k, phase_number, and edges_found
            temp = info.split(' ')
            temp = [i for i in temp if i]
            temp = list(map(int, temp))

            phase_number = temp[3]
            edges_found = []
            for i in range(1, len(temp) // 4):
                edges_found.append((temp[i*4], temp[i*4 + 1], temp[i*4 + 2], temp[i*4 + 3]))
            probes = player_D.detect(edges_found, phase_number)
            s.sendall(probes.encode())
