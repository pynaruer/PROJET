from PySide2.QtWidgets import *
from PySide2.QtGui import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from Figure import *
from mpl_toolkits import mplot3d
from stl import mesh


"""Programme Interface Paramètres"""
class Entry_Box(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.boat = ""
        #self.__gravite = 9.81 #Initiale
        self.__gravite = 0
        self.setWindowTitle("Position d'équilibre d'un bateau")
        self.setMinimumSize(500, 300)

        #Layouts
        self.layout = QVBoxLayout()
        self.layoutEntrees = QHBoxLayout()
        self.layoutBateau1 = QHBoxLayout()
        self.layoutBateau2 = QHBoxLayout()
        self.specialLayout = QHBoxLayout()

        #Labels
        self.welcome = QLabel("Bienvenue sur l'interface de calcul de position de bateaux à l'équilibre")
        self.choix1 = QLabel("Veuillez entrez votre masse (en kg) ainsi que  votre choix de gravité : ")
        self.choix2 = QLabel("Veuillez choisir votre bateau")
        self.layout.addWidget(self.welcome)
        self.layout.addWidget(self.choix1)

        #Creation menu déroulant
        self.choose = QComboBox()
        self.choose.addItem("Gravite terrestre") #9.81
        self.choose.addItem("Gravite lunaire") #1.62
        self.choose.addItem("Gravite martienne") #3.71

        #Entrée de la masse
        self.entreemasse = QLabel("Entrez la masse du bateau (en kg):")
        self.txtenter = QSpinBox()
        self.txtenter.setMaximum(999999999)
        self.txtenter.setMinimum(0)

        #Organisation des layouts
        self.layoutEntrees.addWidget(self.choose)
        self.layoutEntrees.addWidget(self.entreemasse)
        self.layoutEntrees.addWidget(self.txtenter)

        #Ajout au layout en respectant l'ordre
        self.layout.addLayout(self.layoutEntrees)
        self.layout.addWidget(self.choix2)

        self.VHullButton = QRadioButton()
        self.VHullButton.setText("Bateau 1 : V_HULL")
        self.layoutBateau1.addWidget(self.VHullButton)

        self.RectangularButton = QRadioButton()
        self.RectangularButton.setText("Bateau 2 : Rectangular_HULL")
        self.layoutBateau1.addWidget(self.RectangularButton)

        self.CylButton = QRadioButton()
        self.CylButton.setText("Bateau 3 : Cylindrical_HULL")
        self.layoutBateau2.addWidget(self.CylButton)

        self.MiniButton = QRadioButton()
        self.MiniButton.setText("Bateau 4 : Mini650_HULL")
        self.layoutBateau2.addWidget(self.MiniButton)

        self.newButton = QRadioButton()
        self.specialLayout.addWidget(self.newButton)

        self.txtButton = QLineEdit("Entrez le fichier de votre choix")
        self.specialLayout.addWidget(self.txtButton)

        self.layout.addLayout(self.layoutBateau1)
        self.layout.addLayout(self.layoutBateau2)
        self.layout.addLayout(self.specialLayout)

        self.buttonvalidate = QPushButton("Valider")
        self.buttonvalidate.clicked.connect(self.buttonClicked)

        self.txtErreur = QLabel()
        self.txtErreur2 = QLabel()

        self.layout.addWidget(self.buttonvalidate)
        self.layout.addWidget(self.txtErreur2)
        self.layout.addWidget(self.txtErreur)

        self.setLayout(self.layout)

    #Verification box
    def verification(self):
        userInfo = QMessageBox.question(self,"Confirmation", "Confirmer",QMessageBox.Yes | QMessageBox.No)
        if userInfo == QMessageBox.Yes:
            window_1.hide()
            window_2.show()
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
        self.boat = self.txtButton.text()

        #Recuperation du choix du fichier stl
        if self.RectangularButton.isChecked() == False and self.VHullButton.isChecked() == False and self.CylButton.isChecked() == False and self.MiniButton.isChecked() == False and self.newButton.isChecked() == False:
            self.layout.removeWidget(self.txtErreur)
            self.txtErreur = QLabel("Vous devez choisir un modèle de bateau !")
            self.layout.addWidget(self.txtErreur)

        if self.RectangularButton.isChecked() == True :
            self.layout.removeWidget(self.txtErreur)
            self.boat = "Rectangular_HULL_Normals_Outward.STL"
            self.verification()

        elif self.VHullButton.isChecked() == True :
            self.layout.removeWidget(self.txtErreur)
            self.boat = "V_HULL_Normals_Outward.STL"
            self.verification()

        elif self.CylButton.isChecked() == True:
            self.layout.removeWidget(self.txtErreur)
            self.boat = "Cylindrical_HULL_Normals_Outward.STL"
            self.verification()

        elif self.MiniButton.isChecked() == True:
            self.layout.removeWidget(self.txtErreur)
            self.boat = "Mini650_HULL_Normals_Outward.STL"
            self.verification()

        elif self.MiniButton.isChecked() == True:
            self.layout.removeWidget(self.txtErreur)
            self.boat = str(self.txtButton.text())
            self.verification()

    def getBoat(self):
        return self.boat


"""Programme interface finale"""
class Interface(QWidget):
    def __init__(self,boat):
        QWidget.__init__(self)
        self.boat = boat
        self.setWindowTitle("Interface Bateau")
        self.layout = QGridLayout()
        self.setFixedSize(500,300)
        icon = QIcon("bateau")
        self.setWindowIcon(icon)

        #Button
        self.button_1 = QPushButton("Start simulation")
        #self.button_1.setStyleSheet("background-image: url(logo.jpg)")
        self.button_1.setFixedSize(450,273)

        self.layout.addWidget(self.button_1)
        self.button_1.clicked.connect(self.start_simulation)

        self.setLayout(self.layout)

    #Signaux
    def start_simulation(self):
        print(self.boat)
        self.setFixedSize(1000,500)

        self.button_1.hide()

        self.button_2 = QPushButton("Exit")
        self.layout.addWidget(self.button_2,1,8,1,1)
        self.button_2.clicked.connect(self.exit)

        #Graphique
        self.fig2 = plt.figure()
        self.graph = FigureCanvas(self.fig2)
        plt.plot([1,2,3,4])
        plt.xlabel('Calcul de la position du tirant d\'eau')
        self.graph.draw()
        self.layout.addWidget(self.graph,2,5,4,4)

        #Figure 3D
        self.fig = plt.figure()
        self.canvas = FigureCanvas(self.fig)
        axes = mplot3d.Axes3D(self.fig)
        your_mesh = mesh.Mesh.from_file(str(self.boat))
        axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))
        scale = your_mesh.points.flatten("C")
        axes.auto_scale_xyz(scale, scale, scale)
        self.canvas.draw()
        self.layout.addWidget(self.canvas,2,0,4,4)

    def exit(self):
        window_2.close()



if __name__ == "__main__":
    import sys
    app = QApplication([])
    window_1 = Entry_Box()
    window_2 = Interface(window_1.getBoat())
    window_2.hide()
    window_1.show()
    app.exec_()
    sys.exit()
