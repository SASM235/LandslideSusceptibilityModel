#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#Landslide susceptibility model ----------- Part B --------- by Shruti Anna Samuel (s3933141)
#Reclassification and calculating frequency of the layers
#1) Reclassification of layers (aspect, curvature, relative relief, slope). The geomorphology and lithology layers are already categorised as they have categorical data.
#2) Computing the frequency of landslides and percentage area in each category of the rasters using rasters unique layers report, sample raster values, and statistics by categories processing algorithms.

#importing the necessary classes
import math
import qgis
import processing
import pandas as pd

#provide the file path
filepath = "C:\\Users\\Provide_your_filepath_here\\"
#Output filenames
Rslp = "slope_reclass.tif"
Rasp = "aspect_reclass.tif"
Rcur = "curv_reclass.tif"
Rrr = "rr_reclass.tif"
Rgm = "geomraster_clipped.tif"
Rlith = "lithoraster_clipped.tif"

QgsProject.instance().removeAllMapLayers()#To remove the previously loaded layers.

#Reclassification aspect
asp = 'aspect_clipped.tif'
asp_clipped = iface.addRasterLayer(filepath + asp, "asp_clipped") #adding the clipped aspect raster in qgis

#Creating variables that denote the class boundaries for reclassification. 
#Aspect is divided based on the standard values for Flat, N, NE, E, SE, S, SW, W, NW categories.
pos_one = '-2'
pos_two = '0'
pos_three = '22.5'
pos_four = '67.5'
pos_five = '112.5'
pos_six = '157.5'
pos_seven = '202.5'
pos_eight = '247.5'
pos_nine = '292.5'
pos_ten = '337.5'
pos_eleven = '360'
        
table_list = [pos_one,pos_two,1,pos_two,pos_three,2,pos_three,pos_four,3,pos_four,pos_five,4,pos_five,pos_six,5,pos_six,pos_seven,6,pos_seven,pos_eight,7,pos_eight,pos_nine,8,pos_nine,pos_ten,9,pos_ten,pos_eleven,2]
        
alg_params = {
    'INPUT_RASTER': asp_clipped,
    'RASTER_BAND': 1,
    'TABLE': table_list, #Classified as Flat, N, NE, E, SE, S, SW, W, NW
    'OUTPUT': filepath + Rasp
    }
        
processing.runAndLoadResults("native:reclassifybytable",alg_params)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#Reclass curvature
curv = 'curvature_clipped.tif'
curv_clipped = iface.addRasterLayer(filepath + curv, "curvature_clipped") #adding the clipped curvature raster layer in QGIS.

raster_provider = curv_clipped.dataProvider()
stats = raster_provider.bandStatistics(1, QgsRasterBandStats.All) #Finding the raster band statistics to define the classification ranges 

#Classification values categorise the data as convex, flat, concave
pos_one = stats.minimumValue#minimum value of the raster band
pos_two = '-0.01'
pos_three = '0'
pos_four = '+0.01'
pos_five = stats.maximumValue#maximum value of the raster band

table_list = [pos_one,pos_two,1,pos_two,pos_four,2,pos_four,pos_five,3]
        
alg_params_3 = {
    'INPUT_RASTER': curv_clipped,
    'RASTER_BAND': 1,
    'TABLE': table_list,#Classified as convex, flat, and concave
    'OUTPUT': filepath + Rcur,
    }
        
processing.runAndLoadResults("native:reclassifybytable",alg_params_3)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#Reclass relative relief
rr = 'rr_clipped.tif'
rr_clipped = iface.addRasterLayer(filepath + rr, "rr_clipped")#adding the clipped relative relief raster layer in QGIS.

raster_provider = rr_clipped.dataProvider()
stats = raster_provider.bandStatistics(1, QgsRasterBandStats.All) #Finding the raster band statistics to define the classification ranges 
range = stats.maximumValue - stats.minimumValue #Difference between the maximum and minimum values in a raster
step = math.ceil((range/5)*100)/100 #Deciding the step for classification

