
def visualize(n, tunnel, probes, guess):

    # prepare the empty content
    rows = n
    cols = n
    content = [["."]*cols for _ in range(rows)]

    # assign values at coordinates as needed (based on your grid)
    grid = [(i[0], i[1], 'e') for i in tunnel]
    for (y,x,c) in grid: content[x][y] = c
    other_grid = [(i[0], i[1], 'P') for i in probes]
    for (y,x,c) in other_grid: content[x][y] = c
    x234x = [(i[0], i[1], 'G') for i in guess]
    for (y,x,c) in x234x: content[x][y] = c

    # build frame
    width       = len(str(max(rows,cols)-1))
    contentLine = "# | values |"

    dashes      = "-".join("-"*width for _ in range(cols))
    frameLine   = contentLine.replace("values",dashes)
    frameLine   = frameLine.replace("#"," "*width)
    frameLine   = frameLine.replace("| ","+-").replace(" |","-+")

    # print grid
    print(frameLine)
    for i,row in enumerate(reversed(content),1):
        values = " ".join(f"{v:{width}s}" for v in row)
        line   = contentLine.replace("values",values)
        line   = line.replace("#",f"{rows-i:{width}d}")
        print(line)
    print(frameLine)

    # x-axis numbers
    numLine = contentLine.replace("|"," ")
    numLine = numLine.replace("#"," "*width)
    colNums = " ".join(f"{i:<{width}d}" for i in range(cols))
    numLine = numLine.replace("values",colNums)
    print(numLine)

if __name__ == "__main__":
    visualize(12, [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5)], [(9, 9), (8, 8), (0, 0)], [])
    visualize(12, [], [(0, 0)], [(5, 4)])