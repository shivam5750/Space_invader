import pygame
import random
import math
from pygame import mixer
pygame.init()      #intilizing the pygame library

# Open a window on the screen
screen_width=800
screen_height=600
screen=pygame.display.set_mode([screen_width, screen_height])

#adding title and icon to our screen
icon = pygame.image.load('space.png')
pygame.display.set_icon(icon)
pygame.display.set_caption('Space Invaders')



#creating player
playerimg = pygame.image.load('rocket.png')
playerX = 380
playerY = 470  #assigning player x, y coo-ordinate
playerX_change = 0
def player(x, y):
    screen.blit(playerimg ,(x, y))   # blitting means drawing
#displaying score
score_value = 0
font = pygame.font.Font('new.otf',64)
textX = 10
textY = 10
def show_score(x,y):
    score = font.render('score:'+ str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))
#Background image
backgroundimg = pygame.image.load('background.png')
#game over text
over_font = pygame.font.Font('new.otf', 72)

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

#Background sound
'''
You can add sound using pygame by following ways
pygame.music.load(backggroundmusic)
mixer.music.loop(-1)  -1 to make the music to be played in a loop
'''

#creating enemy
enemyimg = []
enemyX  = []
enemyY = []
enemyX_change =[]
enemyY_change =[]
no_of_enemies =6
for i in range(no_of_enemies):
    enemyimg.append(pygame.image.load('ufo.png'))
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(50, 135))  #assigning player x, y coo-ordinate
    enemyX_change.append(5)
    enemyY_change.append(40)
def enemy(x, y,i):
    screen.blit(enemyimg[i], (x, y))

#creating bullet
bulletimg = pygame.image.load('bullet.png')
bulletX =0
bulletY = 500
bulletY_change = 20
bullet_state = 'ready'
def bullet_firing(x,y):
    global bullet_state
    bullet_state = 'Fire'
    screen.blit(bulletimg,(x+16, y+10))
#checking collision
def iscollision(enemyX, enemyY, bulletX, bulletY):
    difference = math.sqrt((math.pow(enemyX-bulletX,2))+(math.pow(enemyY-bulletY,2)))
    if difference < 30:
        return True
    else:
        return False

#game loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(backgroundimg, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   #IN HERE I.E PYGAME ANYTHING WE PRESSED IS A EVENT
            running= False
        #DEFINNING THE CONTROL OF THE GAME
        if event.type == pygame.KEYDOWN:  #KEYDOWN means pressing a button and KEYUP RELEASE THE BUTTON
            if event.key == pygame.K_LEFT:
                playerX_change = -10
            elif event.key == pygame.K_RIGHT:
                playerX_change = 10
            elif event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                   bullet_sound = mixer.Sound('sf_laser_14.mp3')
                   bullet_sound.play()
                   bulletX = playerX
                   bullet_firing(bulletX, bulletY)
        elif event.type == pygame.KEYUP:
                event.key == pygame.K_LEFT and  event.key == pygame.K_RIGHT
                playerX_change = 0


    playerX += playerX_change
    #Defining the boundaries for player
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:    #taken 736 as the pixel of image is 64
        playerX=736
    #creating enemies
    for i in range(no_of_enemies):
        #game over
        if enemyY[i] > 440:
            for j in range(no_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        #Defining the boundaries for enemy and it's movement
        if enemyX[i] <=0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] > 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # detecting collision
        collision = iscollision(enemyX[i], enemyX[i], bulletX, bulletY)
        if collision:
            explosion = mixer.Sound('sf_explosion_20.mp3')
            explosion.play()
            bullet_state == 'ready'
            bulletY = 500
            score_value += 1
            print(score_value)
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 135)

        enemy(enemyX[i], enemyY[i],i)
    # movement of bullet
    if bulletY <= 0:
        bullet_state = 'ready'    #after  every firing it shoild be set again at it's launching position
        bulletY = 500
    if bullet_state == 'Fire':
        bullet_firing(bulletX, bulletY)
        bulletY -= bulletY_change
    player(playerX, playerY)
    show_score(textX,textY)
    pygame.display.update()




