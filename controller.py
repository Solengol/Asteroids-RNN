import pygame as pg
from main import Game as game

def controller():
    env = game()
    env.reset()
    while True:
        keys = pg.key.get_pressed()
        action = [0, 0, 0, 0]   
        if keys[pg.K_LEFT]:
            action[0] = 1
        if keys[pg.K_RIGHT]:
            action[1] = 1
        if keys[pg.K_UP]:
            action[2] = 1
        if keys[pg.K_SPACE]:
            action[3] = 1
        observation, reward, done, score = env.run(action)
        env.draw()
        if done: 
            break


if __name__ == "__main__":
    controller()
