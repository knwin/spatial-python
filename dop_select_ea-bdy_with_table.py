# select features where its codes match with those in an external excel file
# DoP produce a excel table with EA codes selected for 2019 inter census
# DoP also have EA polygons of Census 2014 organize by Township
# Task - select from EA of census 2014 and export as shape file
#
# Written by Kyaw Naing Win
# 2019 - 02 - 26
#
import pandas as pd
import geopandas as gpd
import os

src= r'C:\Temp\dop_test\source\EA_2014_shp'
dst = r'C:\Temp\dop_test\destination\EA_2019_shp'
ea_2019_xls = r"C:\Temp\dop_test\source\Inter_Census_Survey_sample_EAs_cleaned2_.xlsx"
ea_2019_list_df = pd.read_excel(ea_2019_xls)
print ("EA excel list read")
def copyTree(src, dst):
    for dirpath, dirnames, filenames in os.walk(src):
        structure = dst + dirpath[len(src):]
        if not os.path.isdir(structure):
            os.mkdir(structure)
        else:
            print("Folder does already exits!")
    print ("folder structure copied")
    
copyTree (src, dst)

# walk into subdirectories
#  loop through the files
#    if file ends with shp
#      open as geodf
#      loop each line of ea list
#        if EACODE2 = EACODE
#          append the feature to new geodf
#      save new geodf

# walk into subdirectories
for dirpath, dirnames, filenames in os.walk(src):
#  loop through the files
    for file in filenames:
        # if file ends with shp
        if file.endswith('.shp'):
            # open as geodf
            shp = dirpath +"\\"+ file
            ea_2014_gdf = gpd.read_file(shp)
            ea_2019_gdf = gpd.GeoDataFrame() # initialize empty geodf
            # loop each line of ea list
            print ("EA code matching....")
            for eaCode in ea_2019_list_df['EACODE2']:
                #print ("matching EACODE: " + str(eaCode))
                ea_polygon = ea_2014_gdf.loc[ea_2014_gdf['EACODE']==str(eaCode)]
                ea_2019_gdf = gpd.GeoDataFrame(pd.concat([ea_2019_gdf, ea_polygon], ignore_index=True)) # append selected polygon(s)
            
            ea_2019_gdf.to_file(driver='ESRI Shapefile', filename = dst + dirpath[len(src):]+ "\\"+file[:-4]+"_2019.shp", crs=ea_2014_gdf.crs)
            print (file[:-4], "_2019.shp exported")
            









