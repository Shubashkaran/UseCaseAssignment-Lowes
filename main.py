from urllib.parse import quote
from requests import get
from json import loads
from math import radians,sin,cos,asin,sqrt

config={
  "fullNameSearchURL": "https://restcountries.com/v3.1/name/{}?fullText=true",
  "searchBasedOnCodesURL": "https://restcountries.com/v3.1/alpha?codes={}"
}

def calculateApproximateDistance(srcLatLng,destLatLang):
    """Calculates approximate distance between source country and destination country.

        Parameters
        ----------
        srcLatLng : list, required
            lattitude and longitude of the source country
        destLatLng : list, required
            lattitude and longitude of the destination country

        Returns
        ------
        distance : float
            distance between source country and destination country in miles.
    """
    slat,slong,dlat,dlong=map(radians,srcLatLng+destLatLang)
    difflong,difflat=dlong-slong,dlat-slat

    haversine = sin(difflat/2)**2 + cos(slat) * cos(dlat) * sin(difflong/2)**2
    centralAngle = 2 * asin(sqrt(haversine))
    earthRadiusMiles = 3958.8
    return earthRadiusMiles * centralAngle


countryFullName=(input("Enter the country name:\n")).replace('"','').replace('“','').replace('”','')
countryFullNameEncoded=quote(countryFullName)
url=config["fullNameSearchURL"].format(countryFullNameEncoded)
res=get(url)

if(res.status_code==200):
    respSource=loads(res.content)[0]
    borders=respSource["borders"]
    url_n=config["searchBasedOnCodesURL"].format(",".join(borders))
    respNeighbours=loads(get(url_n).content)

    print(f"\nBordering countries of “{countryFullName}” are {', '.join(i['name']['common'] for i in respNeighbours)}\n")

    for i in respNeighbours:
        comLangs=list(set(respSource["languages"]).intersection(set(i["languages"])))
        print(f"{i['name']['common']}\n"
        f"official language – {'yes' if len(comLangs)>0 else 'no'}\n"
        f"Car diving side – {'yes' if respSource['car']['side']==i['car']['side'] else 'no'}\n"
        f"Approx Distance – {int(calculateApproximateDistance(respSource['latlng'],i['latlng']))} Miles\n")
else:
    print("Invalid country name")
