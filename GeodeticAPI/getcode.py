# Python version 3.X
import requests
from requests.auth import HTTPDigestAuth
import json

# Replace with the correct URL
url = "https://apps.epsg.org/api/v1/CoordRefSystem/?keywords="
print("This tool will search Coordinate reference systems for the keyword entered, max 500 elements are retrieved")
Search = input("What are you looking for ? ")

# Execute the search call
myResponse = requests.get(url+Search+"&includeWorld=true&pageSize=500")

# For successful API call, response code will be 200 (OK)
if(myResponse.ok):
    # Loading the response data into a dictionary variable
    # json.loads takes in only binary or string variables
    # Loads (Load String) takes a Json file and converts into python data structure (dict or list, depending on JSON)
    jData = json.loads(myResponse.content)

    for x in jData:
        if(x=="Count"):
            print("Returned elements : %d\n" % (jData[x]))
        if(x=="Results"):
            jResults = jData[x]
            print("elements {0}".format(len(jResults)))
            for y in range(len(jResults)):
                jPart = jResults[y]
                for z in jPart:
                    if(z=="Name"):
                        print("%d\t%s" % (jPart["Code"],jPart[z]))
else:
  # If response code is not ok (200), print the resulting http error code with description
    myResponse.raise_for_status()
