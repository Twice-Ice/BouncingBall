import pygame
import globals as gb
from ball import Ball
from ray import Ray
import random

screen = pygame.display.set_mode((gb.SX, gb.SY), pygame.NOFRAME)

doExit = False
clock = pygame.time.Clock()
ball : Ball = None
colliders : list[Ray] = []

def startGame():
    global ball
    global colliders

    colliders = []
    # colliders.append(Ray((0, 200), (gb.SX, gb.SY)))
    for _ in range(5):
        colliders.append(Ray((random.randint(0, gb.SX), random.randint(0, gb.SY)), (random.randint(0, gb.SX), random.randint(0, gb.SY))))
    colliders.append(Ray((0, 0), (0, gb.SY-1)))
    colliders.append(Ray((0, gb.SY-1), (gb.SX-1, gb.SY-1)))
    colliders.append(Ray((gb.SX-1, gb.SY-1), (gb.SX-1, 0)))
    colliders.append(Ray((gb.SX-1, 0), (0, 0)))

    # ball = Ball(pos = (random.randint(0, gb.SX), random.randint(0, gb.SY)),
    # ball = Ball(
    #             drag=-0.001,
    #             size=2,
    #             color = (150, 150, 150))

startGame()
a = 0
FPS = [10, 60]

cd = 0

while not doExit:
    keys = pygame.key.get_pressed()
    dt = clock.tick(FPS[a%len(FPS)])/1000
    if keys[pygame.K_o]:
        dt /= 100
    cd += dt
    screen.fill(gb.BG)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            doExit = True

    if keys[pygame.K_r]:
        startGame()
    if keys[pygame.K_a]:
        ball = Ball(
                drag=-.01,
                size=2,
                color = (150, 150, 150))
    # if keys[pygame.K_SPACE]:
    if ball:
        ball.update(screen, dt, colliders)
    if keys[pygame.K_i]:
        if cd > 1:
            a+=1
            cd = 0
    
    if ball:
        ball.draw(screen)
    for collider in colliders:
        collider.draw(screen)

    pygame.display.flip()
pygame.quit()