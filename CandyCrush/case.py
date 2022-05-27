import pygame
import random
from plateau import *


class Case():
    def __init__(self, pos, plateau):
        self.liste_img=["bleu.png", "orange.png", "rouge.png", "violet.png", "vert.png", "jaune.png"]
        self.strImg = random.choice(self.liste_img)
        self.img = pygame.image.load(self.strImg)
        self.position = pos
        self.plateau = plateau
