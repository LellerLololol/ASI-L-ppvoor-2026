import sys
 
import pygame
from pygame.locals import *
 
pygame.init()
 
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
  points = [(-50, -50), (50, -50), (50, 50), (-50, 50)]
  pygame.draw.polygon(screen, (0, 255, 0), points, width=0)


  pygame.display.flip()
  fpsClock.tick(fps)a
