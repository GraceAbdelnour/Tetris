from boards import Board
from pieces import Piece, color

import pygame
pygame.init()

board = Board()
piece = Piece()

width, height = Piece().scale*Board().cols, Piece().scale*(Board().rows-2)
screen = pygame.display.set_mode((width, height))

def display(board, piece):
  screen.fill([20, 20, 20])
  
  # Creates fluid grid from piece info and solid board
  grid = list(board.grid)
  overlay = board.overlay(piece.x, piece.y)
  for i in range(len(overlay)):
    if piece.matrix[i]==1:
      grid[overlay[i]] = piece.type
      
  # Fluid console print
  '''
  print()
  for i in range(Board().rows):
    print(board.grid[Board().cols*i:Board().cols*i+Board().cols], i)
  print()
  for i in range(Board().rows):
    print(grid[Board().cols*i:Board().cols*i+Board().cols], i)
  '''

  # Creates pygame grid
  row_cont = 0
  for row in [(grid[i:i+Board().cols]) for i in range(2*Board().cols, (Board().rows+1)*Board().cols, Board().cols)]:
    if row.count(0)!=Board().cols:
      col_cont = 0
      for loc in row:
        if loc != 0:
          pygame.draw.rect(screen, color[loc], (col_cont*Piece().scale,row_cont*Piece().scale,Piece().scale,Piece().scale))
        col_cont += 1
    row_cont += 1

  pygame.display.update()

timer_event = pygame.USEREVENT
pygame.time.set_timer(timer_event, 500)
while True:
  for event in pygame.event.get():
    keys=pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and not board.collision(piece, piece.x-1, piece.y):
      piece.x -= 1
    if keys[pygame.K_RIGHT] and not board.collision(piece, piece.x+1, piece.y):
      piece.x += 1
    if keys[pygame.K_UP]:
      piece.rotate()
      overlay = board.overlay(piece.x, piece.y)
      for i in range(len(overlay)):
        if board.grid[overlay[i]]!=0:
          if 0 >= i <= 7:
            if not board.collision(piece, piece.x, piece.y+1):
              piece.y += 1
            else:
              board.solidify(piece)
              piece = Piece()
          elif i % 4 == 0 and board.grid[overlay[i + 1]] == 0:
            piece.x += 1
          elif i % 2 == 0 and board.grid[overlay[i - 1]] == 0:
            piece.x -= 1
          elif i % 3 == 0 and board.grid[overlay[i - 2]] == 0:
            piece.x -= 2
          else:
            piece.y -= 1
            board.solidify(piece)
          break
    if keys[pygame.K_DOWN] or event.type == timer_event:
      if not board.collision(piece, piece.x, piece.y+1):
        piece.y += 1
      else:
        board.solidify(piece)
        piece = Piece()
    board.line_clear()
    display(board, piece)
print('End')