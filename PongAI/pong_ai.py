import pygame
import sys
import pandas as pd
from sklearn import ensemble
from sklearn.model_selection import train_test_split
import joblib
import numpy as np

class Ball:

    def __init__(self,screen,color,rad,pos):
        self.screen = screen
        self.color = color
        self.rad = rad
        self.pos = pos
        self.vel = [5,5]
        self.acc = 1

    def create(self):
        pygame.draw.circle(screen, self.color, self.pos, self.rad)


    def move(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]


    def collision(self,obj_y):

        if self.pos[1] > (obj_y - self.rad) or self.pos[1] < self.rad:
            self.vel[1] = -self.vel[1]


    def collision_with(self,other,left_side=False):
        self.left_side = left_side

        if self.left_side:
            if self.pos[0] < (other.posx + other.geometry[0])  and self.pos[1] > other.movement and self.pos[1] < other.movement + other.geometry[1] :
                self.vel[0] = -self.vel[0]
                if self.vel[0] < 20:
                    self.vel[0] += self.acc
                    self.vel[1] += self.acc

        else:
            if self.pos[0] > other.posx   and self.pos[1] > other.movement and self.pos[1] < other.movement + other.geometry[1] :
                self.vel[0] = -self.vel[0]
                if self.vel[0] < 10:
                    self.vel[0] -= self.acc
                    self.vel[1] -= self.acc


class Player:

    def __init__(self,screen,color,posx,geometry):
        self.screen = screen
        self.color = color
        self.posx = posx
        self.movement = 200
        self.geometry = geometry
        self.points =  0


    def create(self):
        pygame.draw.rect(self.screen,self.color, (self.posx, self.movement, self.geometry[0], self.geometry[1]))

    def intelligence(self):
        self.df = pd.read_csv("data.csv")
        self.df.drop_duplicates()
        self.X = self.df.drop(columns="posy").values
        self.y = self.df['posy'].values

        self.X_train ,self.X_test ,self.y_train ,self.y_test = train_test_split(self.X,self.y,test_size=0.30,random_state=10)
        self.AI = ensemble.RandomForestRegressor(random_state=10)
        self.AI.fit(self.X_train,self.y_train)

        print("Score: ",self.AI.score(self.X_test,self.y_test))

        joblib.dump(self.AI,'model.pkl')

        self.data = pd.DataFrame(columns=['x','y','dx','dy'])

    def prediction(self,x,y,dx,dy):
        self.ballpos = self.data.append({'x':x,'y':y,'dx':dx,'dy':dy},ignore_index= True)
        self.movement = int(self.AI.predict(self.ballpos))


    def move(self,keys,dsp,ach):
        self.keys = keys

        if self.movement < 0 :
            self.movement = 0
        if self.movement > ( ach - self.geometry[1] ):
            self.movement = ( ach - self.geometry[1] )

        if self.keys[dsp[0]]:
            self.movement += 7
        if self.keys[dsp[1]]:
            self.movement -= 7



pygame.init()
WIDTH = 1000
HEIGHT = 600
FRAMES = 90
SIZE = (WIDTH,HEIGHT)
start = "Press ENTER Key"
flag = False

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("PONG GAME V0.0.1")

clock = pygame.time.Clock()
bgcolor = (40,40,40)
fgcolor = (255,255,255)

ball = Ball(screen,fgcolor,15,[int(WIDTH/2) ,int(HEIGHT/2)])
p1 = Player(screen,fgcolor,(WIDTH - 20),[20,100])
p2 = Player(screen,fgcolor,0,[20,100])

def point_counter(ball,p1,p2):

    if ball.pos[0] > WIDTH:
        p2.points += 1
        return True
    elif ball.pos[0] < 0:
        p1.points += 1
        return True
    else:
        return False

while True:

    keys = pygame.key.get_pressed()

    screen.fill(bgcolor)
    pygame.draw.circle(screen, fgcolor, [int(WIDTH/2) ,int(HEIGHT/2)],100,5)
    pygame.draw.line(screen,fgcolor,(int(WIDTH/2),0),(int(WIDTH/2),HEIGHT),5)

    label = pygame.font.SysFont("Bauhaus 93", 60)
    texto = label.render(start, True, fgcolor, bgcolor)
    screen.blit(texto, (330,90))

    label1 = pygame.font.SysFont("Bauhaus 93", 40)
    texto1 = label1.render(str(p1.points), True, fgcolor, bgcolor)
    screen.blit(texto1, (700, 50))

    label2 = pygame.font.SysFont("Bauhaus 93", 40)
    texto2 = label2.render(str(p2.points), True, fgcolor, bgcolor)
    screen.blit(texto2, (300, 50))

    if point_counter(ball,p1,p2):
        ball.pos = [int(WIDTH/2) ,int(HEIGHT/2)]
        if  np.random.randint(0,2) == 0:
            ball.vel[0],ball.vel[1] =  5, 5

        elif np.random.randint(0,4) == 0:
            ball.vel[0],ball.vel[1] =  5, -5

        elif np.random.randint(0,4) == 1:
            ball.vel[0],ball.vel[1] =  -5, 5
        else:
            ball.vel[0],ball.vel[1] =  -5, -5

        flag = False
        start = 'Press ENTER key'




    p1.create()
    p2.create()
    p1.move(keys,[pygame.K_DOWN,pygame.K_UP],HEIGHT)
    p2.move(keys,[pygame.K_s,pygame.K_w],HEIGHT)

    ball.create()
    ball.collision(HEIGHT)
    ball.collision_with(p1)
    ball.collision_with(p2,20)

    if keys[pygame.K_RETURN]:
        flag = True
        start = ''
    if flag:
        ball.move()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    pygame.display.update()
    clock.tick(FRAMES)
