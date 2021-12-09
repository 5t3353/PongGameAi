import sys
import os
import pygame
from time import perf_counter
from pandas import DataFrame ,read_csv ,concat
from objects.ball import Ball
from objects.player import Player
from auto.ai import AiModel

def run():

    WIDTH = 1000
    HEIGHT = 600
    FRAMES = 90
    BGCOLOR = (0,0,0)
    FGCOLOR = (0,255,0)
    SIZE = (WIDTH,HEIGHT)
    MIDDLE = [WIDTH // 2, HEIGHT // 2]
    RIGHT_SIDE = [980,200]
    LEFT_SIDE = [0,200]

    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("PONG GAME")
    clock = pygame.time.Clock()

    ball = Ball(screen,MIDDLE,FGCOLOR,SIZE)

    player1 = Player(screen,FGCOLOR,LEFT_SIDE,SIZE)

    player2 = Player(screen,FGCOLOR,RIGHT_SIDE,SIZE)

    files = ['auto/datal.csv','auto/data.csv']

    p1_ai = AiModel(files[0])
    p2_ai = AiModel(files[1])
    p1_ai.fit_model()
    p2_ai.fit_model()

    start_timer = perf_counter()

    df = DataFrame(columns = ['x','y','dx','dy','movement'])

    while True:

        screen.fill(BGCOLOR)

        keys = pygame.key.get_pressed()

        ball.create()
        player1.create()
        player2.create()
        ball.collision(player1,'left')
        ball.collision(player2,'right')
        ball.move()


        player1.turn_ai(p1_ai.model_pipe , [ball.pos[0],
                                            ball.pos[1],
                                            ball.vel[0],
                                            ball.vel[1]])

        player2.turn_ai(p2_ai.model_pipe , [ball.pos[0],
                                            ball.pos[1],
                                            ball.vel[0],
                                            ball.vel[1]])



        player1.move(control = [ pygame.K_s , pygame.K_w ],keys = keys)
        player2.move(control = [ pygame.K_DOWN , pygame.K_UP ],keys = keys)

        timer = int(perf_counter() - start_timer)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

        pygame.display.update()
        clock.tick(FRAMES)



if __name__=='__main__':

    run()
