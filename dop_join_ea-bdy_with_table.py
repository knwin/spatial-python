# select features where its codes match with those in an external excel file
# DoP produce a excel table with EA codes selected for 2019 inter census
# DoP also have EA polygons of Census 2014 organize by Township
# Task - select from EA of census 2014 and export as shape file
# Written by Kyaw Naing Win
# 2019 - 02 - 26

import pandas as pd
import geopandas as gpd
#import fiona
import os

#src= r'C:\Temp\dop_test\source\EA_2014_shp' # where all EA bdy folders are stored
src= r'D:\OMM_GIS\Projects\DoP_InterCensus_2019\01_EA\EA_2014_shp'
#dst = r'C:\Temp\dop_test\destination\EA_2019_shp' # where selected 2019 inter census EA bdy folders are stored
dst = r'D:\OMM_GIS\Projects\DoP_InterCensus_2019\01_EA\EA_2019_shp'
ea_2019_xls = r"C:\Temp\dop_test\source\Inter_Census_Survey_sample_EAs_cleaned2_.xlsx"

ea_2019_list_df = pd.read_excel(ea_2019_xls)
print ("EA excel list read")
ea_2019_list_df = ea_2019_list_df.rename(columns={'EACODE2':'EACODE'}) # for joining two table, common column name is required
ea_2019_list_df = ea_2019_list_df.rename(columns={'Ward?':'WARD'}) # ? is not acceptable in shp file
ea_2019_list_df['EACODE'] = ea_2019_list_df['EACODE'].apply(str) # covert EA CODES as string type
ea_2019_list_df['WARD'] = ea_2019_list_df['WARD'].apply(int) # convert bolean to int
print ('EA code column \"EACODE2\" renamed as \"EACODE\", \"Ward?\" rename as \"WARD\"')
#adding 0 for some EA codes where ST code < 10
for eaCode in ea_2019_list_df['EACODE']:
    if (len(str(eaCode)) < 12):
        df_index = ea_2019_list_df.index[ea_2019_list_df['EACODE']==eaCode].tolist()
        ea_2019_list_df.set_value(df_index[0],'EACODE', "0"  + str(eaCode))
print ('EA codes are formatted to 12 character codes')


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
#      join geodf with excel pd using merge
#      save as new shape in destination folder

# walk into subdirectories
f = open("processinglog.txt",'w')
f.write("List of files with different EACODE column name..\n")
f2 =  open("processinglog2.txt",'w')
f2.write("List of files with no matched EACODE\n")
for dirpath, dirnames, filenames in os.walk(src):
#  loop through the files
    for file in filenames:
        # if file ends with shp
        if file.endswith('.shp'):
            # open as geodf
            shp = dirpath +"\\"+ file
            ea_2014_gdf = gpd.read_file(shp)
            # inner join with EA list
            #print ("EA code joining....")
            try:
                ea_2019_gdf = ea_2014_gdf.merge(ea_2019_list_df, on ='EACODE')
            
            except:
                try:
                    ea_2019_gdf = ea_2014_gdf.merge(ea_2019_list_df.rename(columns={'EACODE':'EA_CODE'}), on ='EA_CODE')                
                except:
                    print (shp, "..was skipped due to EA code column name unmatched\n")
                    f.write(shp + "\n")
                    continue
            if ea_2019_gdf.empty:
                print (file, "has no matched EA  in EA 2019 list")
                f2.write(file+"\n")
            else:
                ea_2019_gdf.crs = ea_2014_gdf.crs
                ea_2019_gdf.to_file(driver='ESRI Shapefile', filename = dst + dirpath[len(src):]+ "\\"+file[:-4]+"_2019.shp")
                print (file[:-4], "_2019.shp exported")
f.close()
f2.close()
print ("\n\nprocessing completed...")    
print ("\nread processinglog.txt and processinglog2.txt file for unmatch shps..")









