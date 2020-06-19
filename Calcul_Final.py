from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot

def dicho(FP,bateau):
    zga = -5
    zgb = 0
    epsilon = 0.01
    zgmactuel = 0
    listreturn = []
    xreturn = []
    index = 0

    while True:
        ancienzgm = zgmactuel
        zgmactuel = (zga+zgb) / 2
        resultat = CalculPousseeArchimede(bateau,zgmactuel - ancienzgm)
        phi = resultat - FP
        if abs(phi) < epsilon:
            return -zga,listreturn,xreturn
        elif phi >= 0:
            zga = zgmactuel
            listreturn.append(zga)
        else:
            zgb = zgmactuel
            listreturn.append(zgb)
        xreturn.append(index)
        index +=1

#Calcul du vecteur DS d'une facette à partir de AB et AC
def CalculDS(A,B):
    resultat = []
    for i in range(3):
        resultat.append((A[(i+1) % 3]*B[(i+2) % 3] - A[(i+2) % 3]*B[(i+1) % 3]) /2)
    return resultat

#Calcul de la force de pression sur une facette imergée
def CalculF(Coordonee): #
    rho = 1025
    g = 9.81
    #calcul des vecteurs AB et AC
    AB = [Coordonee[1][0]-Coordonee[0][0], Coordonee[1][1]-Coordonee[0][1], Coordonee[1][2]-Coordonee[0][2]]
    AC = [Coordonee[2][0]-Coordonee[0][0], Coordonee[2][1]-Coordonee[0][1], Coordonee[2][2]-Coordonee[0][2]]
    Z = float((Coordonee[0][2]+Coordonee[1][2]+Coordonee[2][2])/3)
    F = CalculDS(AB,AC) #m^2
    pression_pascal = rho*g*Z
    for i in range (len(F)):
        F[i] *= pression_pascal #N
    return F

#Fonction pour trouver a partir des deux points le point sur la droite qui a Z = 0
def PointAuNiveauDeLeauSurLaDroite(A,B):
    AB = [B[0]-A[0],B[1]-A[1],B[2]-A[2]]
    t = float(-A[2]/AB[2])
    PointEnZ0 = [A[0]+AB[0]*t, A[1]+AB[1]*t, A[2]+AB[2]*t]
    return PointEnZ0

