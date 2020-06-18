from PySide2.QtWidgets import *
from PySide2.QtGui import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot

class Figure:
    def __init__(self,point1,point2,point3):
        self.__point1 = point1
        self.__point2 = point2
        self.__point3 = point3
figure = pyplot.figure()
axes = mplot3d.Axes3D(figure)
your_mesh = mesh.Mesh.from_file('Rectangular_HULL.stl')
axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))
scale = your_mesh.points.flatten("C")
axes.auto_scale_xyz(scale, scale, scale)

class Interface(QWidget):
    def __init__(self,boat):
        QWidget.__init__(self)
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
        self.button_1.clicked.connect(self.start_simulation(boat))

        self.setLayout(self.layout)

    #Signaux
    def start_simulation(self,boat):
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
        your_mesh = mesh.Mesh.from_file(boat)
        axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))
        scale = your_mesh.points.flatten("C")
        axes.auto_scale_xyz(scale, scale, scale)
        self.canvas.draw()
        self.layout.addWidget(self.canvas,2,0,4,4)

    def exit(self):
        window_2.close()
