# Extract Location information from EXIF of drone images and creat a kml
# Kyaw Naing Win
# 2018-09-09
import exifread, os
import datetime
from fastkml import kml
from shapely.geometry import Point
today = str(datetime.date.today())
ctime = str(datetime.datetime.now().time())
today = today + ", " + ctime
path = "D:\\Drone_missions\\shwesantaw\\100MEDIA"

# Create the root KML object
k = kml.KML()
ns = '{http://www.opengis.net/kml/2.2}'
# Create a KML Document and add it to the KML root object
d = kml.Document(ns, 'docid', 'Image locations', 'Created on ' + today)
k.append(d)
# Create a KML Folder and add it to the Document
fkml = kml.Folder(ns, 'fid', 'f name', 'f description')
d.append(fkml)

for file in os.listdir(path):
    if file.endswith(".JPG"):
        f = open(path+"\\"+file, 'rb')
        tags = exifread.process_file(f)
        
        #extract lat, lon, alt tags
        exif_lat = tags["GPS GPSLatitude"]
        exif_lon = tags["GPS GPSLongitude"]
        exif_alt = tags["GPS GPSAltitude"]
        
        #latitude
        lat_deg = exif_lat.values[0].num # values are ratio data type
        lat_min = exif_lat.values[1].num
        lat_sec = exif_lat.values[2].num/exif_lat.values[2].den
        lat = lat_deg + lat_min/60 + lat_sec/3600 # covert into decimal degree
        
        #longitude
        lon_deg = exif_lon.values[0].num # values are ratio data type
        lon_min = exif_lon.values[1].num
        lon_sec = exif_lon.values[2].num/exif_lon.values[2].den        
        lon = lon_deg + lon_min/60 + lon_sec/3600 # covert into decimal degree
        
        #altitude
        alt = exif_alt.values[0].num/ exif_alt.values[0].den #convert ratio to decimal       
          
        #print (file,"- lat: ", lat, ", Lon: ", lon, ", alt: ", alt)

        p = kml.Placemark(ns, 'id', file, 'description')
        p.geometry =  Point(lon,lat, alt)
        fkml.append(p)

f_kml = open(path+"\\"+"drone_img_locations.kml", "w+")
f_kml.write(k.to_string()) 
f_kml.close()
print ("drone_img_locations.kml has been created")
