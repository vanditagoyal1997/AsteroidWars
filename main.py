import pygame, sys
from pygame.locals import *
import random
import math
import time
from spritesheet import SpriteStripAnim
from asteroid import Asteroid
from player import Player
from vector2d import Vector_2D
from savegame import SaveGame

def get_name(windowSurface): #This function blits the welcome screen and accepts the name of the player to maintain the top score
    name = ""
    font = pygame.font.Font(None, 50)
    while True:
        for evt in pygame.event.get():
            if evt.type == KEYDOWN:
                if evt.unicode.isalpha():
                    name += evt.unicode
                elif evt.key == K_BACKSPACE:
                    name = name[:-1]
                elif evt.key == K_RETURN:
                    return name
            elif evt.type == QUIT:
                return
        windowSurface.fill((0, 0, 0))
        block = font.render(name, True, (255, 255, 255))
        rect = block.get_rect()
        rect.center = windowSurface.get_rect().center
        title = font.render('DEFEND THE EARTH', True, (255, 255, 255))
        name_enter = font.render('ENTER YOUR NAME', True, (255, 255 ,255))
        windowSurface.blit(block, rect)
        windowSurface.blit(title, (350, 50))
        windowSurface.blit(name_enter, (350,200))
        pygame.display.flip()

def initialize_game(): #This function initializes the game
    global asteroids, bullets, player, asteroid_size_upgrade, player_reload_time, asteroid_add_time, save_game, myfont, reload_time_set, top_score

    asteroids = []
    bullets = []
    for i in range(0,10):
        asteroids.append(Asteroid(Vector_2D(random.randint(60,640),random.randint(40,640)),Vector_2D(random.randint(0,1000),random.randint(0,1000))))
    player = Player(Vector_2D(40,40), player_name)
    pygame.mouse.set_pos([40,40])
    asteroid_size_upgrade = time.time()
    player_reload_time = time.time()
    asteroid_add_time = time.time()
    save_game = SaveGame(player_name)
    top_score = 0
    if save_game.load():
        top_score = int(save_game.get_properties()['Top Score'])
    pygame.mouse.set_visible(False)
    pygame.mouse.set_pos([40,40])
    myfont = pygame.font.SysFont("impact", 50)
    reload_time_set = False


#Set Up GLOBAL Constants

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 728

# set up pygame
pygame.init()

# set up the window
windowSurface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Defend The Earth')


# Initialize clock and frames per second

clock = pygame.time.Clock()
fps = 60

#Initializing game variables that are treated as global variables
asteroids = []
bullets = []
player = None
save_game = None
myfont = None
asteroid_size_upgrade = time.time()
player_reload_time = time.time()
asteroid_add_time = time.time()
reload_time_set = False
top_score = 0
game_properties = {}

#Getting the name of the player
player_name = get_name(windowSurface)

initialize_game()
#Running Game Loop
while True:
    dtime = clock.tick(fps)/10000.0 #This defines delta time within which all objects are updated

    windowSurface.blit(pygame.image.load('game_images/background_2.jpg'),[0,0])

    #This loop handles the drawing of all the asteroids and maintains a list of them
    for asteroid in asteroids:
        asteroid.collide(asteroids,dtime)
        asteroid.update_position(dtime)
        exists = True # decides to draw
        for bullet in bullets:
            if bullet.collide(asteroid): #If a bullet collides with an asteroid, the bullet and asteroid both disappear
                bullets.remove(bullet)
                exists = False # decides not to draw
        if exists:
            asteroid.draw(windowSurface)
        else:
            asteroids.remove(asteroid)
            player.update_score()
        if int(asteroid.position.x) not in range(0,1024) or int(asteroid.position.y) not in range(0,728): #If an asteroids goes out of bounds, it is considered as a destroyed asteroid
            asteroids.remove(asteroid)

    #This loop handles the drawing of the bullets
    for bullet in bullets:
        if not bullet.update_position(dtime):
            bullets.remove(bullet)
        bullet.draw(windowSurface)

    #This increases the size of the asteroids at fixed intervals of time to increase difficulty
    if time.time() - asteroid_size_upgrade >= 10:
        for asteroid in asteroids:
            if asteroid.size <= 100:
               asteroid.size+=15
        asteroid_size_upgrade = time.time()

    #This reloads the player's ammunition 10 seconds after it got empty
    if player.ammunition <= 0 and reload_time_set == False: # reload_time_set was created so that the reloading only occurs after the bullets have finished.
        player_reload_time = time.time()
        reload_time_set = True
    if time.time() - player_reload_time >=10 and reload_time_set == True:
        player.ammunition = 10
        reload_time_set = False

    #This replenishes the number of asteroids and ensures that any asteroid that is created doesn't get created directly over the player
    if len(asteroids) <= 20 and time.time() - asteroid_add_time >=float(len(asteroids)/10.0):
        forbidden_x = (int(player.position.x), int(player.position.x + player.size))
        forbidden_y = (int(player.position.y), int(player.position.y + player.size))
        while True:
            position_x = random.randint(0,1024)
            if position_x not in range(forbidden_x[0], forbidden_x[1]):
                break
        while True:
            position_y = random.randint(0,728)
            if position_y not in range(forbidden_y[0], forbidden_y[1]):
                break

        asteroid = (Asteroid(Vector_2D(position_x,position_y),Vector_2D(random.randint(0,1000),random.randint(0,1000))))
        asteroids.append(asteroid)
        asteroid_add_time = time.time()
        asteroid.draw(windowSurface)

    #This handles the collision of the player with an asteroid and the explosion. Upon mouse click, the game is restarted
    if player.collide(asteroids,dtime):
        continue_game = False
        frames_done = 0
        player.die()
        if player.score >= top_score:
            save_game.save({'Top Score':player.score})
        while frames_done <= 512: #Takes 512 frames to complete the explosion sequence. player.draw() executes the exlplosion sequence as the player sprite is replaced by the explosion sprite in the Player Class code
            player.draw(windowSurface)
            pygame.display.flip()
            frames_done+=1
        if frames_done >= 512:
            continue_game = False
            while not continue_game:
                #Shows the Game Over Dialog and initializes the game whenever the user clicks
                windowSurface.unlock()
                game_over_label = 'Game Over. Your Score is: ' + str(player.score)
                windowSurface.blit(myfont.render((game_over_label), 1, (255,255,255)),(10,50))
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == MOUSEBUTTONDOWN:
                        initialize_game()
                        continue_game = True
                    if event.type == QUIT or event.type == KEYDOWN:
                        pygame.quit()
                        sys.exit()

    player.draw(windowSurface)
# run the game loop
    windowSurface.unlock()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEMOTION: #Whenever the mouse is moved, the player follows the mouse motion
            player.update_position(event.pos)
        if event.type == MOUSEBUTTONDOWN: #Whenever the mouse button is clicked, the player shoots in the direction he is facing.
            bullet = player.shoot()
            if bullet != None:
                bullets.append(bullet)
    #Handles all the information on the screen
    ammo_label = 'Ammo : ' + str(player.ammunition if player.ammunition >0 else 'Reloading')
    windowSurface.blit(myfont.render((ammo_label), 1, (255,255,255)),(500,50))
    score_label = 'Score : ' + str(player.score)
    windowSurface.blit(myfont.render((score_label), 1, (255,255,255)),(10,50))
    top_score_label = 'Top Score : ' + str(top_score)
    windowSurface.blit(myfont.render((top_score_label), 1, (255,255,255)),(10,80))
    pygame.display.flip()



