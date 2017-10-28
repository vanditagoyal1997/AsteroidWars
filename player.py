'''Class representing the Player'''

import pygame, sys, time
from pygame.locals import *
import random
import math
import time
from spritesheet import SpriteStripAnim
from vector2d import Vector_2D


class Player:
    def __init__(self, position, name):
        self.position = position
        self.name = name
        self.size = 100
        self.sprite = SpriteStripAnim('game_images/astronaut.png', (0,128,128,128), 4, 1, True, 5) #handles the sprite animation
        self.direction = True #True here means facing left. False means facing right
        self.mask = None
        self.ammunition = 10
        self.dead = False
        self.score = 0
        self.sprite.iter()

    def draw(self, windowSurface): #whenever called, this iterates through the sprite to the next image and blits it on the Surface
        image = self.sprite.next().convert()
        image.set_colorkey((0,0,0))# to make background transparent
        image = pygame.transform.scale(image,(self.size,self.size))
        image = pygame.transform.flip(image, self.direction, False)
        self.mask = pygame.mask.from_surface(image)
        windowSurface.unlock()
        windowSurface.blit(image, ((self.position.x),(self.position.y)))
        windowSurface.lock()

    def update_position(self,pos): #Updates position to position given. Also decides direction based on the x parameter of the position
        if pos[0] > self.position.x:
            self.direction = False
        else:
            self.direction = True
        self.position.x = abs(pos[0])
        self.position.y = abs(pos[1])

    def collide(self,asteroids,dtime): #uses the image masks of both the player image and the asteroid image to detect collision
        if self.mask == None:
            return
        for asteroid in asteroids:
            offset_x = int(asteroid.position.x - self.position.x)
            offset_y = int(asteroid.position.y - self.position.y)
            if asteroid.mask == None: # just a basic check
                continue
            if self.mask.overlap_area(asteroid.mask,(offset_x,offset_y))>=10:
                return True
        return False

    def shoot(self): #shoots in the direction of the player
        self.ammunition -= 1
        if self.ammunition >= 0:
            return Bullet(Vector_2D(self.position.x, self.position.y + self.size/2), self.direction)
        else:
            return None

    def die(self): #Whenever the player collides with an asteroid, it changes the sprite to an explosion sprite so that instead of an astronaut, an explosion is shown
        self.dead = True
        self.sprite = SpriteStripAnim('game_images/explosion_strip16.png', (0,0,96,96), 16, 1, True, 5) #Changes sprite to explosion strip to show an explosion
        self.sprite.iter()

    def update_score(self): #adds to the player's score
        self.score += 10


class Bullet:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction
        self.speed = 10000 #Speed of the bullet is pre defined
        self.size = 16
        self.sprite = SpriteStripAnim('game_images/ball_sprite_2.png', (0,0,self.size,self.size), 34, 1, True, 5)
        self.sprite.iter()
        self.mask = None

    def update_position(self,dtime): #According to the direction, updates the position of the bullet
        if self.direction:
            self.position.x -= self.speed*dtime
        else:
            self.position.x += self.speed*dtime
        if int(self.position.x) not in range(0,1024):
            return False
        else:
            return True

    def draw(self, windowSurface): #draws each frame of the bullet sprite
        image = self.sprite.next().convert()
        image.set_colorkey((0,0,0))
        self.mask = pygame.mask.from_surface(image)
        windowSurface.unlock()
        windowSurface.blit(image, ((self.position.x),(self.position.y)))
        windowSurface.lock()

    def collide(self, asteroid): #Uses its own mask and asteroid's mask to detect collision
        if self.mask == None:
            return False
        else:
            offset_x = int(asteroid.position.x - self.position.x)
            offset_y = int(asteroid.position.y - self.position.y)
            if self.mask.overlap_area(asteroid.mask,(offset_x,offset_y))>=10:
                return True
            else:
                return False






