import pandas as pd
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output

import modules.NeighbourhoodNameModule as nnm


#=================================================================================================================

crime_file = "./source-files/Occurrences_Last_90_Days.csv"
assessment_file = "./source-files/Property_Assessment_Data__Current_Calendar_Year_.csv"
languages_file = "./source-files/2016_Census_-_Dwelling_Unit_by_Language__Neighbourhood_Ward_.csv"

# create Pandas df and lists here
df_crimes = pd.read_csv(crime_file)
df_category = df_crimes.groupby(['Occurrence_Category'], as_index=False).size()

df_assessments = pd.read_csv(assessment_file)
df_assessments = df_assessments[(df_assessments['Assessment Class 1'] == 'RESIDENTIAL')]
neighbourhood_list = df_assessments['Neighbourhood'].unique()

df_neighbourhood_average = df_assessments.groupby(['Neighbourhood'], as_index=False)[['Assessed Value']].mean().round(0)
min_value = df_neighbourhood_average.min()[1]
max_value = df_neighbourhood_average.max()[1]

crimes_list = []

for item in df_category.values.tolist():
    crimes_list.append(item[0])




#===================================================================================================================

#APP LAYOUT
app = Dash(__name__)

app.layout = html.Div([
    html.Div([
        "Neighbourhood 1",
        dcc.Dropdown(
            neighbourhood_list,
            placeholder="Select a neighbourhood",
            id='neighbourhood-1-dropdown'
        ),
        html.Div(id='dd-1-output-container')
    ], style={}),
    html.Div([
        "Neighbourhood 2",
        dcc.Dropdown(
           neighbourhood_list,
           placeholder="Select a neighbourhood",
           id='neighbourhood-2-dropdown'
        ),
        html.Div(id='dd-2-output-container')
    ], style={})
], style={'margin': '50px', 'display': 'flex', 'flex-direction': 'row', 'width': 1400})


@app.callback(
    Output('dd-1-output-container', 'children'),
    [Input('neighbourhood-1-dropdown', 'value')],prevent_initial_call=True)
def update_output_1(value):
    return (
        f"You have selected {value}"
    )

@app.callback(
    Output('dd-2-output-container', 'children'),
    [Input('neighbourhood-2-dropdown', 'value')],prevent_initial_call=True)
def update_output_2(value):
    fig = nnm.findLanguagesInNeighbourhood(languages_file, value)
    return (
        dcc.Graph(figure=fig)
    )

if __name__ == '__main__':
    app.run_server(debug=True)