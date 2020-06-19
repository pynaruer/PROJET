from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot

def dicho(FP,bateau):
    zga = -25   #Valeur minimale estimée de la potentielle valeur du tirant d'eau (avec de la marge au cas où)
    zgb = 0   #On pourrait prendre d'autres valeurs mais la position d'équilibre est forcément inférieure à 0
    epsilon = 0.01  #Valeur à partir de la quelle on considère que la résultante est nulle si elle a une valeur inférieur à celle-ci
    zgmactuel = 0
    listreturn = []
    xreturn = []
    index = 0

    while True:
        ancienzgm = zgmactuel    #On a besoin de connaitre la position précédente pour savoir de combien doit translater le bateau
        zgmactuel = (zga+zgb) / 2
        resultat = CalculPousseeArchimede(bateau,zgmactuel - ancienzgm)    #on translate seulement de la différence des positions pour arriver à la position souhaitée
        phi = resultat - FP
        if abs(phi) < epsilon:    #Cas 1 : la résultante des forces est nulle à epsilon près, on est à la position d'équilibre
            return -zga,listreturn,xreturn     #on retourne donc le tirant d'eau, la liste avec toute les positions pour afficher graphiquement les points de la dichotomie et le nombre d'itérations
        elif phi >= 0:    #Cas 2 : la résulante n'est pas nulle et supérieure à 0, le bateau est donc trop immergé, on réduit les recherches entre zgb et zgmactuel
            zga = zgmactuel
            listreturn.append(zga)
        else:      #Cas 3 : la résultante n'est pas nulle et inférieure à 0, le bateau n'est donc pas assez immergé, on réduit les recherches entre zga et zgmactuel
            zgb = zgmactuel
            listreturn.append(zgb)
        xreturn.append(index)  #on créé une liste qui retourne [0,1,2,3, etc ...] pour savoir le nombre d'itération pour créer l'axe des abscisses avec cette liste
        index +=1

#Calcul du vecteur DS d'une facette à partir de AB et AC
def CalculDS(A,B):
    resultat = []

    for i in range(3):  #effectue vecteur AB vectoriel vecteur AC le tout divisé par 2 pour obtenir DS
        resultat.append((A[(i+1) % 3]*B[(i+2) % 3] - A[(i+2) % 3]*B[(i+1) % 3]) /2)

    return resultat

#Calcul de la force de pression sur une facette imergée
def CalculF(Coordonee):
    rho = 1025
    g = 9.81

    #calcul des vecteurs AB et AC (On a des listes dans la liste de coordonnée d'où ces indices)
    AB = [Coordonee[1][0]-Coordonee[0][0], Coordonee[1][1]-Coordonee[0][1], Coordonee[1][2]-Coordonee[0][2]]
    AC = [Coordonee[2][0]-Coordonee[0][0], Coordonee[2][1]-Coordonee[0][1], Coordonee[2][2]-Coordonee[0][2]]
    Z = float((Coordonee[0][2]+Coordonee[1][2]+Coordonee[2][2])/3)  #calcul de la coordonnée Z du milieu de la facette
    F = CalculDS(AB,AC)  #en m^2
    pression_pascal = rho*g*Z

    for i in range (len(F)):
        F[i] *= pression_pascal  #en N

    return F  #retourne le vecteur Force de pression sur une facette

#Fonction pour trouver a partir des deux points le point sur la droite qui a Z = 0
def PointAuNiveauDeLeauSurLaDroite(A,B):   #On utilise les équations paramétriques de la droite portée par les 2 points donnés (on les trouve avec les coordonnées des 2 points fournis)
    AB = [B[0]-A[0],B[1]-A[1],B[2]-A[2]]  #Calcul du vecteur AB
    t = float(-A[2]/AB[2])    #On cherche t tel que z=0 (par exemple on a x(t)= 2t, y(t)= 2+t, z(t)= 4-t on a donc t=-Coordonnée de A /Coordonnée 2 du vecteur AB)
    PointEnZ0 = [A[0]+AB[0]*t, A[1]+AB[1]*t, A[2]+AB[2]*t]  #A partir des équations paramétriques et t on trouve le point correspondant
    return PointEnZ0

