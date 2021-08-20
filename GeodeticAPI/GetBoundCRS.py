# Python version 3.X
import requests
from requests.auth import HTTPDigestAuth
import json

# Replace with the correct URL
early_bound_geodetic = "11"
early_bound_projected = "21"
page_size = 600
url = "https://equinor.geomaticsolutions.com/api/v1/BoundCoordRefSystem/"
request_url = url + "?pageSize=" + str(page_size)
print("This tool will search Bound CRS")
# Search = input("What are you looking for ? ")

# Execute the search call
myResponse = requests.get(request_url)

# For successful API call, response code will be 200 (OK)
if(myResponse.ok):
    # Loading the response data into a dictionary variable
    # json.loads takes in only binary or string variables
    # Loads (Load String) takes a Json file and converts into python data structure (dict or list, depending on JSON)
    jData = json.loads(myResponse.content)
    # If (early_bound_geodetic):
    # Create sql files
    # If (early_bound_projected):
    #   sql = ""INSERT INTO equinor.geodetic_crs values('')""

    for x in jData:
        if(x == "Count"):
            print("Returned elements : %d\n" % (jData[x]))
        if(x == "TotalResults"):
            print("Total elements : %d\n" % (jData[x]))
        if(x == "Results"):
            jResults = jData[x]
            print("elements {0}".format(len(jResults)))
            for y in range(len(jResults)):
                jPart = jResults[y]
                for z in jPart:
                    # if(z == "Code"):
                    if str(jPart["Code"]).startswith(early_bound_geodetic):
                        print("sql = INSERT INTO equinor.geodetic_crs values(\t%s\t%d\t%s\t%s)" %
                              (jPart["DataSource"], jPart["Code"], jPart["Type"], jPart["Name"]))
                    else:
                        print("sql = INSERT INTO equinor.projected_crs values(\t%s\t%d\t%s\t%s)" %
                              (jPart["DataSource"], jPart["Code"], jPart["Type"], jPart["Name"]))
else:
  # If response code is not ok (200), print the resulting http error code with description
    myResponse.raise_for_status()
