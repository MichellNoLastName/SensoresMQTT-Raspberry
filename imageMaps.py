import requests
import shutil

class GetImage:
    def __init__(self,fileRute, center, zoom, APIKeyFile):
        self.fileRute = fileRute
        self.center = center
        self.zoom = zoom
        self.APIKeyFile = APIKeyFile
    
    def getAPIKey(self):
        file = open(self.APIKeyFile)
        key = file.read()
        key = key.replace("\n","")
        return key

    def getStaticGoogleMap(self,imgsize="500x500", imgformat="jpeg",maptype="roadmap"):  
    
        # assemble the URL
        request =  "http://maps.google.com/maps/api/staticmap?" # base URL, append query params, separated by &
   
        # if center and zoom  are not given, the map will show all marker locations
        if self.center != None:
            request += "center=%s&" % self.center
            
        if self.zoom != None:
            request += "zoom=%i&" % self.zoom  # zoom 0 (all of the world scale ) to 22 (single buildings scale)


        request += "size=%s&" % (imgsize)  # tuple of ints, up to 640 by 640
        request += "format=%s&" % imgformat
        request += "maptype=%s&" % maptype  # roadmap, satellite, hybrid, terrain


        # add markers (location and style)
        marker = "markers=size:mid|color:red|label:P|" + self.center
        request += "%s&" % marker


        #request += "mobile=false&"  # optional: mobile=true will assume the image is shown on a small screen (mobile device)
        request += "sensor=false&"   # must be given, deals with getting loction from mobile device
        request += "key=" + self.getAPIKey()
        r = requests.get(request, stream=True)
        if r.status_code == 200:
            imageFile = self.fileRute + ".jpg"
            try:
                with open(imageFile, "wb") as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
                    return 1
            except Exception as ex:
                print("Error: ",ex)
                return 0
        
        
        
        
        