import pygame
import random
import math
from pygame import mixer
#Initialize the pygame
pygame.init()

#create the screen
screen=pygame.display.set_mode((800,600))

#Background image
background=pygame.image.load('background.png')

#Title and icon
pygame.display.set_caption("Space Invader")
icon=pygame.image.load('icon.png')
pygame.display.set_icon(icon)

#Player spaceship
player_img=pygame.image.load('player.png')
player_x=370
player_y=480
player_x_change=0

#Enemy alien
alien_img=[]
alien_x=[]
alien_y=[]
alien_x_change=[]
alien_y_change=[]
num_of_aliens=6
for i in range(num_of_aliens):
    alien_img.append(pygame.image.load('alien.png'))
    alien_x.append(random.randint(0,736))
    alien_y.append(random.randint(50,150))
    alien_x_change.append(3)
    alien_y_change.append(40)

#Bullet
bullet_img=pygame.image.load('bullet.png')
bullet_x=0
bullet_y=480
bullet_y_change=7
bullet_state="ready"

#Score
score=0
font=pygame.font.Font('JetBrainsMono-Medium.ttf',32)
textx,texty=10,10

#Game over text
over_font=pygame.font.Font('JetBrainsMono-Medium.ttf',64)


def show_score(x,y):
    s=font.render("Score : "+ str(score),True,(135,206,235))
    screen.blit(s, (x,y))

def player(x,y):
    screen.blit(player_img,(x,y))

def alien(x,y,i):
    screen.blit(alien_img[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bullet_img,(x+16,y+10))

def collision(alienx,alieny,bulletx,bullety):
    distance=math.sqrt((math.pow(alienx-bulletx,2) + math.pow(alieny-bullety,2)))
    if distance<27:
        return True
    return False

def game_over():
    over=over_font.render("Game Over",True,(255,120,20))
    screen.blit(over, (200,250))


#Game window loop
running=True
while running:

    screen.fill((150,50,250))  
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

        #Keystroke event
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                player_x_change= -5
            if event.key==pygame.K_RIGHT:  
                player_x_change= 5
            if event.key==pygame.K_SPACE:  
                if bullet_state=="ready":
                    bullet_sound=mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bullet_x=player_x
                    fire_bullet(bullet_x,bullet_y)

        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                player_x_change=0
    player_x+=player_x_change       

    #Boundary of spaceship
    if player_x<=0:
        player_x=0
    if player_x>=736:
        player_x=736     

      

    #Enemy movement
    for i in range(num_of_aliens):

        #Game over
        if alien_y[i]>440:
            for j in range(num_of_aliens):
                alien_y[j]=2000
            game_over()
            break
        alien_x[i]+=alien_x_change[i]     

        if alien_x[i]<=0:
            alien_x_change[i]= 3
            alien_y[i]+=alien_y_change[i]
        elif alien_x[i]>=736:
            alien_x_change[i]= -3   
            alien_y[i]+=alien_y_change[i]


        #Collision
        c=collision(alien_x[i],alien_y[i],bullet_x,bullet_y)
        if c:
            explosion_sound=mixer.Sound('explosion.wav')
            explosion_sound.play()
            bullet_y=480
            bullet_state="ready"
            score+=1
            #Enemy respawn
            alien_x[i]=random.randint(0,736)
            alien_y[i]=random.randint(50,150)

        alien(alien_x[i],alien_y[i],i)

    #Bullet mechanics
    if bullet_y<=0:
        bullet_y=480
        bullet_state="ready"
    if bullet_state=='fire':
        fire_bullet(bullet_x,bullet_y)
        bullet_y-=bullet_y_change 

    player(player_x,player_y)
    show_score(textx,texty)
    pygame.display.update()
