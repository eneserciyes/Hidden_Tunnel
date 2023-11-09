import socket
import sys

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

    if k >= 2*n:
        prev_point = (0, 0)
        path = '{} {}'.format(prev_point[0], prev_point[1])
        for i in range(2*(n-1)):
            if i % 2 == 0:
                path += ' {} {}'.format(prev_point[0], prev_point[1] + 1)
                prev_point = (prev_point[0], prev_point[1] + 1)
            else:
                path += ' {} {}'.format(prev_point[0] + 1, prev_point[1])
                prev_point = (prev_point[0] + 1, prev_point[1])
    print(path)
    print("Len path:", len(path))
    return path

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
