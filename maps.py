import requests

class Maps:
    def __init__(self,latitud,longitud):
        self.latitud = latitud
        self.longitud = longitud
    
    def getLocation(self):
        url = 'https://maps.googleapis.com/maps/api/geocode/json'
        params = {'sensor': 'false'}
        coordenadas = self.latitud + ", " + self.longitud
        params["latlng"] = coordenadas
        params["key"] = "API-KEY"
        r = requests.get(url, params=params)
        results = r.json()['results']
        location = results[0]["formatted_address"]
        if location != None:
            return location
        else:
            return "Error"
