# Python version 3.X
# This snippet of code simply returns the WKT for a cooridnate reference system
import requests
from requests.auth import HTTPDigestAuth
import sys

# Replace with the correct URL
url = "https://equinor.geomaticsolutions.com/api/v1/Transformation/"
url_post = "/export/?format=wkt"

#url = "https://equinor.geomaticsolutions.com/api/v1/Extent/"


def getCRSWKT(CRScode):
    global url
    global url_post

    # Execute the search call
    myResponse = requests.get(url+CRScode+url_post)
    #myResponse = requests.get(url+str(CRScode)+"/polygon")

    # For successful API call, response code will be 200 (OK)
    if(myResponse.ok):
        # Print the data as utf-8
        return myResponse.content.decode("utf-8")
    else:
        # If response code is not ok (200), print the resulting http error code with description
        myResponse.raise_for_status()


def main():
    args = sys.argv[1:]
    if args:
        Search = args[0]
    else:
        print("This tool will print the WKT for a given Coordinate reference system")
        Search = input("Enter CRS CODE to retrieve WKT:")

    # Execute the search call
    print(getCRSWKT(Search))


if __name__ == '__main__':
    main()
