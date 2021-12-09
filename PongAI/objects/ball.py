from pygame.draw import circle
from random import choice

class Ball:

    def __init__(self,screen,pos,color,size):
        self.screen = screen
        self.size = size
        self.color = color
        self.pos = pos
        self.vel = [choice([-5,5]),choice([-5,5])]
        self.RADIUS = 10

    def create(self):
        return circle(self.screen,
                      self.color,
                      self.pos,
                      self.RADIUS)

    def move(self):

        if self.pos[0] > (self.size[0] - self.RADIUS) or self.pos[0] < self.RADIUS:

            self.pos[0] , self.pos[1] = self.size[0] // 2 , self.size[1] // 2

            self.vel = [choice([-5,5]),choice([-5,5])]

        if self.pos[1] > (self.size[1] - self.RADIUS) or self.pos[1] < self.RADIUS:

            self.vel[1] = -self.vel[1]

        self.pos[0] += self.vel[0]

        self.pos[1] += self.vel[1]

    def collision(self,other,side):

        if side == 'left':

            horizontal = (self.pos[0] - self.RADIUS <= other.pos[0] + other.geom[0])

        elif side == 'right':

            horizontal = (self.pos[0] + self.RADIUS >= other.pos[0])

        else:
            horizontal = False

        vertical = (self.pos[1] >= other.pos[1])  and ((self.pos[1] + self.RADIUS) <= (other.pos[1] + other.geom[1]))

        if horizontal and vertical:

            self.vel[0] = -self.vel[0]
