import numpy as np, time, logging, copy, random, pygame, os
logging.basicConfig(level=logging.DEBUG,format =' %(asctime)s = %(levelname)s - %(message)s')


pygame.init()
class block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.rect = pygame.Rect(93 + 24 * self.x, 37 + 24 * self.y, 101, 101)
        self.image = load_image(os.path.join('redblock.bmp'))

    def update(self):
        self.rect = pygame.Rect(93 + 24 * self.x, 37 + 24 * self.y, 101, 101)

types0 =  [[[0, 0], [1, 0], [1, 1], [2, 1]],
           [[0, 1], [0, 2], [1, 0], [1, 1]],
           [[0, 0], [1, 0], [1, 1], [2, 1]],
           [[0, 1], [0, 2], [1, 0], [1, 1]]]
types1 = [[[1, 0], [0, 1], [2, 0], [1, 1]],
          [[0, 0], [0, 1], [1, 1], [1, 2]],
          [[1, 0], [0, 1], [2, 0], [1, 1]],
          [[0, 0], [0, 1], [1, 1], [1, 2]],]
types2 = [[[1, 0], [0, 1], [1, 1], [2, 1]],
          [[1, 0], [1, 1], [1, 2], [2, 1]],
          [[0, 1], [1, 1], [2, 1], [1, 2]],
          [[0, 1], [1, 0], [1, 1], [1, 2]]]
types3 = [[[1, 0], [1, 1], [1, 2], [0, 2]],
          [[0, 0], [0, 1], [1, 1], [2, 1]],
          [[0, 0], [0, 1], [0, 2], [1, 0]],
          [[0, 1], [1, 1], [2, 1], [2, 2]]]
types4 = [[[0, 0], [0, 1], [0, 2], [1, 2]],
          [[0, 1], [1, 1], [2, 1], [0, 2]],
          [[1, 0], [1, 1], [1, 2], [0, 0]],
          [[2, 0], [0, 1], [1, 1], [2, 1]]]
types5 = [[[0, 0], [0, 1], [0, 2], [0, 3]],
          [[-1, 1], [0, 1], [1, 1], [2, 1]],
          [[0, 0], [0, 1], [0, 2], [0, 3]],
          [[-1, 1], [0, 1], [1, 1], [2, 1]]]
def load_image(name, init = False):
    fullName = os.path.join('./resources', name)
    try:
        image = pygame.image.load(fullName)
        if init:
            pygame.display.set_mode(image.get_rect().size).blit(image, (0,0))
            pygame.display.flip()
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error as e:
        print('Cannot load image:', fullName)
        raise (e)
    return(image)
background = load_image('hello.bmp', True)
screen = pygame.display.get_surface()


def make_live_blocks(liveBlocks, type = 'random', orientation = 0, level = 0, horizontal = 4):
    if type == 'random':
        type = random.randint(0,5)
    shape = [types0,types1,types2,types3,types4,types5][type]
    for i in shape[orientation]:
        liveBlocks.append(block(i[0] + horizontal,i[1] + level))
    return(type, orientation)


def vertical_checker(liveBlocks,solidBlocks):
    #returns true when something is underneath
    for i in liveBlocks:
        if i.y >= 19:
            return(True)
            loggind.debug('vertical_checker')

        for j in solidBlocks:
            if [i.x,i.y + 1] == [j.x,j.y]:
                return(True)
    return (False)

def row_checker(grid):
    for i in grid:
        if sum(i) == 10:
            return(True)
    return(False)

def update_grid(grid,liveBlocks):
    for i in liveBlocks:
        grid[i.y][i.x] = 1


def game():
    dif = 0.5
    level = 0
    preTime = time.time()
    liveBlocks  = []
    solidBlocks = []
    type, orientation = make_live_blocks(liveBlocks,1,0,0)
    sprites = pygame.sprite.Group()
    def check_left():
        for i in liveBlocks:
            if i.x <= 0:
                return (True)

            for j in solidBlocks:
                if [i.x - 1, i.y] == [j.x, j.y]:
                    return (True)
        return (False)
    def check_right():
        for i in liveBlocks:
            if i.x >= 9:
                return (True)

            for j in solidBlocks:
                if [i.x + 1, i.y] == [j.x, j.y]:
                    return (True)
        return (False)
    horizontal = 4
    grid = np.array([[0] * 10] * 20)
    while True:
        #pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and not check_left():
                    horizontal -= 1
                    for i in liveBlocks:
                        i.x -= 1
                elif event.key == pygame.K_RIGHT and not check_right():
                    horizontal += 1
                    for i in liveBlocks:
                        i.x += 1
                elif event.key == pygame.K_DOWN:
                    while not vertical_checker(liveBlocks,solidBlocks):
                        level += 1
                        for i in liveBlocks:
                            i.y = i.y + 1
                        preTime = time.time() - dif

                elif event.key == pygame.K_UP:
                    liveBlocks = []
                    orientation = (orientation + 1)%4
                    print(orientation)
                    type, orientation = make_live_blocks(liveBlocks,type,orientation,level,horizontal)



        if time.time() - preTime > dif:
            if vertical_checker(liveBlocks, solidBlocks):
                solidBlocks.extend(liveBlocks)
                preTime = time.time()
                update_grid(grid, liveBlocks)
                print(grid)
                level = 0
                liveBlocks = []
                type, orientation = make_live_blocks(liveBlocks, 'random')
                horizontal = 4
                logging.debug('collisions')

                continue
            level += 1
            for i in liveBlocks:
                i.y = i.y + 1
                preTime = time.time()
                logging.debug(level)

        sprites.empty()
        for i in liveBlocks:
            sprites.add(i)
        for i in solidBlocks:
            sprites.add(i)
        sprites.update()

        screen.blit(background, (0, 0))
        sprites.draw(screen)

        pygame.display.flip()
        time.sleep(0.01666666666*2)
game()