def CalculPousseeArchimede(bateau,Translation):  #On prend comme argument le bateau et la position voulue
    PousseArchimede = [0,0,0]
    bateau.translaZ(Translation)   #On effectue un translation de X m selon Z

    for i in bateau.getMesh().vectors:  #On parcourt la liste des facettes (chaque élément de cette liste est une facette et chaque facette est une liste qui contient 3 listes qui correspondent aux 3 coordonnées des sommets)
        if i[0][2] < 0 and i[1][2] < 0 and i[2][2] < 0 :  #Cas ou la facette est totalement immergée
            x=CalculF(i)
            for n in range(len(PousseArchimede)) :
                PousseArchimede[n] = PousseArchimede[n] + x[n]
        elif i[0][2] < 0 or i[1][2] < 0 or i[2][2] < 0 :  #Cas ou la facette est semi-immergée
    #Cas 1 : si A est sous l'eau a chaque fois
            if i[0][2] < 0 and i[1][2] >= 0 and i[2][2] >= 0 :  #Sous-cas 1 : A est le seul sommet immergé
                ABen0 = PointAuNiveauDeLeauSurLaDroite(i[0],i[1])  #On calcule le point en Z=0 sur le segment AB
                ACen0 = PointAuNiveauDeLeauSurLaDroite(i[0],i[2])  #On calcule le point en Z=0 sur le segment AC
                NouvelleCoordonnee = [i[0],ABen0,ACen0]  #Il ne reste plus qu'à créer la facette immergée avec ces deux points en Z0 et A
                x = CalculF(NouvelleCoordonnee)  #On calcule la force sur cette nouvelle facette imergée (le reste de la facette est inintéressante car elle est en dehors de l'eau)
                for n in range(len(PousseArchimede)) :
                    PousseArchimede[n] = PousseArchimede[n] + x[n]
            elif  i[0][2] < 0 and i[1][2] < 0 :  #Sous-cas 2 : A et B sont immergés
                ACen0 = PointAuNiveauDeLeauSurLaDroite(i[0],i[2])  #On calcule le point en Z=0 sur le segment AC
                BCen0 = PointAuNiveauDeLeauSurLaDroite(i[1],i[2])  #On calcule le point en Z=0 sur le segment BC
                PremierDecoupage = [i[0],i[1],BCen0]  #Etant donné qu'on a deux sommets immérgés, nous avons une surface trapèzique que l'on découpe en 2 facettes pour pouvoir calculer la force de pression
                DeuxiemeDecoupage = [i[0],ACen0,BCen0]
                x=CalculF(PremierDecoupage)  #On calcule la force sur ces deux facettes imergées
                y=CalculF(DeuxiemeDecoupage)
                for n in range(len(PousseArchimede)) :
                    PousseArchimede[n] = PousseArchimede[n] + x[n] + y[n]
            elif i[0][2] < 0 and i[2][2] < 0 :  #Sous-cas 3 : A et C sont immergés
                ABen0 = PointAuNiveauDeLeauSurLaDroite(i[0],i[1])  #On calcule le point en Z=0 sur le segment AB
                BCen0 = PointAuNiveauDeLeauSurLaDroite(i[1],i[2])  #On calcule le point en Z=0 sur le segment BC
                PremierDecoupage = [i[0],i[2],BCen0]  #Etant donné qu'on a deux sommets immérgés, nous avons une surface trapèzique que l'on découpe en 2 facettes pour pouvoir calculer la force de pression
                DeuxiemeDecoupage = [i[0],ABen0,BCen0]
                x=CalculF(PremierDecoupage) #On calcule la force sur ces deux facettes imergées
                y=CalculF(DeuxiemeDecoupage)
                for n in range(len(PousseArchimede)) :
                    PousseArchimede[n] = PousseArchimede[n] + x[n] + y[n]
    #Cas 2 : si B est sous l'eau à chaque fois
            if i[1][2] < 0 and i[0][2] >= 0 and i[2][2] >= 0 :  #Sous-cas 1 : B est le seul sommet immergé
                ABen0 = PointAuNiveauDeLeauSurLaDroite(i[0],i[1])  #On calcule le point en Z=0 sur le segment AB
                BCen0 = PointAuNiveauDeLeauSurLaDroite(i[1],i[2])  #On calcule le point en Z=0 sur le segment BC
                NouvelleCoordonnee = [i[1],ABen0,BCen0]   #Il ne reste plus qu'à créer la facette immergée avec ces deux points en Z0 et B
                x = CalculF(NouvelleCoordonnee)  #On calcule la force sur cette nouvelle facette imergée (le reste de la facette est inintéressante car elle est en dehors de l'eau
                for n in range(len(PousseArchimede)) :
                    PousseArchimede[n] = PousseArchimede[n] + x[n]
            elif  i[1][2] < 0 and i[0][2] < 0 :  #Sous-cas 2 : B et A sont immergés
                ACen0 = PointAuNiveauDeLeauSurLaDroite(i[0],i[2])  #On calcule le point en Z=0 sur le segment AC
                BCen0 = PointAuNiveauDeLeauSurLaDroite(i[1],i[2])  #On calcule le point en Z=0 sur le segment BC
                PremierDecoupage = [i[0],i[1],ACen0]  #Etant donné qu'on a deux sommets immérgés, nous avons une surface trapèzique que l'on découpe en 2 facettes pour pouvoir calculer la force de pression
                DeuxiemeDecoupage = [i[0],ACen0,BCen0]
                x=CalculF(PremierDecoupage) #On calcule la force sur ces deux facettes imergées
                y=CalculF(DeuxiemeDecoupage)
                for n in range(len(PousseArchimede)) :
                    PousseArchimede[n] = PousseArchimede[n] + x[n] + y[n]
            elif i[1][2] < 0 and i[2][2] < 0 :  #Sous-cas 3 : B et C sont immergés
                ABen0 = PointAuNiveauDeLeauSurLaDroite(i[0],i[1])  #On calcule le point en Z=0 sur le segment AB
                ACen0 = PointAuNiveauDeLeauSurLaDroite(i[0],i[2])  #On calcule le point en Z=0 sur le segment AC
                PremierDecoupage = [i[1],i[2],ACen0]  #Etant donné qu'on a deux sommets immérgés, nous avons une surface trapèzique que l'on découpe en 2 facettes pour pouvoir calculer la force de pression
                DeuxiemeDecoupage = [i[1],ACen0,ABen0]
                x=CalculF(PremierDecoupage) #On calcule la force sur ces deux facettes imergées
                y=CalculF(DeuxiemeDecoupage)
                for n in range(len(PousseArchimede)) :
                    PousseArchimede[n] = PousseArchimede[n] + x[n] + y[n]
    #Cas 3 : si C est sous l'eau à chaque fois
            if i[2][2] < 0 and i[1][2] >= 0 and i[0][2] >= 0 :  #Sous-cas 1 : C est le seul sommet immergé
                BCen0 = PointAuNiveauDeLeauSurLaDroite(i[1],i[2])  #On calcule le point en Z=0 sur le segment BC
                CAen0 = PointAuNiveauDeLeauSurLaDroite(i[0],i[2])  #On calcule le point en Z=0 sur le segment CA
                NouvelleCoordonnee = [i[2],BCen0,CAen0]   #Il ne reste plus qu'à créer la facette immergée avec ces deux points en Z0 et C
                x = CalculF(NouvelleCoordonnee)  #On calcule la force sur cette nouvelle facette imergée (le reste de la facette est inintéressante car elle est en dehors de l'eau
                for n in range(len(PousseArchimede)) :
                    PousseArchimede[n] = PousseArchimede[n] + x[n]
            elif  i[2][2] < 0 and i[1][2] < 0 :  #Sous-cas 2 : C et B sont immergés
                ACen0 = PointAuNiveauDeLeauSurLaDroite(i[0],i[2])   #On calcule le point en Z=0 sur le segment AC
                ABen0 = PointAuNiveauDeLeauSurLaDroite(i[0],i[1])   #On calcule le point en Z=0 sur le segment AB
                PremierDecoupage = [i[1],i[2],ABen0]  #Etant donné qu'on a deux sommets immérgés, nous avons une surface trapèzique que l'on découpe en 2 facettes pour pouvoir calculer la force de pression
                DeuxiemeDecoupage = [i[2],ACen0,ABen0]
                x=CalculF(PremierDecoupage) #On calcule la force sur ces deux facettes imergées
                y=CalculF(DeuxiemeDecoupage)
                for n in range(len(PousseArchimede)) :
                    PousseArchimede[n] = PousseArchimede[n] + x[n] + y[n]
            elif i[2][2] < 0 and i[0][2] < 0 :   #Sous-cas 3 : C et A sont immergés
                ABen0 = PointAuNiveauDeLeauSurLaDroite(i[0],i[1])  #On calcule le point en Z=0 sur le segment AB
                BCen0 = PointAuNiveauDeLeauSurLaDroite(i[1],i[2])  #On calcule le point en Z=0 sur le segment BC
                PremierDecoupage = [i[0],i[2],ABen0]  #Etant donné qu'on a deux sommets immérgés, nous avons une surface trapèzique que l'on découpe en 2 facettes pour pouvoir calculer la force de pression
                DeuxiemeDecoupage = [i[2],ABen0,BCen0]
                x=CalculF(PremierDecoupage) #On calcule la force sur ces deux facettes imergées
                y=CalculF(DeuxiemeDecoupage)
                for n in range(len(PousseArchimede)) :
                    PousseArchimede[n] = PousseArchimede[n] + x[n] + y[n]

    return PousseArchimede[2]

