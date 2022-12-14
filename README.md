# Landslide Susceptibility Model - Frequency Ratio Method

Landslide Susceptibility model generates landslide susceptibility as a raster layer based on six landslide causative factors.
These include slope, aspect, relative relief, curvature as raster layers and lithology and geomorphology as vector layers.  
In addition to these layers, the study area boundary (polygon) and historical landslide data (points) are required for the analysis. 
The following scripts were written in Python and can be run through the Python console in QGIS. Users can modify the raster cell size 
and the classification parameters based on the study area.


Prerequisities
  1) Slope
  2) Aspect
  3) Relative relief
  4) Curvature
  5) Lithology
  6) Geomorphology
  7) Historical landslide points
  8) Study area boundary

Note: The raster and vector datasets should be located in one folder before processing. All the layers should have the same projection.

The model consists of three parts.
1) Part A - Preprocessing of the layers
2) Part B - Computing the frequency ratio
3) Part C - Deriving the landslide susceptibility raster

