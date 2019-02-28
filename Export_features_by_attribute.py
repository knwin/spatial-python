# Save as separate shapefiles for features with same attribute
# written by Kyaw Naing Win
# 2018-12-12
import pandas as pd
import geopandas as gpd
from geopandas import GeoDataFrame as geodf



poly_shp = r"D:\\My_Documents\\OMM-CDE\\OMM Pilot and Department Activities\\DoP\\EA_Digitizing2019\\DoP_InterCensus_EA_lists\\Ward_VT\\EA_WardVT_database_20190220.shp"
poly_geodf = gpd.read_file(poly_shp)



st_list=["Kachin","Kayah","Kayin","Chin","Sagaing","Tanintharyi","Magway","Mandalay","Mon","Rakhine","Ayeyawady","Nay Pyi Taw",'Shan (East)', 'Shan (North)' ,'Shan (South)' ,'Bago (East)' ,'Bago (West)' ,'Yangon']
#st_list=['Shan (East)', 'Shan (North)' ,'Shan (South)' ,'Bago (East)' ,'Bago (West)' ,'Yangon']

for st in st_list:
    polygon = poly_geodf.loc[poly_geodf['STNAME']==st]
    shp_name = "EA_vt_" + st + ".shp"
    polygon.to_file(driver='ESRI Shapefile', filename=r'D:\\My_Documents\\OMM-CDE\\OMM Pilot and Department Activities\\DoP\\EA_Digitizing2019\\DoP_InterCensus_EA_lists\\Ward_VT\\EA_VT_ST\\'+ shp_name)
    print (shp_name, " exported")

print("processing finished..")