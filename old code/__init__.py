import numpy as np
from running import blocks, tick, initiate, square, solid_blocks

board = solid_blocks()


background, screen = initiate()
shape = blocks()
tick(board, shape, background, screen)