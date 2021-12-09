from pygame.draw import rect
from numpy import array , reshape

class Player:

    def __init__(self,screen,color,pos,size):
        self.screen = screen
        self.color = color
        self.pos = pos
        self.size = size
        self.geom = [20,100]

    def create(self):
        return rect( self.screen,
                     self.color,
                    (self.pos[0],
                     self.pos[1],
                     self.geom[0],
                     self.geom[1]) )

    def turn_ai(self,model,X):

        X = array(X).reshape(1,-1)

        self.pos[1] = int(model.predict(X))

    def move(self,control,keys):

        if self.pos[1] < 0 :
            self.pos[1] = 0

        if self.pos[1] > self.size[1] - self.geom[1]:
            self.pos[1] = self.size[1] - self.geom[1]

        if keys[control[0]]:
            self.pos[1] += 7
        if keys[control[1]]:
            self.pos[1] -= 7
