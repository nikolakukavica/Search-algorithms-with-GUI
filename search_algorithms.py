import pygame
import searches.algorithms as algorithms
import numpy as np

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
LIGHT_GREEN = (0,200,0)
RED = (255, 0, 0)
LIGHT_RED = (200, 0,0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (0,0,200)
YELLOW = (255,255,0)
LIGHT_YELLOW = (200,200,0)
CYAN = (0,255,255)
LIGHT_CYAN = (0,200,200)
GRAY = (127,127,127)
LIGHT_GRAY = (200,200,200)
MAGNETA=(255,0,255)
LIGHT_MAGNETA=(127,0,127)

WIDTH = 785
HEIGHT = 585
WINDOW_SIZE = [WIDTH+200, HEIGHT+100]
MARGIN = 5

ROWS = 7
COLUMNS = 7

CELL_WIDTH = int((WIDTH-((ROWS+1)*MARGIN))/ROWS)
CELL_HEIGHT = int((HEIGHT-((COLUMNS+1)*MARGIN))/COLUMNS)

states = {
    "POCETAK" : {"light_color" : LIGHT_GREEN, "color": GREEN, "value":1},
    "DZID" : {"light_color" : LIGHT_RED, "color": RED, "value":2},
    "KRAJ" : {"light_color" : LIGHT_BLUE, "color": BLUE, "value":3},
    "VATRA" : {"light_color" : LIGHT_YELLOW, "color": YELLOW, "value":4},
    "EMPTY": {"color":WHITE, "light_color":WHITE, "value":0}
}

grid=np.zeros((ROWS,COLUMNS))
weights=np.random.randint(0,4,(ROWS,COLUMNS))
grid_copy = grid.copy()

fire = np.array([[1,2,1],[2,3,2],[1,2,1]])

pygame.init()

screen = pygame.display.set_mode(WINDOW_SIZE)

pygame.display.set_caption("Search Algorithms")

done = False

clock = pygame.time.Clock()

# Print out the statements
print('======== Given Matrix ========')
print(grid)
print('======== Given Weights ========')
print(weights)

putanja = None
state = "POCETAK"
algorithm = "DFS"

def text_objects(text, font, color = BLACK):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def action(arg):
    global grid
    global grid_copy
    global putanja
    global state
    global algorithm
    if arg in states.keys():
        state = arg
    elif arg=="START":
        start = next(zip(*np.where(grid == 1)))
        end = next(zip(*np.where(grid == 3)))
        if start[0] != -1 and start[1] != -1:
            if algorithm == "DFS":
                path, current, found = algorithms.DFS(grid, start, 3)
            elif algorithm == "BFS":
                path, current, found = algorithms.BFS(grid, start, 3)
            elif algorithm == "DIJKSTRA":
                path, current, found = algorithms.Dijkstra(grid, weights, start, 3)
            elif algorithm == "ASTAR":
                path, current, found = algorithms.a_star(grid, weights, start, end, 3)
            if found:
                putanja = algorithms.reconstruct_path(path, start, current)
            else:
                print ("No path found!")
        else:
            print ("No start found!")
    elif arg=="RESET":
        grid = grid_copy.copy()
        putanja = None
    else:
        algorithm = arg

def button_function(msg,x,y,w,h,ic,ac, actiony = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))
        if click[0] == 1:
            pos = pygame.mouse.get_pos()
            column = int(pos[0] // (CELL_WIDTH + MARGIN))
            row = int(pos[1] // (CELL_HEIGHT + MARGIN))
            if actiony == None and grid[row][column]==0:
                if state in ["POCETAK","KRAJ"]:
                    grid[grid == states[state]['value']] = states['EMPTY']['value']
                grid[row][column] = states[state]['value']
                if state == "VATRA":
                    global weights
                    fire_temporary = np.zeros((weights.shape[0] + 2, weights.shape[1] + 2), np.int)
                    fire_temporary[1:-1, 1:-1] += weights
                    fire_temporary[row:row + 3, column:column + 3] += fire
                    weights = fire_temporary[1:-1, 1:-1].copy()
            if actiony!=None:
                action(actiony)
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))

    smallText = pygame.font.Font("freesansbold.ttf", 20)
    textSurf, textRect = text_objects(msg, smallText)
    if actiony==None:
        textRect.center = ((x + 9 * w / 10), (y + (2 * h / 10)))
    else:
        textRect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(textSurf, textRect)

while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill(BLACK)

    for row in range(ROWS):
        for column in range(COLUMNS):
            color = states['EMPTY']['color']

            light_color = states[state]["light_color"]

            for key, value in states.items():
                if grid[row][column]==value['value']:
                    light_color = value["light_color"]
                    color = value["color"]

            button_function(str(weights[row][column]), (MARGIN + CELL_WIDTH) * column + MARGIN,
                       (MARGIN + CELL_HEIGHT) * row + MARGIN, CELL_WIDTH, CELL_HEIGHT, color, light_color)


    button_function("POCETAK", WIDTH + 50, 50, 100, 50, GREEN, LIGHT_GREEN, "POCETAK")
    button_function("DZID", WIDTH + 50, 150, 100, 50, RED, LIGHT_RED,"DZID")
    button_function("KRAJ", WIDTH + 50, 250, 100, 50, BLUE, LIGHT_BLUE,"KRAJ")
    button_function("VATRA", WIDTH + 50, 350, 100, 50, YELLOW, LIGHT_YELLOW, "VATRA")

    button_function("START", WIDTH + 50, 450, 100, 50, CYAN, LIGHT_CYAN, "START")
    button_function("RESET", WIDTH + 50, 550, 100, 50, YELLOW, LIGHT_YELLOW, "RESET")

    button_function("DFS", 50, 600, 50, 50, MAGNETA, LIGHT_MAGNETA, "DFS")
    button_function("BFS", 150, 600, 50, 50, MAGNETA, LIGHT_MAGNETA, "BFS")
    button_function("DIJKSTRA", 250, 600, 120, 50, MAGNETA, LIGHT_MAGNETA, "DIJKSTRA")
    button_function("A*", 420, 600, 50, 50, MAGNETA, LIGHT_MAGNETA, "A*")

    smallText = pygame.font.Font("freesansbold.ttf", 20)
    textSurf, textRect = text_objects("STATE:", smallText,WHITE)
    screen.blit(textSurf, (WIDTH + 50,625))
    textSurf, textRect = text_objects(state, smallText,WHITE)
    screen.blit(textSurf, (WIDTH + 50, 650))
    textSurf, textRect = text_objects("ALGORITHM:", smallText, WHITE)
    screen.blit(textSurf, (WIDTH - 150, 625))
    textSurf, textRect = text_objects(algorithm, smallText, WHITE)
    screen.blit(textSurf, (WIDTH - 150, 650))

    if putanja is not None:
        font = pygame.font.SysFont("comicsansms", 36)
        for i in range(len(putanja)):
            text = font.render(str(i), True, (255, 0, 255))
            screen.blit(text, (
            ((MARGIN + CELL_WIDTH) * putanja[i][1] + MARGIN + CELL_WIDTH//3), ((MARGIN + CELL_HEIGHT) * putanja[i][0])+ MARGIN))

    clock.tick(60)

    pygame.display.flip()

pygame.quit()