from Algo_Dichotomie import *

class Bateau:
    def __init__(self, nom, masse, boat, gravite):
        self.__nom = nom
        self.__masse = masse
        self.__boat = boat
        self.__gravite = gravite
        self.__mesh = mesh.Mesh.from_file(self.__boat)
    def getNom(self):
        return self.__nom
    def getMasse(self):
        return self.__masse
    def getCoque(self):
        return self.__boat
    def getGravite(self):
        return self.__gravite
    def getMesh(self):
        return self.__mesh
    def translaZ(self,choixtransla):
        for i in self.__mesh.vectors:
            for y in i:
                y[2] = y[2] + choixtransla

# #Tests
# tonnerre = Bateau("PetitTonerre",100,'Cylindrical_HULL.stl',9)
# print(CalculF(tonnerre.getMesh().vectors[0]))
# print(CalculF([[0,0,0],[1,0,0],[0,1,0]]))
# print(CalculF([[0,0,-1],[1,0,-1],[0,1,-1]])) #On s'attends a pression/2
#
# #Test calcul DS
# a = [1,0,0]
# b = [0,1,0]
# print(CalculPousseeArchimede(tonnerre,0))
# print(CalculDS(a,b))
