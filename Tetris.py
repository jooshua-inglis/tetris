import numpy as np, time, logging, copy, random, pygame, os
logging.basicConfig(level=logging.DEBUG,format =' %(asctime)s = %(levelname)s - %(message)s')

pygame.init()

class block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.level = 0
        self.x = x
        self.y = y
        self.rect = pygame.Rect(93 + 24 * self.x, 37 + 24 * self.y, 101, 101)
        self.image = load_image(os.path.join('redblock.bmp'))

    def update(self):
        self.rect = pygame.Rect(93 + 24 * self.x, 37 + 24 * (self.y + self.level), 101, 101)

#TODO update the types
types1 = [[[0, 0], [0, 1], [0, 2], [0, 3]],
          [[0, 0], [1, 0], [2, 0], [3, 0]],
          [[0, 0], [0, 1], [0, 2], [0, 3]],
          [[0, 0], [1, 0], [2, 0], [3, 0]]]
types2 = [[[1, 0], [0, 1], [1, 1], [2, 1]],
          [[0, 1], [1, 0], [1, 1], [1, 2]],
          [[0, 0], [0, 1], [0, 2], [1, 1]],
          [[0, 0], [1, 0], [2, 0], [1, 1]]]
types3 = [[[0, 0], [1, 0], [2, 0], [2, 1]],
          [[1, 0], [1, 1], [1, 2], [0, 2]],
          [[0, 1], [1, 1], [2, 1], [0, 0]],
          [[0, 0], [0, 1], [0, 2], [0, 3]]]
types4 = [[[0, 1], [1, 1], [2, 1], [2, 0]],
          [[1, 0], [1, 1], [1, 2], [0, 2]],
          [[0, 1], [1, 1], [2, 1], [0, 0]],
          [[0, 0], [0, 1], [0, 2], [1, 2]]]



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

def make_live_blocks(liveBlocks):
    for i in types1[0]:
        liveBlocks.append(block(i[0],i[1]))
    return (liveBlocks)

def vertical_checker(liveBlocks,solidBlocks):
    for i in liveBlocks:
        if i.y >= 19:
            return(True)
            loggind.debug('vertical_checker')

        for j in solidBlocks:
            if [i.x,i.y + 1] == [j.x,j.y]:
                return(True)
    return (False)

def game():
    dif = 1
    preTime = time.time()
    liveBlocks  = []
    solidBlocks = []
    make_live_blocks(liveBlocks)
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


    while True:
        #pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and not check_left():
                    for i in liveBlocks:
                        i.x -= 1
                elif event.key == pygame.K_RIGHT and not check_right():
                    for i in liveBlocks:
                        i.x += 1
                elif event.key == pygame.K_DOWN:
                    dif = 0

        if vertical_checker(liveBlocks, solidBlocks):
            solidBlocks.extend(liveBlocks)
            time.sleep(1)
            preTime = time.time()
            liveBlocks = []
            make_live_blocks(liveBlocks)
            logging.debug('collisions')
            dif = 1
            
        

        elif time.time() - preTime > dif:
            for i in liveBlocks:
                i.level += 1
                preTime = time.time()

        sprites.empty()
        for i in liveBlocks:
            sprites.add(i)
        for i in solidBlocks:
            sprites.add(i)
        sprites.update()

        screen.blit(background, (0, 0))
        sprites.draw(screen)

        pygame.display.flip()
game()
