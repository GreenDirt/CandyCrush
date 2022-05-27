import pygame
import random
from plateau import Plateau

pygame.init()

clock = pygame.time.Clock()
jeu_fini = False

sizePlateau = (960, 880)
plateau = Plateau((sizePlateau[0], sizePlateau[1]))


while not jeu_fini:
	for event in pygame.event.get():
		if event.type == pygame.MOUSEBUTTONDOWN:          #Clic active, on gere la selection d'un bonbon si le clic est dans le cadre du plateau
			if(0 < pygame.mouse.get_pos()[0] < sizePlateau[0]):
				print(pygame.mouse.get_pos()[0])
				plateau.setSelection(pygame.mouse.get_pos())
		if event.type == pygame.MOUSEBUTTONUP:            #Clic desactive, on gere l'inversion des bonbons et la deselection si le clic est dans le plateau
			if(0 < pygame.mouse.get_pos()[0] < sizePlateau[0]):
				plateau.cible(pygame.mouse.get_pos())
				plateau.setSelection(pygame.mouse.get_pos(), True)


		if event.type  == pygame.QUIT:
			jeu_fini = True
			pygame.quit()
			print("Fermeture du jeu")


	pygame.display.update()

	clock.tick(30)