# extract photos as new chunk with a buffered polygon and 
# written by Kyaw Naing Win, OneMap GIS Program Manager
# 2019-12-12

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
try:
	import PhotoScan as m
except:
	print ("Photoscan module not exit..")
else:
	import Metashape as m
	
# working on shp file
shp = r'C:\WingPy_scripts\geopandas\simplify_kwin_shp\Simplify_kwin.shp'
colNmae = 'Name' # attribute column name
value = "525_B" # attribute of polygon that I want to use
buffer_size = 0.0005 # buffer about 50m in degree
shp_gdf = gpd.read_file(shp) # read as geopandas dataframe
polygon = shp_gdf.loc[shp_gdf[colName] == value] # select desire polygon
polygon['geometry'] = polygon.geometry.buffer(buffer_size)  # buffering

# working on Photoscan part
doc = m.app.document # this is project document in Photoscan/Metashape
chunk= doc.chunk # currennt chunk with all photos
cameras = chunk.cameras # return all camera in the chunk
index_num = []
x = []
y = []
name = []
i = 0
# extract photo names, Xs, Ys and indexes
for camera in cameras:
    name.append(camera.photo.path)
    x.append(camera.reference.location[0])
    y.append(camera.reference.location[1])
    index_num.append(i)
    i = i + 1
	
# create photo locations as GeodataFrame
df = {"name": pd.Series(name, index=index_num), "X" : pd.Series(x, index = index_num), "Y":pd.Series(y, index=index_num)}
df = pd.DataFrame(df)
df['XY'] = list(zip(df.X, df.Y))
df['XY'] = df['XY'].apply(Point)
photo_gdf=gpd.GeoDataFrame(df, geometry = 'XY')

# select photos and create as new chunk in current project
photo_subset = photo_gdf[photo_gdf.within(polygon.geometry[polygon.index.min()])]

new_chunk = doc.addChunk()
new_chunk.addCamera()
new_chunk.addPhotos(photo_subset['name'])