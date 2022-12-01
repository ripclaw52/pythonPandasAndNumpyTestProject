import pandas as pd
import json
import plotly
import plotly.express as px
from dash import Dash, html, dcc, Input, Output

# =================================================================================================================

# create Pandas df and lists here
df_crimes = pd.read_csv('Occurrences_Last_90_Days.csv', low_memory=False)
df_category = df_crimes.groupby(['Occurrence_Category'], as_index=False).size()

df_assessments = pd.read_csv('Property_Assessment_Data_2022.csv', low_memory=False)
df_assessments = df_assessments[(df_assessments['Assessment Class 1'] == 'RESIDENTIAL')]
df_neighbourhood_average = df_assessments.groupby(['Neighbourhood', 'Neighbourhood ID'], as_index=False)[['Assessed Value']].mean().round(0)

# how to iterate through data frame:
# for index, row in df_neighbourhood_average.iterrows():
#     print(row['Neighbourhood'], row['Assessed Value'])
# =============================================================

min_value = df_neighbourhood_average.min()[1]
max_value = df_neighbourhood_average.max()[1]

crimes_list = []

for item in df_category.values.tolist():
    crimes_list.append(item[0])

# ===================================================================================================================

# APP LAYOUT
app = Dash(__name__)

app.layout = html.Div([

    html.Div(children=[
        html.Label('Moving to Edmonton Made Easy',
                   style={
                       'color': 'white',
                       'padding': '30, 30, 30, 0',
                       'width': 60,
                       'font': 'Poppins',
                       'font-size': 25,
                       'text-align': 'center',
                   }),
        html.Br(),
        html.Br(),
        html.Br(),

        html.Label('Neighbourhood Search',
                   style={'color': 'white', 'padding-bottom': 10}),

        dcc.Input(placeholder='Enter Neighbourhood', type='text', id='Neighbourhood_input', value='',
                  style={'marginRight': '10px', 'width': 350, 'padding-top': 10}),

        html.Br(),
        html.Br(),
        html.Label('Crime Statistics', style={'color': 'white', 'padding': 0}),
        dcc.Dropdown(crimes_list, id='crime_dropdown', multi=True,
                     style={'marginRight': '10px', 'width': 350, 'padding-top': 0}),

    ], style={'padding': 30, 'background': '#1C6387', 'width': '25vw'}),

    html.Div(children=[

        html.Label('Neighbourhood Assessment Average', style={'color': '#1C6387', 'padding': 25}),
        html.Div(children=[
            dcc.RangeSlider(
                min=100000,
                max=1000000,
                value=[250000, 300000],
                id='Neighbourhood_Average'),
        ], style={'padding': '0, 20, 10', 'color': '#1C6387'}),

        # html.Br(),
        # dcc.RadioItems(['Residential', 'Commercial']),

        html.Div(children=[
            dcc.RadioItems(['Residential', 'Commercial']),
        ], style={'text-align-last': 'end', 'color': '#1C6387'}),

        html.Div([
            dcc.Graph(id='the_graph', config={'doubleClick': 'reset', 'showTips': True, 'displayModeBar': False,
                                              'watermark': False})
        ], style={'padding': 0, 'flex': 1})

    ], style={'width': '55vw', 'flex': 1}),
], id='Container', style={'display': 'flex', 'flex-direction': 'row', 'height': '95vh', 'padding-right': 10})


@app.callback(
    Output('the_graph', 'figure'),
    [Input('Neighbourhood_input', 'value'),
     Input('Neighbourhood_Average', 'value')])
def update_output(neighbourhoodName, assessmentRange):
    print(assessmentRange)
    df_neighbourhood_average_filtered = df_neighbourhood_average[
        (assessmentRange[0] <= df_neighbourhood_average['Assessed Value']) & (df_neighbourhood_average['Assessed Value'] <= assessmentRange[1])
    ]
    #print(df_neighbourhood_average_filtered[:5])
    print(df_neighbourhood_average_filtered)

    # scatterplot = px.scatter(
    #     data_frame = df_neighbourhood_average_filtered,
    #     x="Neighbourhood",
    #     y="Assessed Value",
    #     hover_data=["Neighbourhood"],
    #     text="Neighbourhood",
    #     height=550,
    #     width = 1100
    # )
    #
    # scatterplot.update_traces(textposition='top center')
    # return (scatterplot)

    #==================================================================================================================#

    with open('City of Edmonton - Neighbourhoods.geojson', 'r') as f:
        neighbourhood = json.load(f)

    # neighbourhoodID_List = []
    i = 0
    for feature in neighbourhood["features"]:
        feature['id'] = int(neighbourhood["features"][i]['properties']['neighbourhood_number'])
        i += 1

    df1 = pd.read_csv("2016_Census_-_Dwelling_Unit_by_Language__Neighbourhood_Ward_.csv", low_memory=False)

    df1.head()
    fig = px.choropleth_mapbox(df1, geojson=neighbourhood, locations=df1.NeighbourhoodID,
                               color=df1.Neighbourhood == neighbourhoodName,
                               mapbox_style='open-street-map',
                               zoom=9.8, center={"lat": 53.545883, "lon": -113.490112},
                               labels=df1.NeighbourhoodName,
                               height=872, hover_name=df1.NeighbourhoodName, opacity=0.25
                               )

    fig.update_geos(fitbounds="locations")
    fig.update_layout(coloraxis_showscale=False, showlegend=False, margin={"r": 0, "t": 20, "l": 20, "b": 20})
    # fig.show()
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
