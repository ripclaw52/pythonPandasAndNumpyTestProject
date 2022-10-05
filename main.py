import numpy as np
import pandas as pd
import plotly as po
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Display version for imported libraries
def library_version():
    print(f"numpy version: {np.__version__}\n"
          f"pandas version: {pd.__version__}\n"
          f"plotly version: {po.__version__}")

#LANG_CENSUS_DF = pd.read_csv("source-files/2016_Census_-_Dwelling_Unit_by_Language__Neighbourhood_Ward_.csv")
#CRIME_OCCUR_DF = pd.read_csv("source-files/Occurrences_Last_90_Days.csv")

'''Map chart with all the locations of the crime occurrences plotted'''
def read_crime_occurances_mapbox():
        df = pd.read_csv("source-files/Occurrences_Last_90_Days.csv")
        fig = px.scatter_mapbox(df,
                                lon=df['X'],
                                lat=df['Y'],
                                zoom=10,
                                color=df['Occurrence_Category'],
                                width=1200,
                                height=900,
                                title="Crime Occurences - Last 90 Days",
                                center=dict(
                                    lat=53.537667,
                                    lon=-113.496135),
                                labels={'Occurrence_Category': 'Category of Occurrence'},
                                )

        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(title_x=0.5)

        fig.show()

if __name__ == '__main__':
    library_version()

    read_crime_occurances_mapbox()