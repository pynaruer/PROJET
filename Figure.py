from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot

"""source : https://w.wol.ph/2015/07/10/rendering-stl-files-matplotlib-numpy-stl/"""
class Figure:
    def __init__(self,point1,point2,point3):
        self.__point1 = point1
        self.__point2 = point2
        self.__point3 = point3

# Create a new plot
figure = pyplot.figure()
axes = mplot3d.Axes3D(figure)
#Load the STL files and add the vectors to the plot
your_mesh = mesh.Mesh.from_file('Rectangular_HULL.stl')
axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))
#Auto scale to the mesh size
scale = your_mesh.points.flatten("C")
axes.auto_scale_xyz(scale, scale, scale)
#Show the plot to the screen
#pyplot.show()
