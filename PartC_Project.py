#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#Landslide susceptibility model ----------- Part C --------- by Shruti Anna Samuel (s3933141)
#Creating the weighted sum of the rasters
#1) Reclassification the layers based on the frequency ratio  values.
#2) Find the final landslide susceptibility using the raster claculator. 


#reclassify by table
#Adding the reclassified layers
filepath = "C:\\Users\\Anna\\Documents\\assignments\\geospatial_programming\\project\\"

Reclassslp = "slope_reclass.tif"
Reclassasp = "aspect_reclass.tif"
Reclasscur = "curv_reclass.tif"
Reclassrr = "rr_reclass.tif"
Reclassgm = "geomraster_clipped.tif"
Reclasslith = "lithoraster_clipped.tif"
lspts = "landslidepts_prj.shp"



#Reclassifying the data using frequency values 
#for lithology
params = {'DATA_TYPE' : 5, 
            'INPUT_RASTER' : filepath + Reclasslith, 
            'NODATA_FOR_MISSING' : False, 
            'NO_DATA' : -9999, 
            'OUTPUT' : filepath + 'RLith1.tif', 
            'RANGE_BOUNDARIES' : 0, 
            'RASTER_BAND' : 1, 
            'TABLE' : ['2285.1','2286','0.2548','2288.1','2289','0.4255','4116.1','4117','1.0908','4137.1','4138','2.302589','4888.1','4889','0.8049','4930.1','4931','0.2479','4940.1','4941','7.4665','2281.1','2282','0','2282.1','2283','0','2283.1','2284','0','2289.1','2290','0','2291.1','2292','0','4121.1','4122','0','4896.1','4897','0','4900.1','4901','0','4931.1','4932','0','4932.1','4933','0','4936.1','4937','0','4937.1','4938','0','4938.1','4939','0','4939.1','4940','0','4941.1','4942','0','4944.1','4945','0','4948.1','4949','0','4951.1','4952','0','4957.1','4958','0','4958.1','4959','0','4961.1','4962','0','4966.1','4967','0','4967.1','4968','0','4988.1','4989','0','4142.1','4143','0','4898.1','4899','0']}
processing.run("native:reclassifybytable", params)

#Reclassifying the data using frequency values 
#for geomorphology
paramsgm = {'DATA_TYPE' : 5, 
            'INPUT_RASTER' : filepath + Reclassgm, 
            'NODATA_FOR_MISSING' : False, 
            'NO_DATA' : -9999, 
            'OUTPUT' : filepath + 'RGm1.tif', 
            'RANGE_BOUNDARIES' : 0, 
            'RASTER_BAND' : 1, 
            'TABLE' : ['0','1','0','1.1','2','0','2.1','3','3.0242','3.1','4','5.6957','4.1','5','0.8901','5.1','6','0','6.1','7','0','7.1','8','0','8.1','9','0','9.1','10','0','10.1','11','0','11.1','12','0','12.1','13','0','13.1','14','0','14.1','15','0','15.1','16','0','16.1','17','1.0154','17.1','18','0','18.1','19','0','19.1','20','1.3049','20.1','21','0','21.1','22','6.3446','22.1','23','0.2581','23.1','24','0','24.1','25','0','25.1','26','0']}
processing.run("native:reclassifybytable", paramsgm)

#Reclassifying the data using frequency values 
#for curvature
paramscur = {'DATA_TYPE' : 5, 
            'INPUT_RASTER' : filepath + Reclasscur, 
            'NODATA_FOR_MISSING' : False, 
            'NO_DATA' : -9999, 
            'OUTPUT' : filepath + 'RCur1.tif', 
            'RANGE_BOUNDARIES' : 0, 
            'RASTER_BAND' : 1, 
            'TABLE' : ['0','1','1.0499','1.1','2','0.8830','2.1','3','1.0297']}
processing.run("native:reclassifybytable", paramscur)

#Reclassifying the data using frequency values 
#for aspect
paramsasp = {'DATA_TYPE' : 5, 
            'INPUT_RASTER' : filepath + Reclassasp, 
            'NODATA_FOR_MISSING' : False, 
            'NO_DATA' : -9999, 
            'OUTPUT' : filepath + 'RAsp1.tif', 
            'RANGE_BOUNDARIES' : 0, 
            'RASTER_BAND' : 1, 
            'TABLE' : ['0','1','0','1.1','2','1.3852','2.1','3','1.6691','3.1','4','1.1211','4.1','5','0.9214','5.1','6','0.3523','6.1','7','0.5876','7.1','8','1.1946','8.1','9','1.1756']}
processing.run("native:reclassifybytable", paramsasp)

#Reclassifying the data using frequency values 
#for slope
paramsslp = {'DATA_TYPE' : 5, 
            'INPUT_RASTER' : filepath + Reclassslp, 
            'NODATA_FOR_MISSING' : False, 
            'NO_DATA' : -9999, 
            'OUTPUT' : filepath + 'RSlp1.tif', 
            'RANGE_BOUNDARIES' : 0, 
            'RASTER_BAND' : 1, 
            'TABLE' : ['0','1','0','1.1','2','0.6675','2.1','3','2.6647','3.1','4','3.1846','4.1','5','0.4216']}
processing.run("native:reclassifybytable", paramsslp)

#Reclassifying the data using frequency values 
#for rr
paramsrr = {'DATA_TYPE' : 5, 
            'INPUT_RASTER' : filepath + Reclassrr, 
            'NODATA_FOR_MISSING' : False, 
            'NO_DATA' : -9999, 
            'OUTPUT' : filepath + 'RRr1.tif', 
            'RANGE_BOUNDARIES' : 0, 
            'RASTER_BAND' : 1, 
            'TABLE' : ['0','1','1.0057','1.1','6','0']}
processing.run("native:reclassifybytable", paramsrr)

#Raster calculation to make the final landslide susceptibility map
#All the reclassified rasters with the frequency ratio values  are added together to make the final susceptibility map
filelists = ["RSlp1.tif", "RAsp1.tif", "Rcur1.tif", "RRr1.tif", "RGm1.tif", "RLith1.tif"]
for file in filelists:
    iface.addRasterLayer((filepath + file), file[:-4])

RSlp2 = filepath + "RSlp1.tif"
RAsp2 = filepath + "RAsp1.tif"
RCur2 = filepath + "Rcur1.tif"
RRr2 = filepath + "RRr1.tif"
RGm2 = filepath + "RGm1.tif"
RLith2 = filepath + "RLith1.tif"
processing.run("qgis:rastercalculator", 
{'EXPRESSION': '"RAsp1@1" + "RGm1@1" + "RLith1@1" + "RRr1@1" + "RSlp1@1" + "Rcur1@1"',
'LAYERS':[filepath + 'slope_reclass.tif'],
'CELLSIZE':0,'EXTENT':None,'CRS':None,
'OUTPUT': filepath + 'weighted.tif'})

iface.addRasterLayer((filepath + 'weighted.tif'), "landslide susceptibility")

print ('Part C of the landslide susceptibility model is completed.')
