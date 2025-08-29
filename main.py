from random import *
import numpy as np
from pygame import *
from time import *
from math import *


#génération du terrain
def génération(largeur,hauteur):
    #passage des variables en mode global pour les utiliser partout dans le code
    global terrain_exploration
    global monstres_exploration
    global position_joueur
    global terrain_généré
    #initialisation de la position du joueur
    position_joueur = [largeur//2,hauteur//2]
    #création des variables
    nombre_de_monstres = int(largeur*hauteur/100)
    terrain_exploration = np.zeros((largeur,hauteur,5))
    monstres_exploration = np.zeros((nombre_de_monstres,2))
    #écran de chargement
    fenêtre.fill(bleu)
    text = police.render("Génération ...",1,noir)
    fenêtre.blit(text, (285*zoom+dec_x, 330*zoom+dec_y))
    fenêtre.blit(télé,(0,0))
    draw.rect(fenêtre,noir,Rect(245*zoom+dec_x,350*zoom+dec_y,210*zoom,35*zoom))
    for n in range(nombre_de_monstres):
        monstres_exploration[n] = [randint(0,largeur-1),randint(0,hauteur-1)]
    for y in range(hauteur):
        draw.rect(fenêtre,gris,Rect(250*zoom+dec_x,355*zoom+dec_y,int(200*zoom/hauteur*y),25*zoom))
        display.flip()  #mise a jour de la fenêtre
        for x in range(largeur):        #génération des mur : 0 = mur en haut, 1 = mur à droite, 2 = mur en bas, 3 = mur à gauche, 4 = cassette
            if y==0:                    
                terrain_exploration[x][y][0] = 2
            else:
                terrain_exploration[x][y][0] = terrain_exploration[x][y-1][2]
            if x+1==largeur:
                terrain_exploration[x][y][1] = 2
            else:
                terrain_exploration[x][y][1] = randint(1,2)     #1=pas de mur 2=mur
            if y+1==hauteur:
                terrain_exploration[x][y][2] = 2
            else:
                terrain_exploration[x][y][2] = randint(1,2)
            if x ==0:
                terrain_exploration[x][y][3] = 2
            else:
                terrain_exploration[x][y][3] = terrain_exploration[x-1][y][1]
            if randint(0,49)==0:
                terrain_exploration[x][y][4] = 1
            #si tous les mur son present alors on retire deux mur face a face
            if terrain_exploration[x][y][0]==terrain_exploration[x][y][1]==terrain_exploration[x][y][2]==terrain_exploration[x][y][3]==2:
                if randint(0,1)==1:
                    if y!=0 and y!=hauteur-1:
                        terrain_exploration[x][y][0]=1
                        terrain_exploration[x][y-1][2]=1
                        terrain_exploration[x][y][2]=1
                        terrain_exploration[x][y+1][0]=1
                else:
                    if x!=0 and x!=largeur-1:
                        terrain_exploration[x][y][1]=1
                        terrain_exploration[x+1][y][3]=1
                        terrain_exploration[x][y][3]=1
                        terrain_exploration[x-1][y][1]=1
    terrain_généré = 1

#affichage du terrain autour du joueur avec le décalage
def affichage(decalage_x,decalage_y):
    global zoom
    global monstres
    #affichage du sol
    fenêtre.fill(couleur_sol)
    for x in range(-1,8):
        for y in range(-1,6):
            #variables pour éviter les répétitions
            xx = x+position_joueur[0]-3
            yy = y+position_joueur[1]-2
            #si le carrau est à l'interrieur du terrain affichage des murs presents
            if xx<len(terrain[0]) and xx>-1 and yy<len(terrain) and yy>-1:
                if terrain[xx][yy][0]==2:
                    draw.rect(fenêtre, couleur_mur, Rect((x*100-10+decalage_x)*zoom+dec_x, (y*100+decalage_y)*zoom+dec_y, 120*zoom, 10*zoom))
                if terrain[xx][yy][1]==2:
                    draw.rect(fenêtre, couleur_mur, Rect((x*100+90+decalage_x)*zoom+dec_x, (y*100-10+decalage_y)*zoom+dec_y, 10*zoom, 120*zoom))
                if terrain[xx][yy][2]==2:
                    draw.rect(fenêtre, couleur_mur, Rect((x*100-10+decalage_x)*zoom+dec_x, (y*100+90+decalage_y)*zoom+dec_y, 120*zoom, 10*zoom))
                if terrain[xx][yy][3]==2:
                    draw.rect(fenêtre, couleur_mur, Rect((x*100+decalage_x)*zoom+dec_x, (y*100-10+decalage_y)*zoom+dec_y, 10*zoom, 120*zoom))
                if terrain[xx][yy][4]==1:
                    fenêtre.blit(cassette,((x*100+30+decalage_x)*zoom+dec_x,(y*100+40+decalage_y)*zoom+dec_y))
                if terrain[xx][yy][4]==2:
                    draw.rect(fenêtre,noir, Rect((x*100+10+decalage_x)*zoom+dec_x, (y*100+10+decalage_y)*zoom+dec_y, 80*zoom, 80*zoom))
            #sinon affichage d'un mur plein
            else:
                draw.rect(fenêtre, couleur_mur, Rect((x*100+decalage_x)*zoom+dec_x, (y*100+decalage_y)*zoom+dec_y, 100*zoom, 100*zoom))
    #affichage du joueur
    draw.rect(fenêtre, couleur_joueur, Rect(320*zoom+dec_x, 220*zoom+dec_y, 60*zoom, 60*zoom))
    #afficahge monstres
    for n in range(len(monstres)):
        if monstres[n][0]==position_joueur[0] and  monstres[n][1]==position_joueur[1]:
            perdu()
        if monstres[n][0]<=position_joueur[0]+4 and monstres[n][0]>=position_joueur[0]-4 and monstres[n][1]<=position_joueur[1]+3 and monstres[n][1]>=position_joueur[1]-3:
            fenêtre.blit(monstre,(((monstres[n][0]-position_joueur[0])*100+10+300+decalage_x)*zoom+dec_x,((monstres[n][1]-position_joueur[1])*100+10+200+decalage_y)*zoom+dec_y))
    if timer!=0:
        affichage_timer()
    affichage_nb_cassette()
    #affichage télé
    fenêtre.blit(télé,(0,0))
    display.flip()

#animation du déplacement grace au décalage de l'affichage
def animation(direction):
    durée_déplacement = 0.3 #secondes
    temps = time()
    if direction==0:
        direction_xy = [0,1]
    elif direction==1:
        direction_xy = [1,0]
    elif direction==2:
        direction_xy = [0,-1]
    elif direction==3:
        direction_xy = [-1,0]
    while time()<temps+durée_déplacement:
        affichage(direction_xy[0]*((time()-temps)/durée_déplacement)*100,direction_xy[1]*((time()-temps)/durée_déplacement)*100)

def verif_cassette(x,y):
    global nb_cassette
    if terrain[x][y][4]==1:
        nb_cassette += 1
        terrain[x][y][4]=0

#verification des touches du clavier
def touches_jeu():
    global quitter
    global terrain_généré
    global orientation_joueur
    global temps_suppression_mur
    for evenement in event.get():
        if evenement.type == QUIT:
            #fermeture de la fenêtre
            quit()
            quitter = 0
            return
        if evenement.type == KEYDOWN:
            if evenement.key == K_KP_ENTER and temps_suppression_mur<time()-60:
                temps_suppression_mur = time()          #suppression mur en face du joueur
                terrain[position_joueur[0]][position_joueur[1]][orientation_joueur] = 1
                if orientation_joueur == 0:
                    terrain[position_joueur[0]][position_joueur[1]-1][2] = 1
                elif orientation_joueur == 1:
                    terrain[position_joueur[0]+1][position_joueur[1]][3] = 1
                elif orientation_joueur == 2:
                    terrain[position_joueur[0]][position_joueur[1]+1][0] = 1
                elif orientation_joueur == 3:
                    terrain[position_joueur[0]-1][position_joueur[1]][1] = 1
            if evenement.key == K_UP and terrain[position_joueur[0]][position_joueur[1]][0] == 1:
                orientation_joueur = 0
                animation(0)
                position_joueur[1]-=1
                verif_cassette(position_joueur[0],position_joueur[1],)
            if evenement.key == K_DOWN and terrain[position_joueur[0]][position_joueur[1]][2] == 1:
                orientation_joueur = 2
                animation(2)
                position_joueur[1]+=1
                verif_cassette(position_joueur[0],position_joueur[1])
            if evenement.key == K_LEFT and terrain[position_joueur[0]][position_joueur[1]][3] == 1:
                orientation_joueur = 3
                animation(1)
                position_joueur[0]-=1
                verif_cassette(position_joueur[0],position_joueur[1])
            if evenement.key == K_RIGHT and terrain[position_joueur[0]][position_joueur[1]][1] == 1:
                orientation_joueur = 1
                animation(3)
                position_joueur[0]+=1
                verif_cassette(position_joueur[0],position_joueur[1])
            if evenement.key == K_ESCAPE:
                menu()

#comptage du nombre de cassettes
def nombre_de_cassettes():
    retour = 0
    for x in range(len(terrain)):
        for y in range(len(terrain[0])):
            if terrain[x][y][4]==1:
                retour += 1
    return retour

def deplacement_monstres():     #déplacement des monstres toutes les demis seconde
    global temps_monstres
    if temps_monstres+0.5<time():
        temps_monstres = time()
        for n in range(len(monstres)):
            monstre_x, monstre_y = monstres[n]
            joueur_x, joueur_y = position_joueur
            if randint(0,4)==0: #20% de chance que le déplacement soit aléatoire pour ne pas qu'il soit coincé et 80% de chance qu'il se déplace vers le joueur
                direction = randint(0,3)
            else:
                angle = atan2(joueur_y - monstre_y, joueur_x - monstre_x)
                direction = int((angle + pi) / (pi / 2)) % 4
            if direction == 1 and monstre_y > 0 and terrain[int(monstre_x)][int(monstre_y)][0] == 1:
                monstres[n][1] -= 1  # haut
            elif direction == 2 and monstre_x < len(terrain) - 1 and terrain[int(monstre_x )][int(monstre_y)][1] == 1:
                monstres[n][0] += 1  # Droite
            elif direction == 3 and  monstre_y < len(terrain[0]) - 1 and terrain[int(monstre_x)][int(monstre_y)][2] == 1:
                monstres[n][1] += 1  # Bas
            elif direction == 0 and monstre_x > 0 and terrain[int(monstre_x)][int(monstre_y)][3] == 1:
                monstres[n][0] -= 1  # gauche

def gagné():
    fenêtre.fill(bleu)
    police1 = font.Font(None, int(50*zoom))
    text = police1.render('GAGNE!',1,noir)
    fenêtre.blit(text, (300*zoom+dec_x,200*zoom+dec_y))
    display.flip()
    sleep(1)
    menu()

def perdu():
    fenêtre.fill(bleu)
    police1 = font.Font(None, int(50*zoom))
    text = police1.render('PERDU!',1,noir)
    fenêtre.blit(text, (300*zoom+dec_x,200*zoom+dec_y))
    display.flip()
    sleep(1)
    menu()

#boucle de jeu
def exploration():
    global quitter
    global nb_de_cassettes          #nombre de cassettes total
    global nb_cassette
    nb_cassette = 0
    nb_de_cassettes = nombre_de_cassettes()
    #variable pour sortir de la boucle de jeu
    continuer = True
    while continuer==1 and quitter == 0:
        touches_jeu()
        affichage(0,0)
        deplacement_monstres()
        if nb_cassette == nb_de_cassettes and terrain[position_joueur[0]][position_joueur[1]][4]==2:
            gagné()

def affichage_nb_cassette():
    global nb_de_cassettes
    text = police.render('score: '+str(nb_cassette)+'/'+str(nb_de_cassettes),1,noir)
    fenêtre.blit(text, (560*zoom+dec_x,30*zoom+dec_y))

def affichage_timer():
    global timer
    text = police.render('temps restant: '+str(int(timer-time())),1,noir)
    fenêtre.blit(text, (10*zoom+dec_x,30*zoom+dec_y))
    if timer < time():
        perdu()

#création d'un bouton
def bouton(x,y,nom):
    text = police.render(nom,1,noir)
    draw.rect(fenêtre,gris,Rect(x+dec_x,y+dec_y,150*zoom,50*zoom))
    draw.rect(fenêtre,blanc,Rect(x+5*zoom+dec_x,y+5*zoom+dec_y,140*zoom,40*zoom))
    fenêtre.blit(text, (x+25*zoom+dec_x,y+16*zoom+dec_y))

#verification si le bouton est pressé
def verif_bouton(pos,x,y,l,L):
    if pos[0]<=(x+l)*zoom+dec_x and pos[0]>=x*zoom+dec_x and pos[1]<=(y+L)*zoom+dec_y and pos[1]>=y*zoom+dec_y:
        return 1
    else: return 0


#passage sur la fenêtre de menu
def menu():
    global monstres
    global nb_cassette
    global terrain_généré
    global timer
    global quitter
    global terrain
    menu = 1
    #verifivation des boutons du menu
    while menu == 1 and quitter == 0:
        affichage_menu()
        for evenement in event.get():
            if evenement.type == QUIT:
                menu = 0
                quitter = 1
            if evenement.type == MOUSEBUTTONDOWN:
                if evenement.button == 1:
                    pos = evenement.pos
                    if verif_bouton(pos,50,50,150,50)==1:
                        niveaux()
                    if verif_bouton(pos,50,125,150,50)==1:
                        if terrain_généré == 0:
                            génération(largeur,hauteur)
                            nb_cassette = 0
                            terrain_généré = 1
                        timer = 0
                        monstres = monstres_exploration
                        terrain = terrain_exploration
                        exploration()
                    if verif_bouton(pos,50,200,150,50)==1:
                        paramètres()

#animation de l'arrière plan des menus
def animation_menu():
    global temps_bonhomme
    global temps_facade
    global temps_lampadaire
    global temps_flame_lampadaire
    if time()-durée_animation_facade>temps_facade:  #affichage de 3 facade suivant le temps pour créer un déplacement
        temps_facade=time()
    for numero in range(3):
            fenêtre.blit(facade,(int(numero*int(919*0.5*zoom)-(time()-temps_facade)/durée_animation_facade*int(919*0.5*zoom))+dec_x,-10+dec_y))

    if time()-durée_animation_bonhomme>temps_bonhomme:  #affichage du bonhomme avec la bonne position par rapport au temps
        temps_bonhomme=time()
    fenêtre.blit(personnage[int((time()-temps_bonhomme)*8)],(300*zoom+dec_x,320*zoom+dec_y))
    
        

    if time()-durée_animation_lampadaire>temps_lampadaire:  #affichage de 3 lampadaire suivant le temps pour créer un déplacement
        temps_lampadaire=time()
    if time()-durée_animation_flame_lampadaire>temps_flame_lampadaire:
        temps_flame_lampadaire=time()
    for numero in range(4):
        fenêtre.blit(lampadaire_double[int(((time()-temps_flame_lampadaire)/durée_animation_flame_lampadaire*4)-0.5)],(numero*300*zoom-(time()-temps_lampadaire)/durée_animation_lampadaire*300*zoom+dec_x,310*zoom+dec_y))
    fenêtre.blit(télé,(0,0))


#mise a jour des variables liées a zoom
def changement_zoom():
    global facade
    global police
    global personnage
    global zoom
    global fenêtre
    global lampadaire_double
    global télé
    global dec_x
    global dec_y
    global monstre
    dec_x = 109*zoom
    dec_y = 145*zoom
    cassette = image.load("./images/cassette.png")
    cassette = transform.scale(cassette,(40*zoom,20*zoom))
    monstre = image.load("./images/monstre.png")
    monstre = transform.scale(monstre,(80*zoom,80*zoom))
    fenêtre = display.set_mode(((700+219)*zoom,(500+315)*zoom))
    télé = image.load("./images/télé.png")
    télé = transform.scale(télé,(919*zoom,815*zoom))
    police = font.Font(None, int(30*zoom)) 
    facade = image.load("./images/facade.jpg")
    facade = transform.scale(facade,(919*0.5*zoom,1024*0.5*zoom))
    for numero in range(8):
        personnage[numero] = image.load("./images/image bonhomme qui court "+str(numero+1)+".png").convert_alpha()
        personnage[numero] = transform.scale(personnage[numero], (31*3*zoom,61*3*zoom))
    for numero in range(4):
        lampadaire_double[numero] = image.load("./images/lampadaire-"+str(numero)+".png").convert_alpha()
        lampadaire_double[numero] = transform.scale(lampadaire_double[numero], (130*zoom,260*zoom)).convert_alpha()
    affichage_paramètre()

def paramètres():
    global zoom
    global fenêtre
    global quitter
    global largeur
    global hauteur
    global police
    paramètres = 1
    while paramètres == 1 and quitter == 0:
        affichage_paramètre()
        for evenement in event.get():
            if evenement.type == MOUSEBUTTONDOWN:
                if evenement.button == 1:
                    #verification des bouton des parametres
                    pos = evenement.pos
                    if verif_bouton(pos,50,50,150,50)==1:
                        zoom = 0.6
                        changement_zoom()
                    if verif_bouton(pos,50,125,150,50)==1:
                        zoom = 0.8
                        changement_zoom()
                    if verif_bouton(pos,50,200,150,50)==1:
                        zoom = 1
                        changement_zoom()
                    if verif_bouton(pos,250,50,150,50)==1:
                        largeur,hauteur = 10,10
                        affichage_paramètre()
                    if verif_bouton(pos,250,125,150,50)==1:
                        largeur,hauteur = 100,100
                        affichage_paramètre()
                    if verif_bouton(pos,250,200,150,50)==1:
                        largeur,hauteur = 1000,1000
                        affichage_paramètre()
                    if verif_bouton(pos,50,400,150,50)==1:
                        paramètres = 0
            if evenement.type == KEYDOWN:
                if evenement.key == K_ESCAPE:
                    paramètres = 0
            if evenement.type == QUIT:
                quit()
                quitter = 1
                paramètres = 0


def niveaux():
    global position_joueur
    global nb_cassette
    global monstres
    global quitter
    global terrain
    global timer
    niveau = 1
    while niveau == 1 and quitter == 0:
        affichage_niveaux()
        for evenement in event.get():
            if evenement.type == QUIT:
                niveau = 0
                quitter = 1
            if evenement.type == MOUSEBUTTONDOWN:
                if evenement.button == 1:
                    pos = evenement.pos
                    if verif_bouton(pos,50,50,150,50)==1:
                        création_niveaux()
                        timer = timer_niveau_1+time()
                        position_joueur = [4,4]
                        nb_cassette = 0
                        monstres = monstres_niveau_1
                        terrain = niveau_1
                        exploration()
                    if verif_bouton(pos,50,125,150,50)==1:
                        création_niveaux()
                        timer = timer_niveau_2+time()
                        position_joueur = [0,0]
                        nb_cassette = 0
                        monstres = monstres_niveau_2
                        terrain = niveau_2
                        exploration()
                    if verif_bouton(pos,50,200,150,50)==1:
                        pass
                    if verif_bouton(pos,50,275,150,50)==1:
                        pass
                        #position_joueur = [5,5]
                        #nb_cassette = 0
                        # exploration(niveau4)
                    if verif_bouton(pos,225,50,150,50)==1:
                        pass
                        #position_joueur = [5,5]
                        #nb_cassette = 0
                        #exploration(niveau5)
                    if verif_bouton(pos,50,400,150,50)==1:
                        niveau = 0

def affichage_niveaux():
    animation_menu()
    bouton(50*zoom,50*zoom,"Niveau 1")
    bouton(50*zoom,125*zoom,"Niveau 2")
    bouton(50*zoom,200*zoom,"Niveau 3")
    bouton(50*zoom,275*zoom,"Niveau 4")
    bouton(225*zoom,50*zoom,"Niveau 5")
    bouton(50*zoom,400*zoom,"Quitter")
    display.flip()

def affichage_menu():
    animation_menu()
    bouton(50*zoom,50*zoom,"Niveaux")
    bouton(50*zoom,125*zoom,"Exploration")
    bouton(50*zoom,200*zoom,"Pramètres")
    display.flip()

#génération de la page de paramètre
def affichage_paramètre():
    global fenêtre 
    global largeur
    global hauteur
    animation_menu()
    text = police.render("Taille écran",1,blanc)
    fenêtre.blit(text, (70*zoom+dec_x, 15*zoom+dec_y))
    text = police.render("Taille carte",1,blanc)
    fenêtre.blit(text, (270*zoom+dec_x, 15*zoom+dec_y))
    #veriffication de quel bouton est activé
    if (largeur,hauteur) == (10,10):
        taille = 0
    elif (largeur,hauteur) == (100,100):
        taille = 1
    elif (largeur,hauteur) == (1000,1000):
        taille = 2
    x = 15*zoom+dec_x
    if zoom == 0.6:
        y = 65*zoom+dec_y
    elif zoom == 0.8:
        y = 140*zoom+dec_y
    elif zoom == 1:
        y = 215*zoom+dec_y
    draw.rect(fenêtre,blanc,Rect(x,y,20*zoom,20*zoom))
    draw.rect(fenêtre,blanc,Rect(215*zoom+dec_x,(65+taille*75)*zoom+dec_y,20*zoom,20*zoom))
    bouton(50*zoom,400*zoom,"Quitter")
    bouton(50*zoom,50*zoom,"551x592")
    bouton(50*zoom,125*zoom,"735x790")
    bouton(50*zoom,200*zoom,"919x987")
    bouton(250*zoom,50*zoom,"petite")
    bouton(250*zoom,125*zoom,"moyenne")
    bouton(250*zoom,200*zoom,"grande")
    display.flip()


def création_niveaux():
    global niveau_2
    global timer_niveau_2
    global monstres_niveau_2
    global niveau_1
    global timer_niveau_1
    global monstres_niveau_1
    #niveau1[x][y][...]0 = mur en haut, 1 = mur à droite, 2 = mur en bas, 3 = mur à gauche 4 = cassette
    niveau_1 = [[[2,2,1,2,1],[1,2,1,2,0],[1,2,1,2,0],[1,1,2,2,0],[2,1,2,2,0],[2,2,1,2,1],[1,1,2,2,0],[2,1,1,2,0],[1,2,1,2,0],[1,1,2,2,0]],
               [[2,1,1,2,0],[1,1,2,2,0],[2,1,1,2,0],[1,2,2,1,0],[2,1,1,1,0],[1,2,1,2,0],[1,2,2,1,0],[2,1,2,1,0],[2,1,2,2,1],[2,1,2,1,0]],
               [[2,2,1,1,0],[1,2,1,1,0],[1,1,2,1,0],[2,1,1,2,1],[1,1,2,1,0],[2,1,1,2,0],[1,1,1,2,0],[1,2,2,1,0],[2,1,2,1,0],[2,1,2,1,0]],
               [[2,1,2,2,1],[2,1,2,2,0],[2,2,1,1,0],[1,2,2,1,0],[2,1,2,1,0],[2,2,2,1,1],[2,2,1,1,0],[1,1,2,2,0],[2,1,2,1,0],[2,1,2,1,0]],
               [[2,1,1,1,0],[1,2,1,1,0],[1,2,1,2,0],[1,2,1,2,0],[1,1,1,1,2],[1,2,1,2,0],[1,2,1,2,0],[1,2,2,1,0],[2,1,2,1,0],[2,1,2,1,0]],
               [[2,2,1,1,0],[1,1,1,2,0],[1,1,1,2,0],[1,1,2,2,0],[2,1,2,1,0],[2,1,1,2,0],[1,2,1,2,0],[1,1,1,2,0],[1,1,2,1,0],[2,1,2,1,0]],
               [[2,1,1,2,0],[1,2,1,1,0],[1,2,1,1,0],[1,1,2,1,0],[2,1,1,1,0],[1,1,2,1,0],[2,1,2,2,0],[2,1,1,1,0],[1,1,2,1,0],[2,1,2,1,0]],
               [[2,1,1,1,0],[1,2,1,2,0],[1,2,1,2,0],[1,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0],[2,2,2,1,0],[2,1,1,1,1],[1,1,2,1,0],[2,1,2,1,0]],
               [[2,1,2,1,0],[2,2,1,2,1],[1,1,2,2,0],[2,1,2,1,0],[2,1,2,1,0],[2,1,1,1,0],[1,2,1,2,0],[1,2,1,1,0],[1,2,2,1,0],[2,1,2,1,0]],
               [[2,2,1,1,0],[1,2,1,2,0],[1,2,2,1,0],[2,2,1,1,0],[1,2,2,1,0],[2,2,1,1,0],[1,2,1,2,0],[1,2,1,2,1],[1,2,2,2,0],[2,2,2,1,1]]]

    timer_niveau_1 = 180
    monstres_niveau_1 = [[7,8]]

    #niveau1[x][y][...]0 = mur en haut, 1 = mur à droite, 2 = mur en bas, 3 = mur à gauche 4 = cassette
    niveau_2 = [[[2,1,1,2,2],[1,1,1,2,0],[1,1,1,2,0],[1,1,1,2,0],[1,1,1,2,0],[1,1,1,2,0],[1,1,1,2,0],[1,1,1,2,0],[1,1,1,2,0],[1,1,2,2,0]],
           [[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0]],
           [[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0]],
           [[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0]],
           [[2,1,2,1,1],[2,1,2,1,1],[2,1,2,1,1],[2,1,2,1,1],[2,1,2,1,1],[2,1,2,1,1],[2,1,2,1,1],[2,1,2,1,1],[2,1,2,1,1],[2,1,2,1,1]],
           [[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0]],
           [[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0]],
           [[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0]],
           [[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0],[2,1,2,1,0]],
           [[2,2,1,1,0],[1,2,1,1,0],[1,2,1,1,0],[1,2,1,1,0],[1,2,1,1,0],[1,2,1,1,0],[1,2,1,1,0],[1,2,1,1,0],[1,2,1,1,0],[1,2,2,1,0]]]
    
    timer_niveau_2 = 100
    monstres_niveau_2 = [[9,0],[9,2],[9,4],[9,6],[9,8]]

#variable pour quitter le programme
quitter = 0

#variables pour l'animation du menu
durée_animation_bonhomme = 1 #secondes
durée_animation_facade = 3 #secondes
durée_animation_lampadaire = 1.95 #secondes
durée_animation_flame_lampadaire = 0.2
temps_bonhomme = time()
temps_facade = time()
temps_lampadaire = time()
temps_flame_lampadaire = time()
temps_suppression_mur = time() - 60
temps_monstres = time()


#taille du terrain
largeur = 100
hauteur = 100

#variable pour savoir si le terrain est généré
terrain_généré = 0

#taille de l'écran
zoom = 0.8 

largeur_écran = 919
hauteur_écran = 815

#initialisation de la fenêtre
init()
fenêtre = display.set_mode((largeur_écran*zoom,hauteur_écran*zoom))
display.set_caption("Backroom")

#importation des images
warning = image.load("./images/warning.png")
warning = transform.scale(warning,(919*zoom,815*zoom))
cassette = image.load("./images/cassette.png")
cassette = transform.scale(cassette,(40*zoom,20*zoom))
monstre = image.load("./images/monstre.png")
monstre = transform.scale(monstre,(80*zoom,80*zoom))
télé = image.load("./images/télé.png")
télé = transform.scale(télé,(919*zoom,818*zoom))
facade = image.load("./images/facade.jpg")
facade = transform.scale(facade,(int(919*0.5*zoom),int(1024*0.5*zoom)))
personnage = np.zeros(8,dtype=object)#liste de zero de type objet et non float
lampadaire_double = np.zeros(4,dtype=object)#liste de zero de type objet et non float
for numero in range(8):
    personnage[numero] = image.load("./images/image bonhomme qui court "+str(numero+1)+".png").convert_alpha()
    personnage[numero] = transform.scale(personnage[numero], (31*3*zoom,61*3*zoom)).convert_alpha()
for numero in range(4):
    lampadaire_double[numero] = image.load("./images/lampadaire-"+str(numero)+".png").convert_alpha()
    lampadaire_double[numero] = transform.scale(lampadaire_double[numero], (114*zoom,213*zoom)).convert_alpha()


#decalage pour la télé
dec_x = 109*zoom
dec_y = 145*zoom

#couleur des éléments
couleur_sol = (255,230,100)
couleur_mur = (220,180,70)
couleur_joueur = (255,255,0)
blanc = (255,255,255)
noir = (0,0,0)
gris = (150,150,150)
bleu = (0,0,80)

orientation_joueur = 1      #0=haut 1=droite 2=bas 3=gauche

#police d'écriture
police= font.Font(None, int(30*zoom))

mixer.init()
mixer.music.load("musiques/Musique d'horreur.mp3")
mixer.music.play(100)


fenêtre.blit(warning,(0,0))
display.flip()
sleep(3)
menu()
