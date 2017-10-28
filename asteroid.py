'''This class represents the Asteroids in the Game'''

import pygame, sys, time
from pygame.locals import *
import random
import math
import time
from spritesheet import SpriteStripAnim
from vector2d import Vector_2D
class Asteroid:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity
        self.size = 100
        self.sprite = SpriteStripAnim('game_images/asteroid1.png', (0,0,72,72), 5, 1, True, 5)
        self.mask = None
        self.sprite.iter()

    def draw(self, windowSurface): #Draws the next frame in the sprite of the asteroid
        #pygame.draw.circle(windowSurface, self.color, (int(self.position.x),int(self.position.y)), self.size)
        image = self.sprite.next().convert()
        image.set_colorkey((0,0,0))
        image = pygame.transform.scale(image,(self.size,self.size))
        self.mask = pygame.mask.from_surface(image)
        windowSurface.unlock()
        windowSurface.blit(image, ((self.position.x),(self.position.y)))
        windowSurface.lock()

    def update_position(self,dtime): #Updates the position of the asteroid in dtime according to the velocity
        self.reflect(1024,728,dtime)
        self.position.x += self.velocity.x*dtime
        self.position.y += self.velocity.y*dtime


    def collide(self,asteroids,dtime): #Checks for collision between two asteroids by checking the distance between the centers of the asteroids.
        for asteroid in asteroids:
            if asteroid.position.x != self.position.x or asteroid.position.y != self.position.y:
                if math.sqrt(((self.position.x+self.velocity.x*dtime) - (asteroid.position.x+asteroid.velocity.x*dtime))**2 + ((self.position.y+self.velocity.y*dtime) - (asteroid.position.y+self.velocity.y*dtime))**2) <=(self.size + asteroid.size)/2:
                    temp = self.velocity    #The velocity is exchanged here between the two bodies. Angle of collision is not considered
                    self.velocity = asteroid.velocity
                    asteroid.velocity = temp
                    self.position.x += self.velocity.x*dtime
                    self.position.y += self.velocity.y*dtime
                    asteroid.position.x += asteroid.velocity.x*dtime
                    asteroid.position.y += asteroid.velocity.y*dtime

    def reflect(self,width,height,dtime): #Checks reflection against the screen boundaries
        if self.position.x + self.velocity.x*dtime <= 0:
            self.velocity.x = abs(self.velocity.x) #for the left boundary

        if self.position.y + self.velocity.y*dtime <= 0:
            self.velocity.y = abs(self.velocity.y)# for the top bondary

        if self.position.x + self.velocity.x*dtime >= width - self.size:
            self.velocity.x = -1*abs(self.velocity.x) # for the right boundary

        if self.position.y + self.velocity.y*dtime >=height - self.size:
            self.velocity.y = -1*abs(self.velocity.y) # for bottom boundary
