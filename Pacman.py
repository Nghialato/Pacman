import pygame
import math
from Board import boards
pygame.init()

Width = 900
Height = 950

screen = pygame.display.set_mode([Width, Height])

timer = pygame.time.Clock()
fps = 60
# font = pygame.font.Font('')
run = True
level = boards
color = 'blue'
Pi = math.pi

def draw_board(lv):
    num1 = ((Height - 50)//32)
    num2 = ((Width)//30)
    for i in range(len(lv)):
        for j in range(len(lv[i])):
            if lv[i][j] == 1:
                pygame.draw.circle(screen, 'white', ((j*num2 + 0.5*num2), (i + 0.5)*num1), 4)
            if lv[i][j] == 2:
                pygame.draw.circle(screen, 'white', ((j*num2 + 0.5*num2), (i + 0.5)*num1), 10)
            if lv[i][j] == 3:
                pygame.draw.line(screen, color, ((j + 0.5)*num2, i*num1), (j*num2 + 0.5*num2, i*num1 + num1), 3)
            if lv[i][j] == 4:
                pygame.draw.line(screen, color, (j*num2, (i + 0.5)*num1), (j*num2 + num2, i*num1 + 0.5*num1), 3)
            if lv[i][j] == 5:
                pygame.draw.arc(screen, color, [(j*num2 - 0.4*num2) - 2, (i + 0.5)*num1, num2, num1], 0, Pi/2, 3)
            if lv[i][j] == 9:
                pygame.draw.line(screen, 'white', (j*num2, (i + 0.5)*num1), (j*num2 + num2, i*num1 + 0.5*num1), 3)



while run :
    timer.tick(fps)
    screen.fill('black')
    draw_board(level)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.flip()
pygame.quit()