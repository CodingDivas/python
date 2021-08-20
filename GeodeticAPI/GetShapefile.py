# Python version 3.X
# This program will use the EPSG.org site get a polygon and then create the
# shapefile of it.
# ------------------------------------------------------------------------------------------------------
import requests
from requests.auth import HTTPDigestAuth
from osgeo import ogr
import json
import sys

# The URL looks like this
#url = "https://apps.epsg.org/api/v1/Extent/"
#url = "https://devweb.geomaticsolutions.com/georepository/dev/api/v1/Extent/"
url = "https://equinor.geomaticsolutions.com/api/v1/Extent/"


def main():
    args = sys.argv[1:]
    if len(args) == 2:
        crsCode = args[0]
        shapeName = args[1]
    else:
        print("This application creates a shapefile given a polygon. The Polygons are defined as extents in the EPSG database")
        print("Currently data is retrieved from "+url)
        print("----------------------------------------------------------------------------------------------------------------")
        print("Usage Polygon <extent code> <shapefile name>")
        exit()

    # Get the extent for the CRS
    myResponse = requests.get(url+str(crsCode)+"/polygon")

    # For successful API call, response code will be 200 (OK)
    if(myResponse.ok):
        crsExtent = ogr.CreateGeometryFromJson(myResponse.text)
    else:
        # If response code is not ok (200), print the resulting http error code with description
        myResponse.raise_for_status()

    # NOTE: The following code does not test for errors, it is simply quick and dirty
    # -------------------------------------------------------------------------------

    # Now create a Shapefile such that we can visualize the data in ArcMAP or QGIS
    driver = ogr.GetDriverByName('ESRI Shapefile')
    ds = driver.CreateDataSource(shapeName+'.shp')
    layer = ds.CreateLayer('Polygon', geom_type=ogr.wkbPolygon)
    Field_Name = "P_Name"

    # Create a filed in the shapefile so we can name the elements we add
    field_testfield = ogr.FieldDefn(Field_Name, ogr.OFTString)
    field_testfield.SetWidth(50)
    layer.CreateField(field_testfield)

    # Create an element in the shape file for the geometry and name it
    if crsExtent.GetGeometryCount() == 1:
        feature = ogr.Feature(layer.GetLayerDefn())
        feature.SetField(Field_Name, 'Extent')
        feature.SetGeometry(crsExtent)
        layer.CreateFeature(feature)
    else:
        # Iterate elements and create all features returned
        index = 1
        for a in crsExtent:
            feature = ogr.Feature(layer.GetLayerDefn())
            feature.SetField(Field_Name, 'geometry'+str(index))
            index = index + 1
            feature.SetGeometry(a)
            layer.CreateFeature(feature)

    # Close the shape file
    ds = None


if __name__ == '__main__':
    main()
