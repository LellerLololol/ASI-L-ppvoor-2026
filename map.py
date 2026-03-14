import pygame

grid = [32, 48]

def createBox(x, y, width, height):
	return pygame.Rect(x, y, width, height)

def createMap(width, height, grid):
	boxWidth = width / grid[0]
	boxHeight = height / grid[1]

	boxes = []
	for i in range(grid[0]):
		boxes.append(createBox(boxWidth * i, 0, boxWidth, boxHeight))
	for i in range(grid[0]):
		boxes.append(createBox(boxWidth * i, height - boxHeight, boxWidth, boxHeight))
	for i in range(grid[1]):
		boxes.append(createBox(0, boxHeight * i, boxWidth, boxHeight))
	for i in range(grid[1]):
		boxes.append(createBox(width - boxWidth, boxHeight * i, boxWidth, boxHeight))

	#box = createBox(320, 460, boxWidth, boxHeight)
	return boxes