#Equal interval classification based on minimum and maximum values of the raster
pos_one = stats.minimumValue - 1
pos_two = (stats.minimumValue + step)
pos_three = (pos_two + step)
pos_four = (pos_three + step)
pos_five = (pos_four + step)
pos_six = (pos_five + step)
        
        
table_list = [pos_one,pos_two,1,pos_two,pos_three,2,pos_three,pos_four,3,pos_four,pos_five,4,pos_five,pos_six,5]
        
alg_params_3 = {
    'INPUT_RASTER': rr_clipped,
    'RASTER_BAND': 1,
    'TABLE': table_list,
    'OUTPUT': filepath + Rrr,
    }
        
processing.runAndLoadResults("native:reclassifybytable",alg_params_3)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#Reclass slope
slp = 'slope_clipped.tif'
slp_clipped = iface.addRasterLayer(filepath + slp, "slope_clipped")#adding the clipped slope raster layer in QGIS.

raster_provider = slp_clipped.dataProvider()
stats = raster_provider.bandStatistics(1, QgsRasterBandStats.All)#Finding the raster band statistics to define the classification ranges 

#Slope is classified as -1 to 5, 5 to 15, 15 to 25, 25 to 35, and >35 categories.
pos_one = '-1'
pos_two = '5'
pos_three = '15'
pos_four = '25'
pos_five = '35'
pos_six = (stats.maximumValue)
        
        
table_list = [pos_one,pos_two,1,pos_two,pos_three,2,pos_three,pos_four,3,pos_four,pos_five,4,pos_five,pos_six,5]
        
alg_params_3 = {
    'INPUT_RASTER': slp_clipped,
    'RASTER_BAND': 1,
    'TABLE': table_list,
    'OUTPUT': filepath + Rslp,
    }
        
processing.runAndLoadResults("native:reclassifybytable",alg_params_3)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#Getting the count of pixels in each category within all LCF layers as tables
#CSV files having the count and area of pixels in each reclassified raster layers are created in the filepath provided.
#These files will have '_csv' suffix


listfiles = [Rslp, Rasp, Rcur, Rrr, Rgm, Rlith]
output = []

for file in listfiles:
    output = file[:-4]+'_csv'+'.csv'
    parameters1 = {'INPUT': (filepath + file),'BAND': 1,'OUTPUT_TABLE': (filepath + output)}

    result = processing.runAndLoadResults("native:rasterlayeruniquevaluesreport",parameters1)

print ('Successfully exported the raster layers unique values report !!')
    
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#  
#Sample rasters with the landslide points
#This step is conducted to find the (Landslide Causative Factor) LCF raster values in the landslide locations

lspts = "landslidepts_prj.shp" #Add the name of the landslide points shapefile located in the filepath folder

for file in listfiles:
    out = file[:-4]+'_sampled'+'.shp' #Output files will have the suffix '_sampled'
    params = {'INPUT': (filepath + lspts), 
              'RASTERCOPY': (filepath + file),
              'COLUMN_PREFIX': 'sample_', #the fields with the sampled values will have the prefix 'sample_1'
              'OUTPUT': filepath + out}
    processing.run("native:rastersampling", params)
    
print ('Successfully sampled the rasters using landslide points!!')
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#statistics by categories

#Adding the output files from the above step
sampledSlp = "slope_reclass_sampled.shp"
sampledAsp = "aspect_reclass_sampled.shp"
sampledCur = "curv_reclass_sampled.shp"
sampledRr = "rr_reclass_sampled.shp"
sampledGm = "geomraster_clipped_sampled.shp"
sampledLith = "lithoraster_clipped_sampled.shp"
lspts = "landslidepts_prj.shp"


#Iterating through the layers to find the number of landslides in each category of the raster layers.
listfiles = [sampledSlp, sampledAsp, sampledCur, sampledRr, sampledGm, sampledLith]

for file in listfiles:
    #for catName in categoryName:
    out = file[:-4]+'_stat'+'.csv'#Output CSV files will have the suffix '_stat'
        
    params = {'INPUT': (filepath + file), 
              'CATEGORIES_FIELD_NAME': 'sample_1',
              'VALUES_FIELD_NAME':'',
              'OUTPUT': filepath + out}
    processing.runAndLoadResults("qgis:statisticsbycategories", params)
    
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#read CSV tables
#Frequency ratio calculation


