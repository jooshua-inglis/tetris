import time
import logging
import random
import os
import pprint
import pygame
from shapes import *
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s = %(levelname)s - %(message)s')

LEFT = -1
RIGHT = 1


class Block(pygame.sprite.Sprite):
    image_names = (
        'red.bmp',
        'yellow.bmp',
        'purple.bmp',
        'orange.bmp',
        'green.bmp',
        'blue.bmp',
        'grey.bmp',
        'black.bmp'
    )
    images = tuple()

    def __init__(self, x, y, shape):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.rect = pygame.Rect(93 + 24 * self.x, 37 + 24 * self.y, 101, 101)
        self.image = Block.images[shape]

    @classmethod
    def load_images(cls):
        cls.images = tuple(map(load_image, cls.image_names))

    def update(self):
        self.rect = pygame.Rect(93 + 24 * self.x, 37 + 24 * self.y, 101, 101)


class Shape:
    def __init__(self, shape_id=None, orientation=0, level=0, horizontal=4):
        self.orientation = orientation
        self.level = level
        self.horizontal = horizontal
        if shape_id is None:
            self.shape_id = random.randint(0, 5)
        else:
            self.shape_id = shape_id
        self.layout = list(self.make_live_blocks(self.shape_id, orientation, level, horizontal))

    @staticmethod
    def make_live_blocks(shape_id=None, orientation=0, level=0, horizontal=4):
        shape = (types0, types1, types2, types3, types4, types5)[shape_id]
        for i in shape[orientation]:
            yield Block(i[0] + horizontal, i[1] + level, shape_id)

    def _rotated_layout(self):
        return Shape(
            shape_id=self.shape_id,
            orientation=(self.orientation + 1) % 4,
            level=self.level,
            horizontal=self.horizontal
        )

    def rotate(self, solid_blocks):
        go = True
        temp_layout = self._rotated_layout()

        for temp_block in temp_layout:
            if temp_block.x < 0 or temp_block.x > 9 or self.adjacent_block_check(solid_blocks):
                go = False
        if go:
            self.layout = temp_layout.layout
            self.orientation = temp_layout.orientation

    def down_one(self):
        self.level += 1
        for i in self.layout:
            i.y += 1

    def move_horizontal(self, direction: int):
        self.horizontal += direction
        for i in self.layout:
            i.x += direction

    def go_down(self, solid_blocks: list):
        while not self.vertical_checker(solid_blocks):
            self.level += 1
            for i in self.layout:
                i.y = i.y + 1

    def vertical_checker(self, solid_blocks: list):
        for i in self.layout:
            if i.y >= 19:
                return True

            for j in solid_blocks:
                if [i.x, i.y + 1] == [j.x, j.y]:
                    return True
        return False

    def check_left(self, solid_blocks: list):
        for i in self.layout:
            if i.x <= 0:
                return True

            for j in solid_blocks:
                if [i.x - 1, i.y] == [j.x, j.y]:
                    return True
        return False

    def check_right(self, solid_blocks):
        for i in self.layout:
            if i.x >= 9:
                return True

            for j in solid_blocks:
                if [i.x + 1, i.y] == [j.x, j.y]:
                    return True
        return False

    def adjacent_block_check(self, solid_blocks):
        for temp_block in self.layout:
            for s_block in solid_blocks:
                if (temp_block.x, temp_block.y) == (s_block.x, s_block.y):
                    return True
        return False

    def __repr__(self):
        return self.layout

    def __iter__(self):
        for i in self.layout:
            yield i


def load_image(name, init=False):
    full_name = os.path.join('./resources', name)
    try:
        image = pygame.image.load(full_name)
        if init:
            pygame.display.set_mode(image.get_rect().size).blit(image, (0, 0))
            pygame.display.flip()
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error as e:
        print('Cannot load image:', full_name)
        raise e
    return image


def create_row(heights, color):
    sprites = [pygame.sprite.Group(Block(i, 19 - height, 0) for i in range(10)) for height in heights]
    for i in sprites:
        i.update()
    return sprites


def flash(heights):
    w_sprites = create_row(heights, 1)
    b_sprites = create_row(heights, 0)

    def _flash(sprites):
        for sprite in sprites:
            sprite.draw(screen)
            pygame.display.flip()
    time.sleep(0.05)

    for i in range(2):
        _flash(b_sprites)
        _flash(w_sprites)


def full_row_checker(grid, solid_blocks):
    deleted_rows = []
    for index, row in enumerate(reversed(grid)):
        if sum(row) == 10:
            deleted_rows.append(19 - index)
            for s_block in solid_blocks.copy():
                if s_block.y == index:
                    solid_blocks.remove(s_block)
                if s_block.y < index:
                    solid_blocks.remove(s_block)
                    s_block.y += 1
                    solid_blocks.append(s_block)
    if not deleted_rows:
        return()
    flash(deleted_rows)
    deleted_rows.reverse()
    for deleted_row in deleted_rows:
        grid.remove(grid[deleted_row])
        grid.append([0]*10)


def update_grid(grid, live_blocks: Shape):
    for i in live_blocks:
        grid[19-i.y][i.x] = 1


def controls(live_blocks: Shape, solid_blocks: list):
    """
    :return: Returns whether to reset time or not
    :rtype bool
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and not live_blocks.check_left(solid_blocks):
                live_blocks.move_horizontal(LEFT)
            elif event.key == pygame.K_RIGHT and not live_blocks.check_right(solid_blocks):
                live_blocks.move_horizontal(RIGHT)
            elif event.key == pygame.K_DOWN:
                live_blocks.go_down(solid_blocks)
                return True
            elif event.key == pygame.K_UP:
                live_blocks.rotate(solid_blocks)
    return False


def collisions(grid: list, solid_blocks: list, live_blocks: Shape,):
    solid_blocks.extend(live_blocks)
    update_grid(grid, live_blocks)
    logging.debug(pprint.pformat(grid))
    live_blocks.__init__()


def display_game(sprites: pygame.sprite.Group, live_blocks: Shape, solid_blocks: list):
    sprites.empty()
    for i in live_blocks:
        sprites.add(i)
    for i in solid_blocks:
        sprites.add(i)
    sprites.update()

    screen.blit(background, (0, 0))
    sprites.draw(screen)

    pygame.display.flip()


def game():
    dif = 0.5
    pre_time = time.time()
    live_blocks = Shape()
    solid_blocks = []
    sprites = pygame.sprite.Group()
    grid = [[0]*10]*20  # Creates a 10 by 20 gird of 0s

    while True:
        if time.time() - pre_time > dif:
            if live_blocks.vertical_checker(solid_blocks):
                collisions(grid, solid_blocks, live_blocks)
                pre_time = time.time()
                continue
            else:

                pre_time = time.time() if controls(live_blocks, solid_blocks) else pre_time
                live_blocks.down_one()
        full_row_checker(grid, solid_blocks)
        display_game(sprites, live_blocks, solid_blocks)
        time.sleep(0.01666666666*2)


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Tetris")
    background = load_image('hello.bmp', True)
    screen = pygame.display.get_surface()
    pygame.display.set_icon(load_image("icon.png"))
    Block.load_images()
    print('loaded images')

    game()
