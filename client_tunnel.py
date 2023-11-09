import socket
import sys
import random

host = "127.0.0.1"
port = 4000

def tunneler(n, p, k):
    '''
    Given:
    (n -> grid size)
    (p -> phase count)
    (k -> max length of path, at least n-1)

    Return:
    (str -> string of the form "x1 y1 x2 y2 x3 y3 ..." where (x1, y1) -> (x2, y2) is a directed edge and (x2, y2) -> (x3, y3) is a directed edge)
    e.g. str -> "0 0 1 0 1 1" is a path starting from (0, 0) going to (1, 0) and then ending at (1, 1)

    Note:
    Since the tunnel starts on the southern horizontal line and ends on the northern horizontal line,
    make sure that the starting point is (x, 0) because y is zero at the south-most horizontal line
    and the end point is (x, n-1) because y is n-1 at the north-most horizontal line.

    Order matters. "0 0 1 0 1 1" cannot be written as "0 0 1 1 1 0", although the points along the path are the same,
    the order of the points determines the direction of the path. So, the second string means that there is a directed edge from (0, 0) to (1, 1) which is invalid.
    '''
    print('n = {}, p = {}, k = {}'.format(n, p, k))

    remaining = k

    path = []
    if n % 2 == 1: start = (n//2, 0)
    else: start = random.choice([(n//2, 0), (n//2-1, 0)])

    path.append(start)

    while remaining > 0:
        x, y = path[-1]
        if y == n-1: break
        if (n-1) - y == remaining:
            for i in range(1, remaining+1):
                path.append((x, y+i))
                remaining -= 1
        else:
            # choose next point
            if n%2 == 1:
                if remaining-3 >= (n-1) - (y+1):
                    # possible_paths_to_next_level = [((x, y+1)), ((x+1, y), (x+1, y+1), (x,y+1)), ((x-1, y), (x-1, y+1), (x,y+1))]
                    roll = random.random()
                    if roll < 0.33:
                        path.append((x, y+1))
                        remaining -= 1
                    elif roll < 0.66:
                        path.append((x+1, y))
                        path.append((x+1, y+1))
                        path.append((x, y+1))
                        remaining -= 3
                    else:
                        path.append((x-1, y))
                        path.append((x-1, y+1))
                        path.append((x, y+1))
                        remaining -= 3
                else:
                    path.append((x, y+1))
                    remaining -= 1
            else:
                if remaining-3 >= (n-1) - (y+1):
                    roll = random.random()
                    if roll < 0.1:
                        if x == n//2:
                            path.append((x+1, y))
                            path.append((x+1, y+1))
                            path.append((x, y+1))
                            remaining -= 3
                        else:
                            path.append((x-1, y))
                            path.append((x-1, y+1))
                            path.append((x, y+1))
                            remaining -= 3
                    elif roll < 0.55:
                        path.append((x, y+1))
                        remaining -= 1
                    else:
                        if x == n//2:
                            path.append((x, y+1))
                            path.append((x-1,  y+1))
                            remaining -= 2
                        else:
                            path.append((x, y+1))
                            path.append((x+1, y+1))
                            remaining -= 2
                elif remaining-2 >= (n-1) - (y+1):
                    roll = random.random()
                    if roll < 0.5:
                        if x == n//2:
                            path.append((x, y+1))
                            path.append((x-1,  y+1))
                            remaining -= 2
                        else:
                            path.append((x, y+1))
                            path.append((x+1, y+1))
                            remaining -= 2
                    else:
                        path.append((x, y+1))
                        remaining -= 1
                else:
                    path.append((x, y+1))
                    remaining -= 1

                

    path_str = ""
    for i in range(len(path)):
        path_str += str(path[i][0]) + " " + str(path[i][1]) + " "

    print(path_str)
    return path_str

if __name__ == "__main__":

    if len(sys.argv) == 2:
        port = int(sys.argv[1])

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        inputs_raw = s.recv(1024)
        inputs_str = str(inputs_raw, 'utf-8')
        vals = inputs_str.split(' ')
        vals = [i for i in vals if i]
        vals = list(map(int, vals))

        n = vals[0]
        p = vals[1]
        k = vals[2]
        print(f"inputs recieved: n = {n}, p = {p}, k = {k}")
        tunnel = tunneler(n, p, k)
        print(f"tunnel created: {tunnel}")
        s.sendall(tunnel.encode())