statrr = pd.read_csv(filepath+'rr_reclass_sampled_stat.csv')
statslp = pd.read_csv(filepath+'slope_reclass_sampled_stat.csv')
statlitho = pd.read_csv(filepath+'lithoraster_clipped_sampled_stat.csv')
statgm = pd.read_csv(filepath+'geomraster_clipped_sampled_stat.csv')
statcurv = pd.read_csv(filepath+'curv_reclass_sampled_stat.csv')
statasp = pd.read_csv(filepath+'aspect_reclass_sampled_stat.csv')

areaPerrr = pd.read_csv(filepath + 'rr_reclass_csv.csv')
areaPerslp = pd.read_csv(filepath + 'slope_reclass_csv.csv')
areaPerlitho = pd.read_csv(filepath + 'lithoraster_clipped_csv.csv')
areaPergm = pd.read_csv(filepath + 'geomraster_clipped_csv.csv')
areaPercurv = pd.read_csv(filepath + 'curv_reclass_csv.csv')
areaPerasp = pd.read_csv(filepath + 'aspect_reclass_csv.csv')

#Computing the landslide frequency of each class in different rasters. 
#Landslide frequency can be calculated as the number of landslide points in each class divided by the total number of landslide points.
totalLS = statrr["count"].sum()
statrr["freqrr"]=statrr["count"]/totalLS
statslp["freqslp"]=statslp["count"]/totalLS
statlitho["freqlitho"]=statlitho["count"]/totalLS
statgm["freqgm"]=statgm["count"]/totalLS
statcurv["freqcurv"]=statcurv["count"]/totalLS
statasp["freqasp"]=statasp["count"]/totalLS

#Computing the area percentage of each class in different rasters. 
#Area percentage can be calculated as the area percentage in each class divided by the total area of the study.
total = areaPerslp['m2'].sum()
areaPerrr["freqclass"]=areaPerrr['m2']/total
areaPerslp["freqclass"]=areaPerslp['m2']/total
areaPerlitho["freqclass"]=areaPerlitho['m2']/total
areaPergm["freqclass"]=areaPergm['m2']/total
areaPercurv["freqclass"]=areaPercurv['m2']/total
areaPerasp["freqclass"]=areaPerasp['m2']/total

#Joining the two tables to calculate the frequency ratio
mergedSlp= areaPerslp.merge(statslp, left_on ='value', right_on='sample_1')
mergedRr = areaPerrr.merge(statrr, left_on ='value', right_on='sample_1')
mergedLitho = areaPerlitho.merge(statlitho, left_on ='value', right_on='sample_1')
mergedGm= areaPergm.merge(statgm, left_on ='value', right_on='sample_1')
mergedCurv = areaPercurv.merge(statcurv, left_on ='value', right_on='sample_1')
mergedAsp = areaPerasp.merge(statasp, left_on ='value', right_on='sample_1')

#Finding the frequency ratio. It is calculated as the frequency of landslides in each class divided by the area perecentage in each class.
mergedSlp["frequency ratio"]=mergedSlp["freqslp"]/mergedSlp["freqclass"]
mergedRr["frequency ratio"]=mergedRr["freqrr"]/mergedRr["freqclass"]
mergedLitho["frequency ratio"]=mergedLitho["freqlitho"]/mergedLitho["freqclass"]
mergedGm["frequency ratio"]=mergedGm["freqgm"]/mergedGm["freqclass"]
mergedCurv["frequency ratio"]=mergedCurv["freqcurv"]/mergedCurv["freqclass"]
mergedAsp["frequency ratio"]=mergedAsp["freqasp"]/mergedAsp["freqclass"]

#printing the attribute tables showing the compiled information from the above steps and the frequency ratio.
print(mergedSlp)
print(mergedRr)
print(mergedLitho)
print(mergedGm)
print(mergedCurv)
print(mergedAsp)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
print ('Part B of landslide susceptibility model is completed. The frequency values for each class in the rasters have been calculated.')