def CalculPousseeArchimede(bateau,Translation):
    PousseArchimede = [0,0,0]
    #On effectue un translation de X m
    bateau.translaZ(Translation)
    for i in bateau.getMesh().vectors:
        if i[0][2] < 0 and i[1][2] < 0 and i[2][2] < 0 :
            x=CalculF(i)
            for n in range(len(PousseArchimede)) :
                PousseArchimede[n] = PousseArchimede[n] + x[n]
        elif i[0][2] < 0 or i[1][2] < 0 or i[2][2] < 0 : #cas particuliers
    #Si A est sous l'eau a chaque fois
            if i[0][2] < 0 and i[1][2] >= 0 and i[2][2] >= 0 :
                ABen0 = PointAuNiveauDeLeauSurLaDroite(i[0],i[1])
                ACen0 = PointAuNiveauDeLeauSurLaDroite(i[0],i[2])
                NouvelleCoordonnee = [i[0],ABen0,ACen0]
                x = CalculF(NouvelleCoordonnee)
                for n in range(len(PousseArchimede)) :
                    PousseArchimede[n] = PousseArchimede[n] + x[n]
            elif  i[0][2] < 0 and i[1][2] < 0 :
                ACen0 = PointAuNiveauDeLeauSurLaDroite(i[0],i[2])
                BCen0 = PointAuNiveauDeLeauSurLaDroite(i[1],i[2])
                PremierDecoupage = [i[0],i[1],BCen0]
                DeuxiemeDecoupage = [i[0],ACen0,BCen0]
                x=CalculF(PremierDecoupage)
                y=CalculF(DeuxiemeDecoupage)
                for n in range(len(PousseArchimede)) :
                    PousseArchimede[n] = PousseArchimede[n] + x[n] + y[n]
            elif i[0][2] < 0 and i[2][2] < 0 :
                ABen0 = PointAuNiveauDeLeauSurLaDroite(i[0],i[1])
                BCen0 = PointAuNiveauDeLeauSurLaDroite(i[1],i[2])
                PremierDecoupage = [i[0],i[2],BCen0]
                DeuxiemeDecoupage = [i[0],ABen0,BCen0]
                x=CalculF(PremierDecoupage)
                y=CalculF(DeuxiemeDecoupage)
                for n in range(len(PousseArchimede)) :
                    PousseArchimede[n] = PousseArchimede[n] + x[n] + y[n]
    #Si B est sous l'eau à chaque fois
            if i[1][2] < 0 and i[0][2] >= 0 and i[2][2] >= 0 :
                ABen0 = PointAuNiveauDeLeauSurLaDroite(i[0],i[1])
                BCen0 = PointAuNiveauDeLeauSurLaDroite(i[1],i[2])
                NouvelleCoordonnee = [i[1],ABen0,BCen0]
                x = CalculF(NouvelleCoordonnee)
                for n in range(len(PousseArchimede)) :
                    PousseArchimede[n] = PousseArchimede[n] + x[n]
            elif  i[1][2] < 0 and i[0][2] < 0 :
                ACen0 = PointAuNiveauDeLeauSurLaDroite(i[0],i[2])
                BCen0 = PointAuNiveauDeLeauSurLaDroite(i[1],i[2])
                PremierDecoupage = [i[0],i[1],ACen0]
                DeuxiemeDecoupage = [i[0],ACen0,BCen0]
                x=CalculF(PremierDecoupage)
                y=CalculF(DeuxiemeDecoupage)
                for n in range(len(PousseArchimede)) :
                    PousseArchimede[n] = PousseArchimede[n] + x[n] + y[n]
            elif i[1][2] < 0 and i[2][2] < 0 :
                ABen0 = PointAuNiveauDeLeauSurLaDroite(i[0],i[1])
                ACen0 = PointAuNiveauDeLeauSurLaDroite(i[0],i[2])
                PremierDecoupage = [i[1],i[2],ACen0]
                DeuxiemeDecoupage = [i[1],ACen0,ABen0]
                x=CalculF(PremierDecoupage)
                y=CalculF(DeuxiemeDecoupage)
                for n in range(len(PousseArchimede)) :
                    PousseArchimede[n] = PousseArchimede[n] + x[n] + y[n]
    #Si C est sous l'eau à chaque fois
            if i[2][2] < 0 and i[1][2] >= 0 and i[0][2] >= 0 :
                BCen0 = PointAuNiveauDeLeauSurLaDroite(i[1],i[2])
                CAen0 = PointAuNiveauDeLeauSurLaDroite(i[0],i[2])
                NouvelleCoordonnee = [i[2],BCen0,CAen0]
                x = CalculF(NouvelleCoordonnee)
                for n in range(len(PousseArchimede)) :
                    PousseArchimede[n] = PousseArchimede[n] + x[n]
            elif  i[2][2] < 0 and i[1][2] < 0 :
                ACen0 = PointAuNiveauDeLeauSurLaDroite(i[0],i[2])
                ABen0 = PointAuNiveauDeLeauSurLaDroite(i[0],i[1])
                PremierDecoupage = [i[1],i[2],ABen0]
                DeuxiemeDecoupage = [i[2],ACen0,ABen0]
                x=CalculF(PremierDecoupage)
                y=CalculF(DeuxiemeDecoupage)
                for n in range(len(PousseArchimede)) :
                    PousseArchimede[n] = PousseArchimede[n] + x[n] + y[n]
            elif i[2][2] < 0 and i[0][2] < 0 :
                ABen0 = PointAuNiveauDeLeauSurLaDroite(i[0],i[1])
                BCen0 = PointAuNiveauDeLeauSurLaDroite(i[1],i[2])
                PremierDecoupage = [i[0],i[2],ABen0]
                DeuxiemeDecoupage = [i[2],ABen0,BCen0]
                x=CalculF(PremierDecoupage)
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
    def getProfondeur(self): return self.__profondeur
    def getPoids(self): return (self.__masse * 9.81)
    def getCoque(self): return self.__coque
    def getMesh(self): return self.__mesh
    def getGravite(self): return self.__gravite
    def translaZ(self,choixtransla):
        for i in self.__mesh.vectors:
            for y in i:
                y[2] = y[2] + choixtransla


#Tests

#tonnerre = Bateau("PetitTonerre",100,'Rectangular_HULL.stl')
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
