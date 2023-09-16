import requests
from math import radians, cos, sin, asin, sqrt

def distance(lat1, lat2, lon1, lon2):
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
      
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius bumi dalam kilometer
    return c * r

# URL API SpaceX (daftar peluncuran)
spacex_launches_url = "https://api.spacexdata.com/v4/launches"

# URL API SpaceX (data launchpad)
spacex_launchpad_url = "https://api.spacexdata.com/v4/launchpads/"

# Token akses Mapbox 
mapbox_access_token = "pk.eyJ1IjoibmF6d2EwMiIsImEiOiJjbGxuNW14enkwZHE0M3BsNDE2bm5jMGhxIn0.9U-lBCWgoV5TvNHvGf0kYg"

# Mengambil data peluncuran dari API SpaceX
response_launches = requests.get(spacex_launches_url)
launches_data = response_launches.json()

# Ambil 20 peluncuran terakhir
recent_launches = launches_data[-20:]

for launch in recent_launches:
    launchpad_id = launch['launchpad']
    response_launchpad = requests.get(spacex_launchpad_url + launchpad_id)
    launchpad_data = response_launchpad.json()

    spacex_longitude = launchpad_data['longitude']
    spacex_latitude = launchpad_data['latitude']

    query = launchpad_data['full_name']
    mapbox_url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{query}.json?access_token={mapbox_access_token}"
    response_mapbox = requests.get(mapbox_url)
    mapbox_data = response_mapbox.json()

    if 'features' in mapbox_data and len(mapbox_data['features']) > 0:
        mapbox_longitude = mapbox_data['features'][0]['center'][0]
        mapbox_latitude = mapbox_data['features'][0]['center'][1]

        distance_km = distance(spacex_latitude, mapbox_latitude, spacex_longitude, mapbox_longitude)
        
        
        print(launch['date_utc'],launchpad_data['full_name'],distance_km)
        
      