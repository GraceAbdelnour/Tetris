from itertools import chain

import pygame
pygame.init()

class Board:
  rows = 18 + 3
  cols = 10
  grid = [0 for i in range(rows*cols)]

  # Returns tuple containing indexs of a 4x4 matrix around a point
  def overlay(self, x, y):
    return tuple(chain.from_iterable([[j for j in range(i+x,i+x+4) if j<self.rows*self.cols] for i in range(self.cols*(y-2)-1,self.cols*(y+2)-1, self.cols)]))

  # Clears line
  def line_clear(self):
    for row in range(0, self.rows*self.cols, self.cols):
      if self.grid[row:row+self.cols].count(0)==0:
        del self.grid[row:row+self.cols]
        for _ in range(self.cols):
          self.grid.insert(0,0)

  # Check for collision
  def collision(self, piece, x, y):
    if (y > self.rows-piece.bound['y'][0] - 1 or
        x < 0 - piece.bound['x'][0] or 
        x > self.cols - piece.bound['x'][1] - 1):
      return True
    overlay = self.overlay(x, y)
    for i in range(len(overlay)):
      if piece.matrix[i]==1 and self.grid[overlay[i]]!=0:
        return True
    return False

  def kick(self, piece):
    # WIP
    pass

  # Adds shape to solid grid
  def solidify(self, piece):
    overlay = self.overlay(piece.x, piece.y)
    for i in range(len(overlay)):
      if piece.matrix[i]==1:
        self.grid[overlay[i]] = piece.type

  # Checks if top out
  def alive(self):
    if (self.grid[0:60]).count(0)==60:
      return True
    return False