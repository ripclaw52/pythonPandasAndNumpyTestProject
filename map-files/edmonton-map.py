from urllib.request import urlopen
import json
import pandas as pd
import plotly.express as px

# Opens the downloaded Neighbourhoods geojson file
with open('City of Edmonton - Neighbourhoods.geojson', 'r') as f:
    neighbourhood = json.load(f)

'''
Feature IDs are required in GeoJSON, the Edmonton GeoJSON has the neighbourhood ID in the properties keys 
(the loaded geojson if basically a big dictionary so access values treat it like a dict). This code assigns each
neighbourhood with its respective ID. This for loop adds an ID key in the neighbourhood geojson with the 
neighbourhood's ID.
'''
# neighbourhoodID_List = []
i=0
for feature in neighbourhood["features"]:
    feature['id'] = int(neighbourhood["features"][i]['properties']['neighbourhood_number'])
    # neighbourhoodID_List.append(int(neighbourhood["features"][i]['properties']['neighbourhood_number']))
    i += 1
    # print(int(neighbourhood["features"][i]['properties']['neighbourhood_number']))


# print(counties["features"][0])
# print(int(neighbourhood["features"][0]['properties']['neighbourhood_number']))
# print(neighbourhood["features"][0]['id'])
# print(neighbourhood["features"][0])

df1 = pd.read_csv("2016_Census_-_Dwelling_Unit_by_Language__Neighbourhood_Ward_.csv")
#df2 = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv", dtype={"fips": str})

df1.head()
# print(df1.NeighbourhoodID)
# column_headers = list(df2.columns.values)
# print("The Column Header :", df1.iloc[[0]])

''' Sets up the choropleth map of Edmonton.
- geojson=neighbourhood, where neighbourhood is the loaded json from the GeoJSON file. The neighbourhood ID that was 
created in the for loop matches the neighbourhood ID in the dataframe column which is named 'NeighbourhoodID' in the
csv file.

- locations=df1.NeighbourhoodID, where df1.NeighbourhoodID accesses the column NeighbourhoodID in the CSV file. df1 is 
the data frame for the language by neighbourhood dataset, but we could use  different or multiple dataset (will have to 
merge the datasets if multiple were used, idk how to do this yet). To access columns in the dataFrame 

Helpful Resources:
- https://medium.com/tech-carnot/interactive-map-based-visualization-using-plotly-44e8ad419b97
- https://plotly.com/python/mapbox-county-choropleth/
- This-> https://stackoverflow.com/questions/60815784/map-with-choroplethmapbox-isnt-showing-in-dash 
  Then -> https://community.plotly.com/t/plot-a-shapefile-shp-in-a-choropleth-chart/27850
'''
fig = px.choropleth_mapbox(df1, geojson=neighbourhood, locations=df1.NeighbourhoodID, color=df1.Ward,
                           #color_continuous_scale="Viridis",
                           mapbox_style="carto-positron",
                           zoom=10, center={"lat": 53.545883, "lon": -113.490112},
                          )

fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()