class Bateau:
    def __init__(self,profondeur,masse,coque,gravite):
        self.__profondeur = profondeur
        self.__masse = masse
        self.__coque = coque
        self.__gravite = gravite
        self.__mesh = mesh.Mesh.from_file(self.__coque)

    def getProfondeur(self):
        return self.__profondeur
    def getPoids(self):
        return (self.__masse * 9.81)
    def getCoque(self):
        return self.__coque
    def getMesh(self):
        return self.__mesh
    def getGravite(self):
        return self.__gravite
    def translaZ(self,choixtransla):
        for i in self.__mesh.vectors:
            for y in i:
                y[2] = y[2] + choixtransla #On parcourt la liste des coordonnées des sommets de facettes et on ajoute à la coordonnée Z la valeur de transalation voulue


#Tests
#tonnerre = Bateau("PetitTonerre",100,'Rectangular_HULL.stl',9.81)
#print(CalculDS([-3,7,4],[1,8,3])) #test CalculDS : affiche théoriquement [-5.5, 6.5, -15.5]
#print(CalculDS([-23,63,-8],[12,40,-44])) #2eme test de CalculDS : affiche théoriquement [-1226, -554, -838]
#print(CalculF([[4,2,3],[1,9,7],[5,10,6]])) #test CalculF : affiche théoriquement [-294954, 348582, -831234]
#print(CalculF([[20,-34,12],[-3,29,4],[32,6,-32]])) #2eme test de CalculF : affiche théoriquement [65747928, 29602656, 44940264]
#print(PointAuNiveauDeLeauSurLaDroite([1,3,2],[-5,0,4])) #test PointAuNiveauDeLeauSurLaDroite : affiche théoriquement [7,6,0]
#print(PointAuNiveauDeLeauSurLaDroite([8,5,12],[19,26,38])) #2eme test PointAuNiveauDeLeauSurLaDroite : affiche théoriquement [7,6,0]
#print(CalculPousseeArchimede(tonnerre,-1)) #test CalculPousseeArchimede : affiche théoriquement 80442 N
#print(CalculPousseeArchimede(tonnerre,-0.5)) #2eme test CalculPousseeArchimede : affiche théoriquement 40221 N
#FP=1590.8*9.81 #test dichotomie : affiche théoriquement 0,194
#print(dicho(FP,tonnerre)) #suite du test
#FP=7609.6*9.81 #test dichotomie : affiche théoriquement 0,928
#print(dicho(FP,tonnerre)) #suite du test
