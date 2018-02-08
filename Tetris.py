import numpy as np, time, logging, copy, random, pygame, os, pprint
logging.basicConfig(level=logging.DEBUG,format =' %(asctime)s = %(levelname)s - %(message)s')

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
pygame.init()
pygame.display.set_caption("tetris")
background = load_image('hello.bmp', True)
screen = pygame.display.get_surface()
images = [load_image('red.bmp'),load_image('yellow.bmp'),load_image('purple.bmp'),load_image('orange.bmp'),load_image('green.bmp'),load_image('blue.bmp'),load_image('white.bmp')]
pygame.display.set_icon(load_image("icon.png"))
print('loaded images')

class block(pygame.sprite.Sprite):

    def __init__(self, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.rect = pygame.Rect(93 + 24 * self.x, 37 + 24 * self.y, 101, 101)
        self.image = images[type]

    def update(self):
        self.rect = pygame.Rect(93 + 24 * self.x, 37 + 24 * self.y, 101, 101)

types0 = [[[0, 0], [1, 0], [1, 1], [2, 1]],
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





def make_live_blocks(liveBlocks, type = 'random', orientation = 0, level = 0, horizontal = 4):
    if type == 'random':
        type = random.randint(0,5)
    shape = [types0,types1,types2,types3,types4,types5][type]
    for i in shape[orientation]:
        liveBlocks.append(block(i[0] + horizontal,i[1] + level, type))
    return(type, orientation)


def vertical_checker(liveBlocks,solidBlocks):
    #returns true when something is underneath
    for i in liveBlocks:
        if i.y >= 19:
            return(True)

        for j in solidBlocks:
            if [i.x,i.y + 1] == [j.x,j.y]:
                return(True)
    return (False)

def flash(heights):
    bSprites = [pygame.sprite.Group(block(i,19 - height, 0) for i in range(10)) for height in heights]
    wSprites = [pygame.sprite.Group(block(i,19 - height, 1) for i in range(10)) for height in heights]
    for i in bSprites:
        i.update()
    for i in wSprites:
        i.update()

    for i in range(2):
        for i in bSprites:
            i.draw(screen)
            pygame.display.flip()
        time.sleep(0.05)
        for i in wSprites:
            i.draw(screen)
            pygame.display.flip()
        time.sleep(0.05)


def row_checker(grid, solidBlocks):
    deletedRows = []
    for index, row in enumerate(grid):
        if sum(row) == 10:
            deletedRows.append(index)
            for sBlock in solidBlocks.copy():
                if sBlock.y == 19 - index:
                    solidBlocks.remove(sBlock)
                if sBlock.y < 19 - index:
                    solidBlocks.remove(sBlock)
                    sBlock.y += 1
                    solidBlocks.append(sBlock)

    if deletedRows == []:
        return()
    flash(deletedRows)
    deletedRows.reverse()
    for deletedRow in deletedRows:
        grid.remove(grid[deletedRow])
        grid.append([0]*10)

def update_grid(grid,liveBlocks):
    for i in liveBlocks:
        grid[19-i.y][i.x] = 1

def game():
    dif = 0.5
    level = 0
    preTime = time.time()
    liveBlocks  = []
    solidBlocks = []
    type, orientation = make_live_blocks(liveBlocks,'random',0,0)
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
    grid = [[0]*10 for i in range(20)]
    def make_bottom_rows(x):
        liveBlocks.clear()
        for j in range(x):
            for i in range(10):
                liveBlocks.append(block(i,x - 19,0))


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
                    go = True
                    tempBlocks = liveBlocks.copy()
                    make_live_blocks(tempBlocks,type,(orientation + 1)%4,level,horizontal)

                    def adjacent_block_check():
                        for tBlock in tempBlocks:
                            for sBlock in solidBlocks:
                                if [tBlock.x, tBlock.y] == [sBlock.x, sBlock.y]:
                                    return (True)
                        return (False)

                    for tBlock in tempBlocks:
                        if tBlock.x < 0 or tBlock.x > 9 or adjacent_block_check():
                            go = False
                    if go:
                        liveBlocks = []
                        orientation = (orientation + 1)%4
                        type, orientation = make_live_blocks(liveBlocks,type,orientation,level,horizontal)

        if time.time() - preTime > dif:
            if vertical_checker(liveBlocks, solidBlocks):
                solidBlocks.extend(liveBlocks)
                preTime = time.time()
                update_grid(grid, liveBlocks)
                logging.debug(pprint.pformat(grid))
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
        row_checker(grid, solidBlocks)
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
