import pygame
import math

import switch as switch

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
player_imgs = []
for i in range(1, 5):
    player_imgs.append(pygame.transform.scale(pygame.image.load('Asset/Pacman/Pacman' + str(i) + '.png'), (45, 45)))
    print(len(player_imgs))

player_x = 450
player_y = 450
player_speed = 5
moving = False
direction = 0
direction_command = 0
counter = 0
turn_allowed = [False, False, False, False]

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
            if lv[i][j] == 6:
                pygame.draw.arc(screen, color, [j*num2 + 0.5 * num2, (i + 0.5)*num1, num2, num1], Pi/2, Pi, 3)
            if lv[i][j] == 7:
                pygame.draw.arc(screen, color, [(j*num2 + 0.5*num2) , (i - 0.4)*num1, num2, num1], Pi, 3*Pi/2, 3)
            if lv[i][j] == 8:
                pygame.draw.arc(screen, color, [j*num2 - 0.4 * num2 - 2, (i - 0.5)*num1, num2, num1], 3*Pi/2, 2*Pi, 3)
            if lv[i][j] == 9:
                pygame.draw.line(screen, 'white', (j*num2, (i + 0.5)*num1), (j*num2 + num2, i*num1 + 0.5*num1), 3)

def draw_player():
    if direction == 0:
        screen.blit(player_imgs[counter//4], (player_x, player_y))
    elif direction == 1:
        screen.blit(pygame.transform.flip(player_imgs[counter//4], True, False), (player_x, player_y))
    elif direction == 2:
        screen.blit(pygame.transform.rotate(player_imgs[counter // 4], 90), (player_x, player_y))
    elif direction == 3:
        screen.blit(pygame.transform.rotate(player_imgs[counter//4], -90), (player_x, player_y))

def check_position(center_x, center_y):
    turn = [False, False, False, False]
    num1 = (Height - 50)//32
    num2 = Width//30
    num3 = 15
    if center_x // 30 < 29:
        if direction == 0:
            if level[center_y//num1][(center_x - num3)//num2] < 3:
                turn[1] = True
        if direction == 1:
            if level[center_y//num1][(center_x + num3)//num2] < 3:
                turn[0] = True
        if direction == 2:
            if level[(center_y + num3)//num1][(center_x)//num2] < 3:
                turn[3] = True
        if direction == 3:
            if level[(center_y - num3)//num1][(center_x)//num2] < 3:
                turn[2] = True
        if direction == 2 or direction == 3:
            if 12 <= center_x % num2 <= 18:
                if level[(center_y + num3)//num1][center_x//num2] < 3:
                    turn[3] = True
                if level[(center_y - num3)//num1][center_x//num2] < 3:
                    turn[2] = True
            if 12 <= center_y % num1 <= 18:
                if level[(center_y)//num1][(center_x - num2)//num2] < 3:
                    turn[1] = True
                if level[(center_y)//num1][(center_x + num2)//num2] < 3:
                    turn[0] = True
        if direction == 0 or direction == 1:
            if 12 <= center_x % num2 <= 18:
                if level[(center_y + num1)//num1][center_x//num2] < 3:
                    turn[3] = True
                if level[(center_y - num1)//num1][center_x//num2] < 3:
                    turn[2] = True
            if 12 <= center_y % num1 <= 18:
                if level[(center_y)//num1][(center_x - num3)//num2] < 3:
                    turn[1] = True
                if level[(center_y)//num1][(center_x + num3)//num2] < 3:
                    turn[0] = True
    else:
        turn[0] = True
        turn[1] = True

    return turn

def move_player(playr_x, playr_y):
    if direction == 0 and turn_allowed[0]:
        playr_x += player_speed
    if direction == 1 and turn_allowed[1]:
        playr_x -= player_speed
    if direction == 2 and turn_allowed[2]:
        playr_y -= player_speed
    if direction == 3 and turn_allowed[3]:
        playr_y += player_speed
    return playr_x, playr_y

while run :
    timer.tick(fps)
    screen.fill('black')
    if counter < 15:
        counter+=1
    else:
        counter = 0
    draw_board(level)
    draw_player()
    if moving:
        player_x, player_y = move_player(player_x, player_y)
    center_x = player_x + 23
    center_y = player_y + 24
    turn_allowed = check_position(center_x, center_y)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            moving = True
            if event.key == pygame.K_RIGHT:
                direction_command = 0
            if event.key == pygame.K_LEFT:
                direction_command = 1
            if event.key == pygame.K_UP:
                direction_command = 2
            if event.key == pygame.K_DOWN:
                direction_command = 3
        if event.type == pygame.KEYUP:
            moving = False
            if event.key == pygame.K_RIGHT and direction_command == 0:
                direction_command = direction
            if event.key == pygame.K_LEFT and direction_command == 1:
                direction_command = direction
                turn_allowed[1] = False
            if event.key == pygame.K_UP and direction_command == 2:
                direction_command = direction
                turn_allowed[2] = False
            if event.key == pygame.K_DOWN and direction_command == 3:
                direction_command = direction
                turn_allowed[3] = False

    if direction_command == 0 and turn_allowed[0]:
        direction =0
    if direction_command == 1 and turn_allowed[1]:
        direction = 1
    if direction_command == 2 and turn_allowed[2]:
        direction = 2
    if direction_command == 3 and turn_allowed[3]:
        direction = 3
    if player_x > 900:
        player_x = -47
    elif player_x < -50:
        player_x = 897
    pygame.display.flip()
pygame.quit()