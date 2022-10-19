#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#Landslide susceptibility model ----------- Part A --------- by Shruti Anna Samuel (s3933141)
#Preprocessing the data
#1) Vector to raster data (lithology and geomorphology)
#2) Clipping the rasters with the study area output

#importing the necessary classes
import processing
from processing.core.Processing import Processing
from qgis.core import *
from qgis.utils import iface
from qgis.PyQt.QtCore import QVariant
from osgeo import gdal

#this allows GDAL to throw Python Exceptions
gdal.UseExceptions()

os.chdir("C:\\Users\\Provide_your_filepath_here\\")#Set the directory
#provide the file path and the input file names
filepath = "C:\\Users\\Provide_your_filepath_here\\" 
slp = "slope.tif"#Name of the slope raster data
asp = "aspect.tif"#Name of the aspect raster data
cur = "curvature.tif"#Name of the curvature raster data
rr = "rr.tif"#Name of the relative relief raster data
gm = "geomorphology_prj.shp"#Name of the geomorphology vector data
lith = "lithology_prj.shp"#Name of the Lithology vector data
wyd = "wyd_output.shp"#Name of the study area vector data

#Adding the Wayanad study area in QGIS using iface
wyd_out = iface.addVectorLayer(filepath + wyd, wyd[:-4],"ogr")

#Add the layers in the project using iface.
iface.addVectorLayer(filepath + lith, lith[:-4],"ogr")
iface.addVectorLayer(filepath + gm, gm[:-4],"ogr")
slope = iface.addRasterLayer(filepath + slp, "slope")

#Defining the extent of the raster layers. Any raster layer can be used to get the extent. In this example, I have used the slope raster.
ext = slope.extent()
xmin = ext.xMinimum()
xmax = ext.xMaximum()
ymin = ext.yMinimum()
ymax = ext.yMaximum()
coords = "%f,%f,%f,%f" %(xmin, xmax, ymin, ymax) 

#vector to raster conversion. Lithology and Geomorphology are mostly provided as vector data which has to be converted to raster files.
#vector to raster conversion here is done using the gdal:rasterize processing algorithm.

#lithology vector to lithology raster conversion
lithoraster = 'C:\\Users\\Provide_your_filepath_here\\lithoraster.tif' #output path and filename
params = {'INPUT': filepath + lith,
          'FIELD': 'UID_NOTATI',#Mention the field based on which the raster has to be created.
          'UNITS': '1',
          'WIDTH': '12.5',#Raster cell size
          'HEIGHT': '12.5',#Raster cell size
          'EXTENT': coords,#extent of the raster layer
          'DATA_TYPE': '5',
          'OUTPUT': lithoraster}
processing.run("gdal:rasterize",params)
lithology = QgsRasterFileWriter(lithoraster) #Writing the raster layer
iface.addRasterLayer(lithoraster, "lithoraster") #Adding the raster layer to QGIS


#geomorphology vector to geomorphology raster conversion
georaster = 'C:\\Users\\Provide_your_filepath_here\\geomraster.tif' #output path and filename
params1 = {'INPUT': filepath + gm,
          'FIELD': 'Geom_class',#Mention the field based on which the raster has to be created.
          'UNITS': '1',
          'WIDTH': '12.5',#Raster cell size
          'HEIGHT': '12.5',#Raster cell size
          'EXTENT': coords,#extent of the raster layer
          'DATA_TYPE': '5',
          'OUTPUT': georaster}
processing.run("gdal:rasterize",params1)
geomorphology = QgsRasterFileWriter(georaster)#Writing the raster layer
iface.addRasterLayer(georaster, "geomraster")#Adding the raster layer to QGIS

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#Clipping the rasters to the study area extent


inputfile = []
outputfile = []

#For loop used to iterate the .tif files in the filepath and clip the raster layers. 
for file in os.listdir(filepath):
    if file.endswith(".tif"):
        layer = iface.addRasterLayer((filepath + file), file[:-4])
        inputfile.append(file)
        outputfilename = file[:-4]+'_clipped'+file[-4:]
        parameters = {'INPUT': filepath + file,
                      'MASK': wyd_out,#Study area vector file
                      'NODATA': 9999,
                      'CROP_TO_CUTLINE': True,
                      'KEEP_RESOLUTION': True,
                      'OPTIONS': None,
                      'DATA_TYPE': 0,
                      'OUTPUT': filepath + outputfilename}
        print(parameters)
        processing.runAndLoadResults("gdal:cliprasterbymasklayer",parameters)
    
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
print ('Part A of the landslide susceptibility model is completed. The LCF layers are preprocessed.')
