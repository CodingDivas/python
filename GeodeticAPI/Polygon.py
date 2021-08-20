# Python version 3.X
# This program will use the beta site of the GR to get two separate polygons and then create the
# intersection of the two.
# ------------------------------------------------------------------------------------------------------
import requests
from requests.auth import HTTPDigestAuth
from osgeo import ogr
import json
import sys

# The URL looks like this
# https://beta-api.epsg.org/api/v1/Extent/3180/polygon/
url = "https://apps.epsg.org/api/v1/Extent/"


def main():
    args = sys.argv[1:]
    if len(args) == 3:
        crsCode = args[0]
        tfmCode = args[1]
        shapeName = args[2]
    else:
        print("This application creates a shapefile containing the intersection of")
        print(
            "two given polygons. The Polygons are defined as extents in the EPSG database")
        print("and the extent codes need to exist in registry.")
        print("Currently data is retrieved from "+url)
        print("---------------------------------------------------------------------------------")
        print("Usage Polygon <extent code> <extent code> <shapefile name>")
        exit()

    # Get the extent for the CRS
    myResponse = requests.get(url+str(crsCode)+"/polygon")

    # For successful API call, response code will be 200 (OK)
    if(myResponse.ok):
        crsExtent = ogr.CreateGeometryFromJson(myResponse.text)
    else:
        # If response code is not ok (200), print the resulting http error code with description
        myResponse.raise_for_status()

    # Get the extent for the transformation
    myResponse = requests.get(url+str(tfmCode)+"/polygon")

    # For successful API call, response code will be 200 (OK)
    if(myResponse.ok):
        tfmExtent = ogr.CreateGeometryFromJson(myResponse.text)
    else:
        # If response code is not ok (200), print the resulting http error code with description
        myResponse.raise_for_status()

    # Create a new geometry showing the difference between the extent of ED50 / UTM zone 31N and ED50
    # or the part of the ED50 / UTM zone 31N extent that is not inside the extent for ED50.
    intersectionExtent = crsExtent.Intersection(tfmExtent)
    print("Resulting intersection has " +
          str(intersectionExtent.GetGeometryCount())+" geometries")
    if (intersectionExtent is None or intersectionExtent.IsEmpty()):
        print("The two extents do not intersect.")
        exit()

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

    # Create an elements in the shape file for the intersection geometry and name it
    print(intersectionExtent)
    if intersectionExtent.GetGeometryCount() == 1:
        feature = ogr.Feature(layer.GetLayerDefn())
        feature.SetField(Field_Name, 'Intersection')
        feature.SetGeometry(intersectionExtent)
        layer.CreateFeature(feature)
    else:
        index = 1
        for a in intersectionExtent:
            feature = ogr.Feature(layer.GetLayerDefn())
            feature.SetField(Field_Name, 'geometry'+str(index))
            index = index + 1
            feature.SetGeometry(a)
            layer.CreateFeature(feature)

    # Close the shape file
    ds = None


if __name__ == '__main__':
    main()
