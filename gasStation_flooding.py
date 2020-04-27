import requests
import pandas as pd
import shapefile as shp
import csv
import folium


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

# Read Pinellas county flood data from FEMA
floodSHP = shp.Reader("FEMA_Pinellas_Data/S_FLD_HAZ_AR.shp")

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
