import requests
import pandas as pd
import shapefile as shp
import csv
import folium

# Crime Data from Pinellas Crime Viewer: http://egis.pinellascounty.org/apps/CrimeViewer/
url = 'http://egis.pinellascounty.org/arcgis/rest/services/LawEnforcement/CrimeViewer/MapServer/0/' \
      'query?'
query = 'f=json&where=CATEGORY%20IN%20(%27%27%2C%27grpBURGLARY%27%2C%27BURGLARY-BUSINESS%27%2C%27' \
    'BURGLARY-RESIDENCE%27%2C%27BURGLARY-STRUCTURE%27%2C%27BURGLARY-VEHICLE%27%2C%27grpRobbery%27%2C%27' \
    'ROBBERY-ARMED%27%2C%27ROBBERY-CARJACKING%27%2C%27ROBBERY-HOME%20INVADE%27%2C%27ROBBERY-UNARMED%27%2C' \
    '%27grpTHEFT%27%2C%27THEFT-GRAND%27%2C%27THEFT-PETIT%27%2C%27THEFT-PURSE%20SNATCH%27%2C%27THEFT-' \
    'SHOPLIFTING%27%2C%27STOLEN%20VEHICLE%27%2C%27STOLEN%20VEHICLE%20-%20REC%27%2C%27%27)%20AND%20AGENCY' \
    '_ID%20IN%20(%27%27%2C%27PCPO%27%2C%27CPD%27%2C%27%27)%20AND%20%20REPORT_DATE%20%3E%3D%20date%20%272019' \
    '-4-21%27%20AND%20REPORT_DATE%20%3C%3D%20date%20%272020-04-28%27&returnGeometry=true&spatialRel=esriSpatial' \
    'RelIntersects&outFields=REPORT_KEY%2CLAT%2CLON%2CAGENCY_ID%2CCATEGORY%2CREPORT_CODE%2CREPORT_DATE%2COFFENSE_' \
    'START_TIME%2CBLOCK_ADDRESS%2CCITY%2CZIP'

pinellasCrimeRequests = requests.post(url+query)
pinellasCrime = pinellasCrimeRequests.json()

# Gas station locations in Clearwater, FL from NREL
gasStationRequests = \
    requests.get(
        'https://developer.nrel.gov/api/alt-fuel-stations/v1/nearest.json?api_key=RweLonDakbcLwofn4cPSKcMJFqoW7TZ3KBTH'
        'zam8&location=Clearwater+FL')
gasStationData = gasStationRequests.json()
gasStationTable = pd.DataFrame(gasStationData['fuel_stations'])
# gasStationTable.to_csv('clearwater_gasStations.csv')

# Make shapefile point from gas station dataframe
w = shp.Writer('QGIS/gas_pts')
w.field('X','F',10,5)
w.field('Y','F',10,5) #float - needed for coordinates
w.field('label')
for index, row in gasStationTable.iterrows():
   w.point(row['longitude'],row['latitude'])
   w.record(row['longitude'],row['latitude'],str(row['station_name']))
w.close()

gasSHP = shp.Reader("QGIS/gas_pts.shp")

# Clearwater city polygon from open data ArcGIS
flCitiesSHP = shp.Reader("QGIS/City_Boundaries/City_Boundaries.shp")

# Select Clearwater from the rest of the boundaries
fields = flCitiesSHP.fields[1:]
field_names = [field[0] for field in fields]
w2 = shp.Writer('QGIS/clearwater',shapeType=5)
w2.fields = fields
# construction of a dictionary field_name:value
for layer in flCitiesSHP.iterShapeRecords():
    rec = layer.record
    atr = dict(zip(field_names, layer.record))
    if atr['CITY_NAME'] == 'Clearwater':
        print(layer)
        w2.record(layer.shape)
        data = atr
        #w2.poly(atr['ShapeSTAre'],atr['ShapeSTLen'])
        w2.record(data['CITY_NAME'],data['ShapeSTAre'],data['ShapeSTLen'])
        #w2._shapes.append(r.shape)
w2.close()

# Leaflet
m = folium.Map(location=[45.5236, -122.6750])
