import pygame, sys
from pygame.locals import *
from playsound import playsound
from pathlib import Path
import math
import keyboard
import random
import controller
from pygame.math import Vector2

SCRIPT_DIR = Path(__file__).parent
GEAR = SCRIPT_DIR / 'running-gear-6403.mp3'

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Screen information
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 1000

DISPLAY = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAY.fill(WHITE)
pygame.display.set_caption("Graffiti Gamebot")

Score = 0



def rotate(image, rect, angle, offset):
    """Rotate the image while keeping its center."""
    # Rotate the original image without modifying it.
    new_image = pygame.transform.rotate(image, angle)
    offset_rotated = offset.rotate(-angle)
    # Get a new rect with the center of the old rect.
    rect = new_image.get_rect(center=rect.center+offset_rotated)
    return new_image, rect


class Arm1(pygame.sprite.Sprite):
    def __init__(self, id):
        super().__init__()

        self.moving = False

        self.joy = pygame.joystick.Joystick(id)
        self.name = self.joy.get_name()
        self.joy.init()
        self.numaxes = self.joy.get_numaxes()
        self.numballs = self.joy.get_numballs()
        self.numbuttons = self.joy.get_numbuttons()
        self.numhats = self.joy.get_numhats()

        self.axis = []
        for i in range(self.numaxes):
            self.axis.append(self.joy.get_axis(i))

        self.ball = []
        for i in range(self.numballs):
            self.ball.append(self.joy.get_ball(i))

        self.button = []
        for i in range(self.numbuttons):
            self.button.append(self.joy.get_button(i))

        self.hat = []
        for i in range(self.numhats):
            self.hat.append(self.joy.get_hat(i))

        self.image = pygame.image.load("arm1.png")
        self.rotation = 0
        self.image = pygame.transform.rotate(self.image, self.rotation)
        self.rect = self.image.get_rect()
        self.rect.center = (240, 350)

    def update(self):
        pressed_keys = pygame.key.get_pressed()

        hat = self.joy.get_hat(0)
        rightbutton = self.joy.get_button(5)
        leftbutton = self.joy.get_button(4)

        self.rect.move_ip(0,5 * self.joy.get_axis(1))
        

        self.rotation += -self.joy.get_axis(3)

        if self.rotation > 75:
            self.rotation = 75

        if self.rotation < -75:
            self.rotation = -75

        if self.rect.centery > 650:
            self.rect.centery = 650
        
        if self.rect.centery < 60:
            self.rect.centery = 60

        Mouse_x, Mouse_y = pygame.mouse.get_pos()
        global Score 
        Score = (Mouse_x, Mouse_y)
        # if pressed_keys[K_UP]:
        # playsound(r"C:\Users\night\PythonProjects\GEAR.mp3")
        # self.rect = self.image.get_rect()

    def draw(self, surface):
        image, rect = rotate(self.image, self.rect, self.rotation, Vector2(210, 0))
        surface.blit(image, rect)


R1 = Arm1(0)


class Pole(pygame.sprite.Sprite):
    def __init__(self, id):
        super().__init__()
        self.image = pygame.image.load("Pole.png")
        self.image = pygame.transform.scale(self.image, (700, 700))
        self.rotation = 0
        #self.image = pygame.transform.rotate(self.image, self.rotation)
        self.rect = self.image.get_rect()
        self.rect.center = (250, 350)

    def draw(self, surface):
        image, rect = rotate(self.image, self.rect, self.rotation, Vector2(0,0))
        surface.blit(image, rect)

P1 = Pole(1)

class arm2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.joy = pygame.joystick.Joystick(0)
        # self.name = self.joy.get_name()
        self.joy.init()
        self.image = pygame.image.load("arm1.png")
        self.rect = self.image.get_rect()
        self.rect.center = (R1.rect.center)
        self.offset = Vector2(0, 0)
        self.direction = 0
        self.toggled = False

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        hat = self.joy.get_hat(0)
        self.rect.center = (R1.rect.center)

        if (pressed_keys[K_z] or self.joy.get_button(2)) and not self.toggled:
            if self.offset.x == 0:
                self.offset.x = 400
            elif self.offset.x == 400:
                self.offset.x = 0

        self.toggled = (pressed_keys[K_z] or self.joy.get_button(2))
        if self.offset.x > 400:
            self.offset.x = 400

        if self.offset.x < 0:
            self.offset.x = 0

        

    def draw(self, surface):
        image, rect = rotate(self.image, self.rect, R1.rotation, Vector2(210,0))
        rotatedoffset = self.offset.rotate(-R1.rotation)
        rect = image.get_rect(center=rect.center+rotatedoffset)
        surface.blit(image, rect)

