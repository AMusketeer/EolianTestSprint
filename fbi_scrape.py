import requests
import pandas as pd
import shapefile
import folium

# API Key RweLonDakbcLwofn4cPSKcMJFqoW7TZ3KBTHzam8
# Request format https://api.usa.gov/crime/fbi/sapi/api/data/arrest/states/offense/FL//2000%2F01%2F01/2020%2F01%2F01?api_key=RweLonDakbcLwofn4cPSKcMJFqoW7TZ3KBTHzam8

baseURL = 'https://api.usa.gov/crime/fbi/sapi'

gasStationRequests = \
    requests.get(
        'https://developer.nrel.gov/api/alt-fuel-stations/v1/nearest.json?api_key=RweLonDakbcLwofn4cPSKcMJFqoW7TZ3KBTH'
        'zam8&location=Clearwater+FL')
gasStationData = gasStationRequests.json()
gasStationTable = pd.DataFrame(gasStationData['fuel_stations'])

# Read Pinellas county flood data from FEMA
sf = shapefile.Reader("FEMA_Pinellas_Data/S_FLD_HAZ_AR.shp")

# Leaflet
m = folium.Map(location=[45.5236, -122.6750])