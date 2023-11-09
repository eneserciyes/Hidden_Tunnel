
def check_length(k, tunnel):
    # check length
    if len(tunnel) > k + 1:
        raise Exception("tunnel length exceeds k - the max tunnel length")

def check_indexing(n, tunnel):
    # check valid indexing, as in x and y are in the range [0, n-1]
    for i in tunnel:
        if i[0] > n-1 or i[0] < 0:
            raise Exception("invalid point: ", i, " - position not on the grid")
        if i[1] > n-1 or i[1] < 0:
            raise Exception("invalid point: ", i, " - position not on the grid")

def check_connectivity(tunnel):
    # check connectivity, from an intersection, the path can only go up, down, left, or right
    for i in range(1, len(tunnel)):
        # check if path goes up, down, left, or right by 1 unit
        if bool(abs(tunnel[i][0] - tunnel[i-1][0]) == 1) ^ bool(abs(tunnel[i][1] - tunnel[i-1][1]) == 1):
            continue
        else:
            raise Exception(f"invalid pathing from points {tunnel[i-1]} to {tunnel[i]}")
        
def check_cycle(tunnel):
    # for a simple path, if a point along the path is visited more than once, then there is a cycle. 
    visited = []
    for i in tunnel:
        if i in visited:
            raise Exception(f"cycle detected along tunnel path at {i}")
        visited.append(i)

def check_branch(tunnel):
    pass

def check_start_end(n, tunnel):
    # starting point should have y = 0
    # ending point should have y = n-1
    if tunnel[0][1] != 0:
        raise Exception(f"tunnel start point invalid: {tunnel[0]}")
    if tunnel[-1][1] != n-1:
        raise Exception(f"tunnel end point invalid: {tunnel[-1]}")
    
def check_bidirectional(tunnel):
    # an edge is bidirectional if two points along the path are the same
    for i in range(1, len(tunnel)):
        if tunnel[i] == tunnel[i-1]:
            raise Exception(f"tunnel invalid, bi-directional edge detected along path at point {tunnel[i]}")

def check_valid_tunnel(n, k, tunnel):
    '''
    check length
    check indexing
    check connectivity
    check for cycle
    check for branch -> unnecessary/redundant. if you disagree, please contact me at jg7955@nyu.edu
    check for start and end
    check bidirectional edge -> also maybe redundant since bi-directional <=> cycle

    -- inputs --
    n: grid size
    k: max path length
    tunnel: list of points(int tuple) along the path [(x1, y1), (x2, y2), (x3, y3), ...] where a directed edge exists from (x1, y1) -> (x2, y2) and from (x2, y2) -> (x3, y3)
    '''

    check_length(k, tunnel)
    check_indexing(n, tunnel)
    check_connectivity(tunnel)
    check_cycle(tunnel)
    check_start_end(n, tunnel)

def no_exceptions_validity_check(n, k, tunnel):
    '''
    does the same thing as check_valid_tunnel(), but catches the exceptions and returns True or False
    Returns True if tunnel path is valid, else return False
    '''
    try: check_length(k, tunnel) 
    except: return False
    try: check_indexing(n, tunnel)
    except: return False
    try: check_connectivity(tunnel)
    except: return False
    try: check_cycle(tunnel)
    except: return False
    try: check_start_end(n, tunnel)
    except: return False
    try: check_start_end(n, tunnel)
    except: return False
    return True

if __name__ == "__main__":
    test = [(0, 0),(1, 0), (1, 1)]
    wrong = [(0, 0), (0, 1), (1, 2)]
    wrong2 = [(0, 0), (1, 0), (0, 0)]
    #check_valid_tunnel(2, 2, test)
    #check_valid_tunnel(3, 2, wrong)
    check_length(2, test)
    check_indexing(2, test)
    check_connectivity(test)
    check_cycle(test)
    check_start_end(2, test)
    print(no_exceptions_validity_check(2, 2, test))