

`questions, concerns, comments -> email or google spaces chat (jg7955@nyu.edu)`

# Hidden Tunnel Game Implementation

`important note please read`

The default server-sided tunnel validity checker is set to ignore invalid paths and return True or False.
I set it this way because exceptions are annoying.
But during the competition, I will use another checker, also provided, which will raise an exception if the tunnel pathing is invalid.
The two checkers are identical other than the fact that one raises exceptions while the other does not. 

see server.py line 50 for the actual calls to the validity check functions and you'll see what I mean.

`Logistics`

Grid is an n by n, where the x-coordinates and y-coordinates range from 0 to n-1 inclusive, or, [0, n-1].
An intersection is a point on the grid. (x, y) is an intersection.

The Detector can place probes at intersections (x, y) and will recieve an update in the next phase regarding whether there are edges of the tunnel at the intersections probed.

An edge is two points on the grid. In general, (x1, y1, x2, y2) is a directed edge from (x1, y1) to (x2, y2)

After the last phase, an additional phase numbered 'p+1' will ask the Detector to return their guess for the path of the tunnel

`Visualization`

The server prints a basic ascii visual. The grid is printed along with the tunnel path being represented by the character 'e'. Probes are represented by 'P' and the guess path made by the detector is represented by 'G'. These symbols can be adjusted in "ascii_visual.py" lines 10-15.

`how to run`

with default python clients:

1. python server.py 'n' 'p' 'k' '(optional port number)'
2. python client_tunnel.py '(optional port number)'
3. python client_detector.py '(optional port number)'

if you use your own client, see below for setup

`how to implement solution`

If you want to use the default python clients, implement:
tunneler() in client_tunnel.py and
detect() in client_detector.py

---------------------------------------------------------

If you want to use your own client:

The server expects two separate connections coming in one by one, as in,
once the tunneler connects and sends the tunnel info, the tunneler is disconnected,
and the server then waits for a new connection from the detector side. 

The tunneler client should connect to the server, which is currently hosted locally, and then send an encoded tunnel string to the server.
The tunnel string should be of the form "x1 y1 x2 y2 x3 y3 ..." where each point (x1, y1) represents a point along the tunnel path. The points should be properly ordererd such that "x1 y1 x2 y2 ..." means that the path goes from point (x1, y1) to point (x2, y2) and so on.
e.g. "0 0 1 0 1 1" means a path starting from (0, 0), going to (1, 0), and ending at (1, 1).
Make sure the starting point starts on the bottom horizontal line y = 0 and ends on the top horizontal line y = n-1.

The detector client should connect to the server, which is currently awaiting a second connection after having initialized the tunnel, and send probes strings in each phase and lastly a path guess. Basic server logic: send game info, then recieve detector output; loop. The server will always send at each phase an encoded string of the form "n p k phase x1 y1 x2 y2 ..." where n is the grid size, p is the total number of phases, k is the max tunnel length, phase is the current phase number ranging 1 to p+1, and conditional x1 y1 x2 y2. The tailing "x1 y1 x2 y2 ..." represents the edges probed by the previous phase, and it is a conditional tailing because at phase 1 you have yet to probe anything, and then the overall string would be "n k p phase". In the case that the probes sent out in the previous phase do not find any edges, you will again recieve just "n p k phase". Otherwise, the tail of the string "n p k phase x1 y1 x2 y2 ..." will represent the edges found by the probes from the previous phase, where each grouping of 4 integers "x1 y1 x2 y2" represents one edge. The edge "x1 y1 x2 y2" represents a directed edge along the tunnel from point (x1, y1) to (x2, y2). Therefore, the order matters a lot.
e.g. "10 4 3 14" represents grid size 10, total number of phases 4, current phase number 3, max tunnel length 14, and no edges found in the previous phase.
e.g. "10 4 3 14 0 0 1 0 4 4 4 5" represents grid size 10, total number of phases 4, current phase number 3, max tunnel length 14, a directed edge from point (0, 0) to (1, 0), and another directed edge from point (4, 4) to (4, 5)

At phase number 'p+1', the detector should send an encoded string 'path' to the server representing the guessed path.
This path should be of the same format as that sent out by tunneler.

for further questions or clarification, contact me

`inputs and scoring mechanism`

Specified at competition:

`n` -> grid size (max value 20)
`p` -> number of phases (max value 5)
`k` -> max length of tunnel path (max value 50)

Your score is the number of probes used as the Detector.
Each player will play once as the Tunneler and once as the Detector,
the player with the lower score as the detector wins the game.

You can use as many probes as you'd like. less the better.


# Word for word description from heuristics website

There is a grid of size n by n, where n will be given the day of the competition. One player, called T for tunneler, has placed a tunnel from the bottom, beginning anywhere along the horizontal line marked Start in the south, and ending anywhere along the horizontal side End in the north. The tunnel follows the path of the roads somehow but may wind around. It is also a simple path (no dead ends and no loops along the way). Further, at any intersection, there cannot be more than two streets having parts of the tunnel underneath that intersection.

The second player, called D for detector, wants to probe a minimum number of times and yet be able to find the exact route of the tunnel.

Suppose a probe reports whether a tunnel ran under an intersection or not and which street(s) (up to two streets) next to the intersection the tunnel runs under. Thus, it is a directional probe.

The tunnel is at most k blocks (a parameter I will give on the day of the competition) long and begins at Start and ends at End.

The game will be played in p phases (another parameter given at the day of the competition). In each phase, D will place some number of probes at intersections and will recive their reports. By the end of the last phase, D must guess the tunnel.

The score of D is the number of probes D used assuming D found the path. If D does not find the path, then the score is infinity. D's goal is to get as low a score as possible.

Each competition will consist of two games where each team plays the role of T once and D once. Whichever team receives the lowest score as D wins.

Given n (the grid is n by n), p (the number of phases), and k (the length of the path which must be at least n-1), (i) draw the grid, (ii) distribute n, p, k to both players, (iii) receive the edges of the tunnel from T, (iv) display the tunnel to the viewers. Then the architect will give interact with D to get the probes for each phase, display the answers and provide them to D, and get D's guess as to the tunnel path after all p phases. The architect will then calculate D's score. In each game, each of T and D have two minutes to play. Thus, a full competition should take 8 minutes or less (especially because T will normally play quite fast). This is the architecture for Dig That on the game website.

# --------------------------------------------------#
