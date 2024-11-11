import pygame
from pygame import Vector2
import globals as gb
from ray import Ray
import numpy as np

class BRay(Ray):
    def __init__(self, 
                 p1 : Vector2|tuple = (0, 0), 
                 angle : float = 0,
                 length : float = 10):
        self.child : BRay = None
        self.angle : float = angle
        self.length : float = length
        p2 = Vector2(p1) + Vector2(np.cos(np.radians(angle)) * length, np.sin(np.radians(angle)) * length)
        super().__init__(p1, p2)

    def update(self,
               p1 : Vector2|tuple = (0, 0),
               angle : float = 0,
               length : float = 10):
        self.child = None
        self.angle : float = angle
        self.length : float = length
        self.p1 = p1
        self.p2 = Vector2(p1) + Vector2(np.cos(np.radians(angle)) * length, np.sin(np.radians(angle)) * length)

    def getChildren(self) -> int:
        if self.child == None:
            return 0
        else:
            return self.child.getChildren() + 1

    def childP2(self):
        if self.child:
            return self.child.childP2()
        else:
            return self.p2
        
    def drawChildren(self, 
                     screen : pygame.Surface):
        self.draw(screen)
        if self.child:
            self.child.drawChildren(screen)

    def collide(self,
                colliders : list[Ray] = [],
                collideCount : int = 0) -> tuple[Vector2, float, int] | None:
        collisions = self.collisionPointList(colliders, sortCollisions=True)

        # print(len(collisions), collisions, self.getChildren())
        if len(collisions) > 0:
            collideCount += 1

            minCollision = collisions[0]
            newLength = self.length - minCollision[1]

            normal = minCollision[2]
            rayAngle = self.getAngle()
            relAngle = rayAngle - normal
            angle = normal - relAngle + 180

            childLength = minCollision[1]

            self.child = BRay(
                p1 = minCollision[0],# + Vector2(np.cos(np.radians(self.angle)) * newLength, np.sin(np.radians(self.angle)) * newLength),
                angle = angle,
                length = childLength,
            )
            childCollide = self.child.collide(colliders, collideCount)
            if childCollide:
                return childCollide
            else:
                return self.child.p2, self.child.angle, collideCount

class Ball:
    def __init__(self,
                 pos : Vector2 = (gb.SX/2, gb.SY/2),
                 size : int = 1,
                 color : tuple = (255, 255, 255),
                 gravity : float = 20,
                 drag : float = .15):
        self.pos : Vector2 = Vector2(pos)
        self.velo : Vector2 = Vector2(0, 0)
        self.size : int = size
        self.color : tuple = color
        self.ray : BRay = BRay()
        self.grav = gravity
        self.drag = drag

    def move(self,
             screen : pygame.Surface,
             dt : float,
             colliders : list[Ray] = []):
        # self.ray.drawChildren(screen)

        self.gravity(dt)

        self.ray.update(self.pos, 
                        np.degrees(np.atan2(self.velo.y, self.velo.x)),
                        np.sqrt((self.velo.x)**2 + (self.velo.y)**2))

        cData = None
        if (np.floor(self.velo.x) != 0 or np.floor(self.velo.y) != 0):
            cData = self.ray.collide(colliders)

        if cData:
            self.pos = cData[0]
            angle = cData[1]
            drag = self.drag*cData[2]
            
            veloDist = np.sqrt((self.velo.x)**2 + (self.velo.y)**2) * (1-drag)

            self.velo = Vector2(np.cos(np.radians(angle)) * veloDist, np.sin(np.radians(angle)) * veloDist)
        else:
            self.pos = self.ray.p2

    def gravity(self,
                dt : float):
        self.velo += Vector2(0, self.grav * dt)

    def draw(self,
             screen : pygame.Surface):
        # pass
        pygame.draw.circle(screen, self.color, self.pos, self.size)
        pygame.draw.line(screen, (255, 255, 255), self.pos, self.pos + self.velo, 1)

    def update(self,
               screen : pygame.Surface,
               dt : float,
               colliders : list[Ray] = []):
        # self.draw(screen)
        self.move(screen, dt, colliders)