import sys
import map
 
import pygame
from pygame.locals import *
 
pygame.init()

grid = [32, 48]

fps = 60
fpsClock = pygame.time.Clock()
 
width, height = 640, 920
screen = pygame.display.set_mode((width, height))

# Game loop.
while True:
  screen.fill((0, 0, 0))
  
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
  
  # Update.
  
  # Draw.
  boxes = map.createMap(width, height, grid)
  for b in boxes:
    pygame.draw.rect(screen, (0, 255, 0), b)


  pygame.display.flip()
  fpsClock.tick(fps)
