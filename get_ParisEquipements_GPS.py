# require Python 2.7

import urllib2
import json

###################################################
categories = "235" # (pour l'instant entrer plusieurs catégories ne fonctionne pas...)
###################################################

# les catégories :
# toutes les biliotèques de Paris : "238,239,315,38,316,318,235,237,240"
# toutes les piscines de Paris : "29,27"
# tous les espaces verts de Paris : "304,14,7,91"
# tous les musées de Paris : "67,68,12"
# tous les cinémas et théatres de Paris : "34,70,85,74"
# les autres : https://api.paris.fr:3000/data/1.0/Equipements/get_categories/?token=d7ff0546ffe8d9e14ff45d0f0468cdd665ca6f4ed14c0f96e10c5e849788d5b3

paris_url = "https://api.paris.fr:3000/data/1.0/Equipements/get_equipements/?token="
paris_url += "d7ff0546ffe8d9e14ff45d0f0468cdd665ca6f4ed14c0f96e10c5e849788d5b3" # mon identifiant perso
paris_url += "&cid="
paris_url += categories
paris_url += "&offset=0&limit=100"

paris_req = urllib2.Request(paris_url)
paris_handle = urllib2.urlopen(paris_req)
paris_content = paris_handle.read()
paris_equipements = json.loads(paris_content)

i = 0
equipements = len(paris_equipements["data"])-1

while i < equipements:

    print i
    
    address_array = str.split(paris_equipements["data"][i]["address"].encode('utf-8'));
    zipCode_array = str.split(str(paris_equipements["data"][i]["zipCode"]));

    address = ''
    
    for i2 in address_array:
        address += str(i2) + '+'

    for i3 in zipCode_array:
        address += str(i3) + '+'

    address += "Paris,+France"
    
    geocode_url = "http://maps.googleapis.com/maps/api/geocode/json?address="
    geocode_url += address
    geocode_url += "&sensor=false"

    geocode_req = urllib2.Request(geocode_url)
    geocode_handle = urllib2.urlopen(geocode_req)
    geocode_content = geocode_handle.read()
    geocode_equipements = json.loads(geocode_content)
    
    if (len(geocode_equipements["results"]) > 0):
        paris_equipements["data"][i]["coord"] = str(geocode_equipements["results"][0]["geometry"]["location"]["lng"])
        paris_equipements["data"][i]["coord"] += ':' + str(geocode_equipements["results"][0]["geometry"]["location"]["lat"])
        print paris_equipements["data"][i]["coord"]
        i += 1
    else:
        print "zap! no geocode answer"

outputFile = open("parisEquipements_"+str(categories)+".json", 'w')
outputFile.write(json.dumps(paris_equipements));

print ("done!")
