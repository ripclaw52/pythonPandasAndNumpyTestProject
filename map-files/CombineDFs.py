import pandas as pd
import json
import plotly.express as px
from dash import Dash, html, dcc, Input, Output

# Data Frames initialization
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
# ==================================================================================================================== #
df_languages = pd.read_csv("2016_Census_-_Dwelling_Unit_by_Language__Neighbourhood_Ward_.csv", low_memory=False)

df_assessments = pd.read_csv('Property_Assessment_Data_2022.csv', low_memory=False)
df_assessments = df_assessments[(df_assessments['Assessment Class 1'] == 'RESIDENTIAL')]
df_neighbourhood_average = \
    df_assessment_filtered = df_assessments.groupby(['Neighbourhood', 'Neighbourhood ID'],
                                                    as_index=False)[
    ['Assessed Value', 'Latitude', 'Longitude']].mean()

df_columns1 = list(df_assessments.columns.values)
print(df_columns1)

pd.set_option('display.expand_frame_repr', False)
print(df_assessments.groupby(['Neighbourhood', 'Neighbourhood ID'],
                             as_index=False)[
          ['Assessed Value', 'Latitude', 'Longitude']].mean())

print("=============================================\n")
assessmentRange = [-1000000000000, 1000000000000]
df_neighbourhood_average_filtered = df_neighbourhood_average.loc[
    (assessmentRange[0] <= df_neighbourhood_average['Assessed Value']) & (
            df_neighbourhood_average['Assessed Value'] <= assessmentRange[1])
    ]

# Dataframe combination
df_combined = pd.concat([df_languages,
                         df_assessment_filtered.drop(columns="Neighbourhood")], axis='columns')

df_columns = list(df_combined.columns.values)
print(df_columns)

pd.set_option('display.expand_frame_repr', False)
print(df_combined)
# ==================================================================================================================== #
