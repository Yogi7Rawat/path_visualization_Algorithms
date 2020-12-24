import pygame
from queue import Queue


width = 800
screen = pygame.display.set_mode((width, width))
pygame.display.set_caption("Yogendra visualization Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUISE = (64, 224, 208)


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neigh = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUISE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_close(self):
        self.color = RED

    def make_open(self):
        self.color = YELLOW

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUISE 

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neigh(self, grid):
        self.neigh = []
        
        #down
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neigh.append(grid[self.row + 1][self.col])

        #up
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neigh.append(grid[self.row - 1][self.col])

        #right
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neigh.append(grid[self.row][self.col + 1]) 

        #left
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neigh.append(grid[self.row][self.col - 1])





def Draw_Path(came_from, curr, draw):

    while curr in came_from:
        curr = came_from[curr]
        curr.make_path()
        draw() 



def BFS(draw, grid, start, end):
    q = Queue()
    q.put(start)
    came_from = {}

    visited = {start}

    while not q.empty():
        current = q.get()
        if current == end:
            Draw_Path(came_from, end, draw)
            end.make_end()
            return True

        for neigh in current.neigh:
            if neigh not in visited:
                came_from[neigh] = current
                q.put(neigh)
                visited.add(neigh)
                neigh.make_open()
        draw()

    return False



def DFS(draw, grid, start, end):
    
    came_from = {};
    visited = {start}
    stack = []
    stack.append(start);
    while(len(stack)):
      current = stack[-1];
      stack.pop();
      if current==end:
        Draw_Path(came_from, end, draw)
        end.make_end()
        return True;
        
      if current not in visited:
        visited.add(current);
      
      for neigh in current.neigh:
        if neigh not in visited:
          came_from[neigh] = current;
          stack.append(neigh);
          neigh.make_open()
          
      draw();
          
    return False;

def make_grid(rows, width):
    grid = []
    gap = width // rows 
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid

def draw_grid(screen, rows, width):
    gap = width//rows 

    #drawing horizontal lines
    for i in range(rows):
        pygame.draw.line(screen, GREY, (0, i*gap), (width , i * gap))

    #drawing vertical lines
        for j in range(rows):
            pygame.draw.line(screen, GREY, (j*gap, 0), (j * gap, width))

def draw(screen, grid, rows, width):
    screen.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(screen)

    draw_grid(screen, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    x, y = pos

    row = x // gap
    col = y // gap 

    return row, col 


def main(screen, width):
    rows = 50
    grid = make_grid(rows, width)

    start = None
    end = None

    run = True
    started = False

    while(run):
        draw(screen, grid, rows, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue

            if pygame.mouse.get_pressed()[0]: #left
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, width)
                node = grid[row][col]

                if not start and node != end:
                    start = node 
                    start.make_start()
                elif not end and node != start:
                    end = node
                    end.make_end()

                elif node != end and node != start:
                    node.make_barrier()


            elif pygame.mouse.get_pressed()[2]: #right click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None 
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neigh(grid)

                    DFS(lambda: draw(screen, grid, rows, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None 
                    grid = make_grid(rows, width)

    pygame.quit()

main(screen, width)