R2 = arm2()

class fingers(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.joy = pygame.joystick.Joystick(0)
        # self.name = self.joy.get_name()
        self.joy.init()
        self.image = pygame.image.load("fingers.png")
        self.image = pygame.transform.scale(self.image, (200, 200))
        self.rect = self.image.get_rect()
        self.rect.center = (R1.rect.center)
        self.offset = Vector2(0, 0)
        self.direction = 0
        self.toggled = False
        self.closed = False

    def update(self):
        actualcenter = Vector2 (self.rect.centerx, self.rect.centery)
        actualcenter += Vector2 (535 + R2.offset.x,0).rotate (-R1.rotation)
        if self.joy.get_button(3) and not self.toggled and not self.closed:
            self.image = pygame.image.load("closedfingers.png")
            self.image = pygame.transform.scale(self.image, (200, 200))
            if C1.rect.centerx > actualcenter.x - 100 and C1.rect.centerx < actualcenter.x + 100 and C1.rect.centery > actualcenter.y - 100 and C1.rect.centery < actualcenter.y + 100:
                C1.grabbed = True
            self.closed = True
        elif self.joy.get_button(3) and not self.toggled and self.closed:
            self.image = pygame.image.load("fingers.png")
            self.image = pygame.transform.scale(self.image, (200, 200))
            if C1.grabbed:
                C1.rect.center = (actualcenter.x, actualcenter.y)
            C1.grabbed = False
            self.closed = False
        
            
        self.toggled = self.joy.get_button(3)

        

    def draw(self, surface):
        self.rect.center = (R1.rect.center)
        image, rect = rotate(self.image, self.rect, R1.rotation, Vector2(210,0))
        rotatedoffset = (R2.offset + Vector2(325,0)).rotate(-R1.rotation)
        rect = image.get_rect(center=rect.center+rotatedoffset)
        surface.blit(image, rect)

F1 = fingers()

class cube(pygame.sprite.Sprite):
    def __init__(self, id):
        super().__init__()
        self.image = pygame.image.load("cubefrc.png")
        self.image = pygame.transform.scale(self.image, (200, 200))
        self.rotation = 0
        #self.image = pygame.transform.rotate(self.image, self.rotation)
        self.rect = self.image.get_rect()
        self.rect.center = (1200, 650)
        self.grabbed = False
        self.velocity  = 0
        self.prevy = 650


    def update(self):
        self.prevy = self.rect.centery
        if self.grabbed == True:
            self.rect.center = F1.rect.center
        if not self.grabbed:
            self.velocity += 0.1 
            self.rect.centery += self.velocity
        if self.rect.centery > 650:
            self.rect.centery = 650
            self.velocity = 0
        if self.prevy <= 110 and self.rect.centery > 110 and self.rect.centerx > 910 and self.rect.centerx < 1490:
            self.rect.centery = 110
            self.velocity = 0

    def draw(self, surface):
        if self.grabbed == True:
            self.rect.center = (R1.rect.center)
            image, rect = rotate(self.image, self.rect, R1.rotation, Vector2(210,0))
            rotatedoffset = (R2.offset + Vector2(325,0)).rotate(-R1.rotation)
            rect = image.get_rect(center=rect.center+rotatedoffset)
            surface.blit(image, rect)
        else:
            surface.blit(self.image, self.rect)

C1 = cube(3)

class Shelf(pygame.sprite.Sprite):
    def __init__(self, id):
        super().__init__()
        self.image = pygame.image.load("shelf.png")
        self.image = pygame.transform.scale(self.image, (700, 700))
        self.rotation = 0
        #self.image = pygame.transform.rotate(self.image, self.rotation)
        self.rect = self.image.get_rect()
        self.rect.center = (1200, 300)

    def draw(self, surface):
        image, rect = rotate(self.image, self.rect, self.rotation, Vector2(0,0))
        surface.blit(image, rect)

S1 = Shelf(4)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    R1.update()
    R2.update()
    F1.update()
    C1.update()
    DISPLAY.fill(WHITE)
    S1.draw(DISPLAY)
    R1.draw(DISPLAY)
    P1.draw(DISPLAY)
    R2.draw(DISPLAY)
    F1.draw(DISPLAY)
    C1.draw(DISPLAY)
    

    font = pygame.font.SysFont(None, 24)
    img = font.render(str(Score), True, RED)
    DISPLAY.blit(img, (20, 20))
    pygame.display.update()
    FramePerSec.tick(FPS)
