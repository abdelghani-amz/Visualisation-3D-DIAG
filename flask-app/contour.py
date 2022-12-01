from vtkmodules.vtkFiltersCore import (
    vtkDecimatePro,
    vtkTriangleFilter
)
from vtkmodules.vtkIOXML import (
    vtkXMLPolyDataWriter
)

from vtkmodules.vtkFiltersGeneral import (
    vtkDiscreteFlyingEdges3D
)

from vtkmodules.vtkIOImage import vtkNIFTIImageReader

def read_volume(file_name):
    """
    :param file_name: The filename of type 'nii.gz'
    :return: vtkNIFTIImageReader (https://www.vtk.org/doc/nightly/html/classvtkNIFTIImageReader.html)
    """
    reader = vtkNIFTIImageReader()
    reader.SetFileName(file_name)
    reader.Update()
    return reader


def decimate(inputPolys, triangles , decimator):
    triangles.SetInputConnection(inputPolys)
    triangles.Update()

    decimator.SetInputConnection(triangles.GetOutputPort())
    decimator.SetTargetReduction(0.8)
    decimator.PreserveTopologyOn()
    decimator.Update()

    return decimator.GetOutputPort()


def render(file_name, dir):

    reader = read_volume(file_name)
    image = reader.GetOutputPort()

    surface = vtkDiscreteFlyingEdges3D()
    surface.SetInputConnection(image)
    surface.GenerateValues(1, 1, 1)
    surface.Update()
    lung1 = (surface.GetOutputPort())

    surface2 = vtkDiscreteFlyingEdges3D()
    surface2.SetInputConnection(image)
    surface2.GenerateValues(1, 2, 2)
    surface2.Update()
    lung2 = (surface2.GetOutputPort())

    surface3 = vtkDiscreteFlyingEdges3D()
    surface3.SetInputConnection(image)
    surface3.GenerateValues(1, 3, 3)
    surface3.Update()
    lung3 = (surface3.GetOutputPort())

    triangles = vtkTriangleFilter() ; triangles2 = vtkTriangleFilter() ; triangles3 = vtkTriangleFilter() 
    decimatePro = vtkDecimatePro() ; decimatePro2 = vtkDecimatePro() ; decimatePro3 = vtkDecimatePro() 

    writer1 = vtkXMLPolyDataWriter()
    writer1.SetFileName(dir + "red.vtp")
    writer1.SetInputConnection(decimate(lung1, triangles, decimatePro))
    writer1.Write()

    writer2 = vtkXMLPolyDataWriter()
    writer2.SetFileName(dir + "green.vtp")
    writer2.SetInputConnection(decimate(lung2, triangles2, decimatePro2))
    writer2.Write()

    writer3 = vtkXMLPolyDataWriter()
    writer3.SetFileName(dir + "blue.vtp")
    writer3.SetInputConnection(decimate(lung3, triangles3, decimatePro3))
    writer3.Write()





