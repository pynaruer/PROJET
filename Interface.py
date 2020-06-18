from PySide2.QtWidgets import *
from PySide2.QtGui import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from mpl_toolkits import mplot3d
from stl import mesh
from Calcul_Final import *
import numpy as np
import time


"""Programme Interface Paramètres"""
class Entry_Box(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.number = 0
        self.__boat = ""
        self.__gravite = 0
        self.setWindowTitle("Position d'équilibre d'un bateau")
        self.setFixedSize(600, 400)
        icon = QIcon("logo.png")
        self.setWindowIcon(icon)

        #Layouts
        self.layout = QVBoxLayout()
        self.layoutProf = QHBoxLayout()
        self.layoutGrav = QHBoxLayout()
        self.layoutEntrees = QHBoxLayout()
        self.layoutBateau1 = QHBoxLayout()
        self.layoutBateau2 = QHBoxLayout()
        self.layoutBateau3 = QHBoxLayout()
        self.layoutBateau4 = QHBoxLayout()
        self.specialLayout = QHBoxLayout()

        #Style
        self.setStyleSheet(open('mystylesheet.css').read())

        #Labels
        self.welcome = QLabel("Bienvenue sur l'interface de calcul de position de bateaux à l'équilibre")
        self.choix1 = QLabel("Veuillez entrez votre choix de gravité : ")
        self.choix2 = QLabel("Veuillez choisir votre bateau : ")
        self.layout.addWidget(self.welcome)
        self.layoutGrav.addWidget(self.choix1)

        #Creation menu déroulant
        self.choose = QComboBox()
        self.choose.addItem("Gravite terrestre") #9.81
        self.choose.addItem("Gravite lunaire") #1.62
        self.choose.addItem("Gravite martienne") #3.71
        self.layoutGrav.addWidget(self.choose)

        #Entree profondeur
        self.entreeprof = QLabel("Veuillez saisir la profondeur (en m) : ")
        self.prof = QDoubleSpinBox()
        self.prof.setMinimum(-999999999)
        self.prof.setMaximum(999999999)

        #Entrée de la masse
        self.entreemasse = QLabel("Entrez la masse du bateau (en kg) : ")
        self.txtenter = QDoubleSpinBox()
        self.txtenter.setMaximum(999999999)
        self.txtenter.setMinimum(1)

        #Organisation des layouts
        self.layoutEntrees.addWidget(self.entreemasse)
        self.layoutEntrees.addWidget(self.txtenter)
        self.layoutProf.addWidget(self.entreeprof)
        self.layoutProf.addWidget(self.prof)

        #Ajout au layout en respectant l'ordre
        self.layout.addLayout(self.layoutEntrees)
        self.layout.addLayout(self.layoutGrav)
        self.layout.addLayout(self.layoutProf)
        self.layout.addWidget(self.choix2)

        self.VHullButton = QRadioButton("  Bateau 1 : V_HULL")
        self.layoutBateau1.addWidget(self.VHullButton)

        self.RectangularButton = QRadioButton("Bateau 2 : Rectangular_HULL")
        self.layoutBateau1.addWidget(self.RectangularButton)

        self.CylButton = QRadioButton("  Bateau 3 : Cylindrical_HULL")
        self.layoutBateau2.addWidget(self.CylButton)

        self.MiniButton = QRadioButton("Bateau 4 : Mini650_HULL")
        self.layoutBateau2.addWidget(self.MiniButton)

        self.AluButton = QRadioButton("  Bateau 5 : BargeAlu_HULL")
        self.layoutBateau3.addWidget(self.AluButton)

        self.ssMarinButton = QRadioButton("Bateau 6 : ssMarin_HULL")
        self.layoutBateau3.addWidget(self.ssMarinButton)

        self.WigleyButton = QRadioButton("  Bateau 7 : Wigley_HULL")
        self.layoutBateau4.addWidget(self.WigleyButton)

        self.newButton = QRadioButton()
        self.specialLayout.addWidget(self.newButton)
        self.txtButton = QLineEdit("Entrez le fichier de votre choix")
        self.specialLayout.addWidget(self.txtButton)

        self.layout.addLayout(self.layoutBateau1)
        self.layout.addLayout(self.layoutBateau2)
        self.layout.addLayout(self.layoutBateau3)
        self.layout.addLayout(self.layoutBateau4)
        self.layout.addLayout(self.specialLayout)



        self.buttonvalidate = QPushButton("Valider")
        self.buttonvalidate.clicked.connect(self.buttonClicked)
        self.layout.addWidget(self.buttonvalidate)

        self.txtErreur = QLabel()
        self.txtErreur2 = QLabel()

        self.setLayout(self.layout)

    #Verification box
    def verification(self):
        userInfo = QMessageBox.question(self,"Confirmation", "Confirmer",QMessageBox.Yes | QMessageBox.No)
        if userInfo == QMessageBox.Yes:
            self.number = 1
            self.close()
        elif userInfo == QMessageBox.No:
            pass

    def buttonClicked(self):
        #Recuperation de la valeur du menu déroulant
        if self.choose.currentText() == "Gravite lunaire":
            self.__gravite = 1.62
        elif self.choose.currentText() == "Gravite martienne":
            self.__gravite = 3.71
        elif self.choose.currentText() == "Gravite terrestre":
            self.__gravite = 9.81

        #Recuperation de la masse
        self.__masse = self.txtenter.value()

        #Recuperation de l'url de l'stl
        self.__boat = self.txtButton.text()

        #Recuperation du choix du fichier stl
        if self.RectangularButton.isChecked() == False and self.VHullButton.isChecked() == False and self.CylButton.isChecked() == False and self.MiniButton.isChecked() == False and self.newButton.isChecked() == False and (self.newButton.isChecked() == False or self.txtButton.text() == "Entrez le fichier de votre choix"):
            self.layout.removeWidget(self.txtErreur)
            self.txtErreur = QLabel("Vous devez choisir un modèle de bateau !")
            self.layout.addWidget(self.txtErreur)

        if self.RectangularButton.isChecked() == True :
            self.layout.removeWidget(self.txtErreur)
            self.__boat = "Rectangular_HULL_Normals_Outward.STL"
            self.verification()

        elif self.VHullButton.isChecked() == True :
            self.layout.removeWidget(self.txtErreur)
            self.__boat = "V_HULL_Normals_Outward.STL"
            self.verification()

        elif self.CylButton.isChecked() == True:
            self.layout.removeWidget(self.txtErreur)
            self.__boat = "Cylindrical_HULL_Normals_Outward.STL"
            self.verification()

        elif self.MiniButton.isChecked() == True:
            self.layout.removeWidget(self.txtErreur)
            self.__boat = "Mini650_HULL_Normals_Outward.STL"
            self.verification()

        elif self.newButton.isChecked() == True:
            self.layout.removeWidget(self.txtErreur)
            self.__boat = str(self.txtButton.text())
            self.verification()

        elif self.ssMarinButton.isChecked() == True:
            self.layout.removeWidget(self.txtErreur)
            self.__boat = "ssmarin_L=4_W=2_H=2_Normals_Outward.STL"
            self.verification()

        elif self.WigleyButton.isChecked() == True:
            self.layout.removeWidget(self.txtErreur)
            self.__boat = "WIGLEY_L=2500_B=250_T=156_NormalOutward2.STL"
            self.verification()

        elif self.AluButton.isChecked() == True:
            self.layout.removeWidget(self.txtErreur)
            self.__boat = "BargeAlu_L_2980_W_633_H_400_NormalOutward2.STL"
            self.verification()

    def getBoat(self):
        return self.__boat
    def getProfondeur(self):
        return self.entreeprof
    def getMasse(self):
        return self.__masse
    def getGravite(self):
        return self.__gravite
    def getNumber(self):
        return self.number

"""Programme interface finale"""
class Interface(QWidget):
    def __init__(self,boat,tirant,listgraph,listx):
        QWidget.__init__(self)
        self.coque = boat.getCoque()
        self.__tirant = tirant
        self.__listgraph = listgraph
        self.__listx = listx
        self.setWindowTitle("Interface Bateau")
        self.layout = QGridLayout()

        #Style
        self.setStyleSheet(open('mystylesheet.css').read())
        self.setFixedSize(600,400)
        icon = QIcon("logo.png")
        self.setWindowIcon(icon)

        #Button
        self.button_1 = QPushButton("Start simulation")
        self.progressbar = QProgressBar()

        self.layout.addWidget(self.button_1)
        self.layout.addWidget(self.progressbar)
        self.progressbar.hide()

        self.button_1.clicked.connect(self.start_simulation)

        self.setLayout(self.layout)

    #Signaux
    def start_simulation(self):
        self.button_1.hide()
        self.progressbar.show()
        for i in range(101):
            self.progressbar.setValue(i)
            time.sleep(0.05)
        self.setFixedSize(1000,550)
        self.progressbar.hide()
        self.button_2 = QPushButton("Exit")
        self.layout.addWidget(self.button_2,8,8,1,1)
        self.button_2.clicked.connect(self.exit)

        #Graphique
        self.fig2 = plt.figure()
        self.graph = FigureCanvas(self.fig2)
        plt.ylim(-4,0)
        plt.plot(self.__listx,self.__listgraph)
        plt.xlabel('Calcul de la position du tirant d\'eau')
        self.graph.draw()
        self.layout.addWidget(self.graph,2,5,4,4)

        #Figure 3D
        self.fig = plt.figure()
        self.canvas = FigureCanvas(self.fig)
        axes = mplot3d.Axes3D(self.fig)
        your_mesh = mesh.Mesh.from_file(self.coque)
        axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))
        scale = your_mesh.points.flatten("C")
        axes.auto_scale_xyz(scale, scale, scale)
        self.canvas.draw()
        self.layout.addWidget(self.canvas,2,0,4,4)

    def exit(self):
        self.close()


if __name__ == "__main__":
    import sys
    app = QApplication([])
    window_1 = Entry_Box()
    window_1.show()
    app.exec_()
    tonnerre = Bateau(window_1.getProfondeur(),window_1.getMasse(),window_1.getBoat(),window_1.getGravite())
    tirant,listgraph,listx = dicho(window_1.getMasse()*window_1.getGravite(),tonnerre)
    if window_1.getNumber() == 1:
        window_2 = Interface(tonnerre,tirant,listgraph,listx)
        window_2.show()
        app.exec_()
        sys.exit()
