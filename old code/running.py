import numpy as np, time, logging, copy, random,    pygame, os
logging.basicConfig(level=logging.DEBUG,format =' %(asctime)s = %(levelname)s - %(message)s')

class solid_blocks(pygame.sprite.Sprite):
    def __init__(self):
        self.grid = np.array([[0]*6]*20)
        self.sprites = pygame.sprite.Group()

    def __repr__(self):
        return(self.grid)

    def __getitem__(self, key):
        self.grid[key]
    

    def solidify(self,shape):
        for sprite in shape.sprites.sprites():
            self.sprites.add(sprite)
            self.grid[sprite.coor[0],sprite.coor[1]] = 1
            
class square(pygame.sprite.Sprite):
    def __init__(self,color,coor):
        pygame.sprite.Sprite.__init__(self)
        self.coor = coor
        self.image = load_image(os.path.join('%sblock.bmp' % color))
        self.x = 93 + 24    * (coor[1])
        self.y = 37 + 24 * (coor[0])
        self.rect = pygame.Rect(self.x,self.y,101,101)

    def update(self):
        self.rect = pygame.Rect(self.x,self.y,101,101)


class blocks():

        types1 = [[[0,0],[1,0],[2,0],[3,0]],
                 [[0,0],[0,1],[0,2],[0,3]],
                 [[0,0],[1,0],[2,0],[3,0]],
                 [[0,0],[0,1],[0,2],[0,3]]]
        

        types2 = [[[0,1],[1,0],[1,1],[1,2]],
                 [[1,0],[0,1],[1,1],[2,1]],
                 [[0,0],[0,1],[0,2],[1,1]],
                 [[0,0],[0,1],[0,2],[0,3]]]

        types3 = [[[0,0],[1,0],[2,0],[2,1]],
                 [[1,0],[1,1],[1,2],[0,2]],
                 [[0,1],[1,1],[2,1],[0,0]],
                 [[0,0],[0,1],[0,2],[0,3]]]


        types4 = [[[0,1],[1,1],[2,1],[2,0]],
                 [[1,0],[1,1],[1,2],[0,2]],
                 [[0,1],[1,1],[2,1],[0,0]],
                 [[0,0],[0,1],[0,2],[1,2]]]


        def __init__(self):
            self.blockShape = random.choice([blocks.types1,blocks.types2,blocks.types3,blocks.types4])
            self.state = 0
            logging.debug('The shape list is: ' + str(self.blockShape))
            self.sprites = pygame.sprite.Group()
            for i in self.blockShape[self.state]:
                logging.debug(i)
                self.sprites.add(square('red',i))
            self.elevation = 0

        def count(self):
                self.move_down_count += 1
                if self.move_down_count == 60:
                        self.move_down_count = 0
                        self.move_down()

        def move_down(self):
            self.elevation += 1
            for i in self.sprites.sprites():
                logging.debug(i.y)
                i.y += 24
                logging.debug('Move down')
                logging.debug(i.y)
                self.sprites.update()

        def turn(self):
            self.state = (self.state + 1)%3
            self.sprites.empty()
            for i in self.blockShape[self.state]:
                logging.debug(i)
                i[0] += self.elevation
                self.sprites.add(square('red',i))
            self.sprites.update()



        def new_shape(self):
            self.blockShape = random.choice([blocks.types1,blocks.types2,blocks.types3,blocks.types4])
            logging.debug('The shape list is: ' + str(self.blockShape))
            self.state = 0
            self.elevation = 0
            self.move_down_count = 0


            

def update_board(currentBoard,currentShape,change_state = 0):
        updatedBoard = copy.copy(currentBoard)
        for i in currentShape.blockShape[currentShape.state]:
                logging.debug('individual co ord for block is: %s' % i)
                logging.debug('elevation is %s' % currentShape.elevation)
        return(updatedBoard)

def cheaker(currentBoard,currentShape):
        try :
            for i in currentShape.blockShape[currentShape.state]:
                if currentBoard.grid[i[0] + currentShape.elevation + 1,i[1]] == 1:
                            #print(update_board(currentBoard,currentShape))
                            logging.debug('collision')
                            return(False)
        except:
                logging.debug('at bottom')
                #print(update_board(currentBoard,currentShape))
                return(False)

        return(True)                

def row_cheack(currentShape):
    for index, row in enumerate(currentShape):
        if sum(row) == 1:
            currentShape[index] = 0
            for i in solid_blocks.sprites.sprites():
                if i.y == 37 + 24 * (coor[index]):
                    solid_blocks.sprites.remove(i)

def tick(currentBoard,currentShape, board, screen):
    preTime = time.time()
    while True:

#pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    currentShape.turn()
                    logging.debug('turrnig')

        screen.blit(board,(0,0))
        currentShape.sprites.draw(screen)
        currentBoard.sprites.draw(screen)
        pygame.display.flip()

        #logging.debug('pass')
        if not cheaker(currentBoard,currentShape):
            currentBoard = update_board(currentBoard,currentShape)


            currentBoard.solidify(currentShape)

            logging.debug(currentBoard.grid)
            del currentShape
            currentShape = blocks()
            continue
        if time.time() - preTime > 1:
            currentShape.move_down()
            preTime = time.time()

#graphics----------------------------------------------------------------------
def load_image(name):
    fullName = os.path.join('./resources', name)
    try:
        image = pygame.image.load(fullName)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error as e:
        print('Cannot load image:', fullName)
        raise (e)
    return(image)


def initiate():
    pygame.init()

#imports the background image
    fullName = os.path.join('./resources', 'hello.bmp')
    try:
        background = pygame.image.load(fullName)
        screen = pygame.display.set_mode(background.get_rect().size)
        if background.get_alpha() is None:
            background = background.convert()
        else:
            background = background.convert_alpha()
    except Exception as e:
        print('Cannot load background:', fullName)
        raise (SystemExit, e)

#updates the borad for the first time
    screen.blit(background, (0, 0))
    pygame.display.flip()

    return(background, screen)
    #--------------------------------------------------------------------------------------
