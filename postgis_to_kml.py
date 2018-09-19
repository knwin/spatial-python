# View point data stored as pogist, on Google Earth
# written by Kyaw Naing Win
# date: 14 - 8 - 2018

import cgi
import sys
from fastkml import kml
from shapely.geometry import Point
import psycopg2

url = cgi.FieldStorage()
bbox = url['BBOX'].value
bbox = bbox.split(',')
west = float(bbox[0])
south =float(bbox[1])
east = float(bbox[2])
north =float(bbox[3])

#center_lng = ((east - west) / 2) + west
#center_lat = ((north - south) / 2) + south
viewWidth = (east - west)/2
# Create the root KML object
if viewWidth < 0.5:
    
    k = kml.KML()
    ns = '{http://www.opengis.net/kml/2.2}'
    
    # Create a KML Document and add it to the KML root object
    d = kml.Document(ns, 'docid', 'doc name', 'doc description')
    k.append(d)
    
    with psycopg2.connect(host="localhost", port = 5432 ,database="base_gis", user="postgres", password="postgres") as connection:
        with connection.cursor() as  cursor:
            #cursor.execute ("SELECT ST_X(geom),ST_Y(geom) FROM mmr_pplp2_250k_mimu WHERE ts = 'Pakokku'")
            cursor.execute ("SELECT ST_X(geom),ST_Y(geom) FROM mmr_pplp2_250k_mimu WHERE geom && ST_MakeEnvelope(%s,%s,%s,%s,4326)", (west, south, east, north))
            #print  (cursor.rowcount, " records have been retrieved.")
            #extract rows from cursor
            row = cursor.fetchone()
            while row is not None:
                # Create a Placemark
                p = kml.Placemark(ns, '', '', 'this point extract from postgresql db')
                p.geometry =  Point(row[0], row[1], 0)
                d.append(p)            
                row = cursor.fetchone()
        #print ("cursor closed ", cursor.closed)
    
    print("content-type: text/html\n")
    #sys.stdout.write('<?xml version="1.0" encoding="UTF-8"?>')
    #sys.stdout.write('Content-Type: application/vnd.google-earth.kml+xml')
    #sys.stdout.write('content-type: text/html\n' )
    sys.stdout.write(k.to_string(prettyprint=True))
    connection.close()
