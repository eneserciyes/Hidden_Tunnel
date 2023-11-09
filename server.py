import socket
import sys
from check_valid import check_valid_tunnel, no_exceptions_validity_check
from ascii_visual import visualize
import time

host = '127.0.0.1'
port = 4000

if __name__ == "__main__":
    if len(sys.argv) == 5:
        n = int(sys.argv[1])
        p = int(sys.argv[2])
        k = int(sys.argv[3])
        port = int(sys.argv[4])
    elif len(sys.argv) == 4:
        n = int(sys.argv[1])
        p = int(sys.argv[2])
        k = int(sys.argv[3])
    else:
        pass

    print(f"port number: {port}")

    tunnel = []

    # connect to tunneler

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("awaiting tunneler to connect..")
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()
        conn, addr = s.accept()

        with conn:
            print(f"tunneler connected by {addr}")
            inputs = str(n) + ' ' + str(p) + ' ' + str(k)
            conn.sendall(inputs.encode()) # send n, p, k to the tunnel client
            tunnel_str = conn.recv(1024).decode() # recieve the tunnel path in string form
            print("tunnel recieved: ", tunnel_str)

            # translate tunnel_str into tunnel list -> list of points on the grid that the tunnel runs through [(x1, y1), (x2, y2), ...]
            temp = tunnel_str.split(' ')
            temp = [i for i in temp if i]
            temp = list(map(int, temp))

            for i in range(len(temp) // 2):
                tunnel.append((temp[i*2], temp[i*2 + 1]))

            # script to check if tunnel is valid. Returns True if valid, else returns False
            is_valid = no_exceptions_validity_check(n, k, tunnel)
            if not is_valid:
                print("tunnel not valid, continuing...")
            # script to check if tunnel is valid, below will be uncommented during competition and will raise exception on invalid paths
            #check_valid_tunnel(n, k, tunnel)

            print("tunnel established: ", tunnel_str)
            visualize(n, tunnel, [], [])

    # connect to detector

    number_of_probes_used = 0
    path_guess = []
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("awaiting detector to connect..")
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()
        conn, addr = s.accept()

        with conn:
            edges_found = []
            
            # for p phases, get the probes and return the probed information
            for phase in range(1, p+1):
                print(f"phase: {phase}")
                send_str = str(n) + ' ' + str(p) + ' ' + str(k) + ' ' + str(phase)
                for edge in edges_found:
                    send_str = send_str + ' ' + str(edge[0]) + ' ' + str(edge[1]) + ' ' + str(edge[2]) + ' ' + str(edge[3])
                conn.sendall(send_str.encode())
                edges_found = [] # refresh edges_found for the next phase
                probes_str = conn.recv(1024).decode()
                if probes_str == 'none':
                    visualize(n, tunnel, [], [])
                    time.sleep(2)
                    continue
                print("probing: ", probes_str)
                
                # convert probes_str into list of points
                probes = []
                temp = probes_str.split(' ')
                temp = [i for i in temp if i]
                temp = list(map(int, temp))

                for i in range(len(temp) // 2):
                    probes.append((temp[i*2], temp[i*2 + 1]))
                visualize(n, tunnel, probes, [])
                time.sleep(2)
                number_of_probes_used += len(probes)

                # update edges_found
                for i in probes:
                    if i in tunnel:
                        index = tunnel.index(i)
                        if index == 0:
                            edges_found.append((tunnel[index][0], tunnel[index][1], tunnel[index+1][0], tunnel[index+1][1]))
                        elif index == len(tunnel) - 1:
                            edges_found.append((tunnel[index-1][0], tunnel[index-1][1], tunnel[index][0], tunnel[index][1]))
                        else:
                            edges_found.append((tunnel[index][0], tunnel[index][1], tunnel[index+1][0], tunnel[index+1][1]))
                            edges_found.append((tunnel[index-1][0], tunnel[index-1][1], tunnel[index][0], tunnel[index][1]))

            # after p phases, get the path guess from the detector
            send_str = str(n) + ' ' + str(p) + ' ' + str(k) + ' ' + str(p+1)
            for edge in edges_found:
                send_str = send_str + ' ' + str(edge[0]) + ' ' + str(edge[1]) + ' ' + str(edge[2]) + ' ' + str(edge[3])
            conn.sendall(send_str.encode())
            path_guess_str = conn.recv(1024).decode()
            print("path guess: ", path_guess_str)
            print("actual tunnel:")
            visualize(n, tunnel, [], [])
            time.sleep(1.2)

            # convert path guess str into list
            temp = path_guess_str.split(' ')
            temp = [i for i in temp if i]
            temp = list(map(int, temp))

            for i in range(len(temp) // 2):
                path_guess.append((temp[i*2], temp[i*2 + 1]))
            print("your guess:")
            visualize(n, [], [], path_guess)


        # Check path_guess and see if it matches tunnel path
        correct = True
        if len(tunnel) != len(path_guess):
            correct = False
            print(f"path guessed incorrectly. tunnel length: {len(tunnel)}. guessed path length: {len(path_guess)}")
        else:
            # since the pathing is expected to be a simple path, each point along the two paths should be the same point
            for i in range(len(tunnel)):
                if tunnel[i] != path_guess[i]:
                    correct = False
                    print(f"path guessed incorrectly. points at {tunnel[i]} and {path_guess[i]} do not match")
        if correct:
            print("tunnel path guessed correctly")
            print(f"number of probes used: {number_of_probes_used}")
        else:
            print("tunnel path guessed incorrectly")
            print(f"number of probes used: {number_of_probes_used}")