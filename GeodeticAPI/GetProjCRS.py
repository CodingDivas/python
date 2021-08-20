# Python version 3.X
import requests
from requests.auth import HTTPDigestAuth
import json

# Replace with the correct URL
url = "https://equinor.geomaticsolutions.com/api/v1/ProjectedCoordRefSystem/"
print("Given an EPSG code for a projected CRS, this tool returns the name and prints the extent data for all usages")
Search = input("What code are you looking for ? ")
value = int(Search)

Search = str(value)
RequestURL = url+Search+"/"
myResponse = requests.get(RequestURL)

# For successful API call, response code will be 200 (OK)
if(myResponse.ok):
    # Loading the response data into a dict variable
    jData = json.loads(myResponse.content)
    print("CRS name   : "+jData["Name"])
    print("Base CRS   : "+jData["BaseCoordRefSystem"]["Name"])
    print("Projection : "+jData["Projection"]["Name"])
    print("Coord sys  : "+jData["CoordSys"]["Name"])
    print("Type       : "+jData["Kind"])
    # Now iterate the usages
    for usage in jData["Usage"]:
        print("Code : " + str(usage["Extent"]["Code"]))
        # Got a code, so we can get the data
        myResponse = requests.get(
            "https://equinor.geomaticsolutions.com/api/v1/Extent/" + str(usage["Extent"]["Code"]))
        if myResponse.ok:
            extentData = json.loads(myResponse.content)
            print("Extent name : " + extentData["Name"])
            print("Extent desc : " + extentData["Description"])
            print("BBX North   : " +
                  str(extentData["BoundingBoxNorthBoundLatitude"]))
            print("BBX West    : " +
                  str(extentData["BoundingBoxWestBoundLongitude"]))
            print("BBX East   : " +
                  str(extentData["BoundingBoxEastBoundLongitude"]))
            print("BBX South   : " +
                  str(extentData["BoundingBoxSouthBoundLatitude"]))
else:
    # If response code is not ok (200), print the resulting http error code with description
    if (myResponse.status_code == 500):
        print(Search+" code is not a projected CRS")
        value = value + 1
    else:
        myResponse.raise_for_status()
