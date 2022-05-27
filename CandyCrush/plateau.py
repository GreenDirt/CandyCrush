import random
from case import Case
import pygame
import time

class Plateau():
    """
    Attributs :
        size : tuple de la taille de l'ecran
        ecran : l'objet pygame screen
        plateau : dictionnaire contenant les bonbons sous la forme plateau[x, y]
        caseCible
        caseSelectionnee
        posCaseSelectionnee
        score
    Methodes :
        updateAffichage(self) -> Actualisation graphique(blit) de tous les bonbons du plateau
        setSelection(self, mousePos, desactive=False) -> definie la selection lors d'un premier clic sur un bonbon, permet aussi la deselection
        cible(self, mousePos) -> Deuxieme clic, tentative d'inversion, puis appel des fonctions de tests d'alignements et de destruction
        destruction(self, animations=True) -> Fonction principale de destruction, elle appelle les tests, puis les destructeurs
        testAlignementHorizontal(self)
        destructionTroisHorizontal(self, alignements, animations=True)
        animationDescenteBlocHorizontal(self, bloc, vitesseDescente=1)
        testAlignementVertical(self)
        destructionTroisVertical(self, alignements, animations=True)
        animationDescenteBlocVertical(self, bloc, vitesseDescente=10)
        menuAfficher()
        afficherScore()
    """

    def __init__(self, size): #size sous la forme d'un tuple(nombre de pixels)
        #images de 96x88
        pygame.display.set_caption("Candy Crush")
        self.size = size[0], size[1]
        #self.ecran = pygame.display.set_mode(self.size)
        self.ecran = pygame.display.set_mode((size[0]+540, size[1]))

        self.score = 0

        print("*** Generation du plateau ***")
        self.plateau = {}

        for i in range(int(size[0]/96)):
            for j in range(int(size[1]/88)):
                self.plateau[i, j] = Case([i, j], self) #Creation du plateau de base aléatoire

        self.destruction(False) #Suppression des combinaisons initiales sans animations
        self.updateAffichage()        #Affichage des carreau APRES creation du plateau
        self.posCaseSelectionnee = ()
        self.testAlignementVertical()
        self.testAlignementHorizontal()

        self.score = 0
        self.font = pygame.font.SysFont(None, 25)
        self.menuAfficher()
        self.afficherScore()

        print("***Fin de l'initialisation du plateau***")

    def updateAffichage(self):      #Permet d'actualiser l'affichage de toutes les cases du plateau et du menu
        print("--")
        for i in range(int(960/96)):
            for j in range(int((880/88))):
                self.ecran.blit(self.plateau[i, j].img, (i*96, j*88))
        self.menuAfficher() #Actualise le menu
        self.afficherScore()

    def setSelection(self, mousePos, desactive=False):      #Lors d'un premier clic sur un bonbon, permet la sauvegarde de la case selectionnee et l'affichage du cadre bleu
        if(desactive):  #Deselection du bonbon
            try:
                print("Deselection de la case " + str(self.posCaseSelectionnee))
                self.caseSelectionnee.img = pygame.image.load(self.caseSelectionnee.strImg[0:len(self.caseSelectionnee.strImg)-4] + ".png")
                self.caseSelectionnee = 0
                self.posCaseSelectionnee = ()
            except:
                pass
        else:       #Selection du bonbon
            self.posCaseSelectionnee = (int(mousePos[0]/96), int(mousePos[1]/88))
            print("Selection de la case " + str(self.posCaseSelectionnee))
            self.caseSelectionnee = self.plateau[self.posCaseSelectionnee[0], self.posCaseSelectionnee[1]]
            self.caseSelectionnee.img = pygame.image.load(self.caseSelectionnee.strImg[0:len(self.caseSelectionnee.strImg)-4] + "_s.png")   #Rajoute "_s" au nom du bonbon pour obtenir le cadre

        self.updateAffichage()

    def cible(self, mousePos):          #Cible un bloc apres un deuxieme clic, verifie que le clic est valide et gere la destruction des blocs
        posCible = (int(mousePos[0]/96), int(mousePos[1]/88))
        self.caseCible = self.plateau[posCible[0], posCible[1]]

        print(str(posCible[0]) + ";" + str(posCible[1]))
        print(str(self.posCaseSelectionnee[0]) + ";" + str(self.posCaseSelectionnee[1]))
        if(not(self.posCaseSelectionnee[0]-1 <= posCible[0] <= self.posCaseSelectionnee[0]+1 and posCible[1] == self.posCaseSelectionnee[1]) and\
         not(self.posCaseSelectionnee[1]-1 <= posCible[1] <= self.posCaseSelectionnee[1]+1 and posCible[0] == self.posCaseSelectionnee[0])):    #Si le clic n'est pas a cote du bonbon selectionne on annule la selection
            self.setSelection(0, True)
            return 0

        print("Tentative d'inversion des blocs " + str(self.posCaseSelectionnee) + " et " + str(self.caseCible.position))

        self.plateau[self.posCaseSelectionnee[0], self.posCaseSelectionnee[1]] = self.caseCible     #Inverse les deux bonbons, alignements possible ou pas
        self.plateau[posCible[0], posCible[1]] = self.caseSelectionnee

        self.caseSelectionnee.img = pygame.image.load(self.caseSelectionnee.strImg[0:len(self.caseSelectionnee.strImg)-4] + ".png")
        self.updateAffichage()
        pygame.display.update()
        pygame.time.wait(100)   #Permet de voir l'echec ou la reussite qu'on vient de faire(le bonbon change de place puis revient)

        reussite = self.destruction()
        if(not reussite):                                                                           #Si pas d'alignement, on reinverse
            self.plateau[self.posCaseSelectionnee[0], self.posCaseSelectionnee[1]] = self.caseSelectionnee
            self.plateau[posCible[0], posCible[1]] = self.caseCible
            self.updateAffichage()

    def destruction(self, animations=True):      #Detruit les blocs detectes par trois a l'aide des fonctions : testAlignementsHorizontaux, testAlignementsVerticaux, destructionTroisHorizontal, destructionTroisVertical
        print("///////////Debut de la destruction des alignements(Animations : " + str(animations) + ")///////////")

        alignementsHorizontaux = self.testAlignementHorizontal()
        alignementsVerticaux = self.testAlignementVertical()

        reussite = False    #Permet a la methode cible de savoir si des alignements ont ete trouves
        while(alignementsHorizontaux != [] or alignementsVerticaux != []):
            alignementsHorizontaux = self.testAlignementHorizontal()    #On recherche des alignements a chaque destruction pour savoir ce qui a changé
            alignementsVerticaux = self.testAlignementVertical()
            for alignement in alignementsHorizontaux:                   #On prend chaque alignement pour le detruire
                self.destructionTroisHorizontal(alignement, animations)

            for alignement in alignementsVerticaux:
                self.destructionTroisVertical(alignement, animations)
            reussite = True

        print("///////////Fin de la destruction///////////")
        return reussite

    def testAlignementHorizontal(self):
        alignements = []
        for x in range(int(self.size[0]/96)-2):
            for y in range(int(self.size[1]/88)):
                if(self.plateau[x, y].strImg == self.plateau[x+1, y].strImg == self.plateau[x+2, y].strImg):    #On parcourt le plateau pour trouver les alignements horizontaux
                    alignements.append([(x, y), (x+1, y), (x+2, y)])


        print("Alignements horizontaux trouves : " + str(alignements))
        return alignements

    def destructionTroisHorizontal(self, alignements, animations=True): #Alignement sous la forme d'une liste de trois tuples
        print("Destruction de l'alignement horizontal : " + str(alignements))
        for alignement in alignements:
            self.plateau[alignement[0], alignement[1]].img = pygame.image.load("vide.png")
            self.updateAffichage()

        for y in range(alignements[0][1],-1, -1):                       #Parcourt l'alignement en remontant jusqu'en haut, d'abord du point de vue du plateau(pas graphique)
            for x in range(alignements[0][0], alignements[2][0]+1):
                if(y == 0):
                    self.plateau[x, y] = Case([x, -1], self)
                else:
                    self.plateau[x, y] = self.plateau[x, y-1]
                    self.plateau[x, y].position = [x, y-1]
            self.score += 60                                        #Ajoute le score

        if(animations):                                                 #Si l'animation est activee, on descend progressivement les bonbons pour rejoindre les valeurs du plateau
            bloc = []
            for y in range(alignements[0][1]+1):
                    bloc.append((alignements[0][0], y))
                    bloc.append((alignements[1][0], y))
                    bloc.append((alignements[2][0], y))
            self.animationDescenteBlocHorizontal(bloc)

    def animationDescenteBlocHorizontal(self, bloc, vitesseDescente=1): #Le bloc est une liste des tuples de coordonnees a descendre en meme temps
        print("Animation horizontale descente du bloc de bonbons : " + str(bloc))
        for bonbon in bloc:
                self.plateau[bonbon[0], bonbon[1]].position[1] = (self.plateau[bonbon[0], bonbon[1]].position[1])*88    #On convertit en coors brutes pour les coordonnees de y

        descenteTerminee = False
        while(not descenteTerminee):
            for bonbon in bloc:
                self.plateau[bonbon[0], bonbon[1]].position[1] += 1 #Ajoute un pixel a la position du bonbon
                self.ecran.blit(self.plateau[bonbon[0], bonbon[1]].img, (self.plateau[bonbon[0], bonbon[1]].position[0]*96, self.plateau[bonbon[0], bonbon[1]].position[1]))    #Actualise l'affichage avec les coordonnees en y

                if(self.plateau[bonbon[0], bonbon[1]].position[1]%88 == 0): #A l'aide d'un modulo, on regarde si le bonbon a finit sa course (de y1 a y2, on regarde si y == 2*88)
                    descenteTerminee = True

            pygame.display.update()
            pygame.time.wait(vitesseDescente)

    def testAlignementVertical(self):
        alignements = []
        for x in range(int(self.size[0]/96)):
            for y in range(int(self.size[1]/88)-2):
                if(self.plateau[x, y].strImg == self.plateau[x, y+1].strImg == self.plateau[x, y+2].strImg):
                    alignements.append([(x, y), (x, y+1), (x, y+2)])

        print("Alignements verticaux trouves : " + str(alignements))
        return alignements

    def destructionTroisVertical(self, alignements, animations=True): #Alignement sous la forme d'une liste de trois tuples
        print("Destruction de l'alignement vertical : " + str(alignements))
        for alignement in alignements:
            self.plateau[alignement[0], alignement[1]].img = pygame.image.load("vide.png")
            self.updateAffichage()

        x = alignements[0][0]
        for y in range(alignements[2][1], -1, -1):
            if(y < 3):
                self.plateau[x, y] = Case([x, y-3], self)
            else:
                self.plateau[x, y] = self.plateau[x, y-3]
                self.plateau[x, y].position = [x, y-3]
        self.score += 60

        if(animations):
            bloc = []
            for y in range(alignements[2][1]+1):
                    bloc.append((alignements[0][0], y))
            self.animationDescenteBlocVertical(bloc)

    def animationDescenteBlocVertical(self, bloc, vitesseDescente=1): #Le bloc est une liste des tuples de coordonnees a descendre en meme temps
        placeOrigine = self.plateau[bloc[0][0], bloc[0][1]].position[1]
        print("Animation verticale descente du bloc de bonbons : " + str(bloc))
        for bonbon in bloc:
                self.plateau[bonbon[0], bonbon[1]].position[1] = (self.plateau[bonbon[0], bonbon[1]].position[1])*88    #On convertit en coors brutes

        descenteTerminee = False
        while(not descenteTerminee):
            for bonbon in bloc:
                self.plateau[bonbon[0], bonbon[1]].position[1] += 1
                self.ecran.blit(self.plateau[bonbon[0], bonbon[1]].img, (self.plateau[bonbon[0], bonbon[1]].position[0]*96, self.plateau[bonbon[0], bonbon[1]].position[1]))

            if(self.plateau[bloc[0][0], bloc[0][1]].position[1]/88 == placeOrigine+3):
                descenteTerminee = True

            pygame.display.update()
            pygame.time.delay(1)


    def menuAfficher(self):
        print("Affichage du menu")
        white = (255, 255, 255, 255)
        sizeMenu = (200, 100)
        self.rectangle = pygame.Surface(sizeMenu)
        self.font = pygame.font.SysFont(None, 25)
        pygame.draw.rect(self.rectangle, white, self.rectangle.get_rect())
        self.ecran.blit(self.rectangle, (1200,50))
        pygame.display.update()
        pygame.draw.rect(self.rectangle, white, self.rectangle.get_rect())
        self.ecran.blit(self.rectangle, (1200,250))
        pygame.display.update()
        pygame.draw.rect(self.rectangle, white, self.rectangle.get_rect())
        self.ecran.blit(self.rectangle, (1200,650))
        pygame.display.update()

    def afficherScore(self):
        print("Actualisation du score")
        black = (0, 0, 0, 0)
        a = self.score
        txt = self.font.render(str(a), True, black)
        text_rect = txt.get_rect()
        text_rect = (1200 + 200/2, 50 + 35)
        self.ecran.blit(txt, text_rect)
        pygame.display.update()

