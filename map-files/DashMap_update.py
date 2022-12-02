import pandas as pd
import json
import plotly.express as px
from dash import Dash, html, dcc, Input, Output

# =================================================================================================================

# create Pandas df and lists here
df_crimes = pd.read_csv('../../Occurrences_Last_90_Days.csv', low_memory=False)
df_crimes_category = df_crimes.groupby(['Occurrence_Category'], as_index=False).size()
df_crimes_property = df_crimes[(df_crimes['Occurrence_Group'] == 'Property')]

# print(df_crimes_property)

df_assessments = pd.read_csv('Property_Assessment_Data_2022.csv', low_memory=False)
df_assessments = df_assessments[(df_assessments['Assessment Class 1'] == 'RESIDENTIAL')]
df_neighbourhood_average = \
df_assessments.groupby(['Neighbourhood', 'Neighbourhood ID'],
                       as_index=False)[
    ['Assessed Value', 'Latitude', 'Longitude']].mean()

pd.set_option('display.expand_frame_repr', False)
print(df_assessments)

# set 'neighbourhood' as a global value to avoid loading same data everytime
with open('City of Edmonton - Neighbourhoods.geojson', 'r') as f:
    neighbourhood = json.load(f)


# =============================================================

min_value = df_neighbourhood_average.min()[1]
max_value = df_neighbourhood_average.max()[1]

crimes_list = []

for item in df_crimes_category.values.tolist():
    crimes_list.append(item[0])

neighbourhood_list = df_assessments['Neighbourhood'].unique()
# ===================================================================================================================

# APP LAYOUT
app = Dash(__name__)

app.layout = html.Div([

    html.Div(children=[
        html.Label('Moving to Edmonton Made Easy',
                   style={
                       'color': 'white',
                       'padding': '30, 30, 30, 30',
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

        dcc.Dropdown(options=neighbourhood_list,
                     placeholder='Enter Neighbourhood', id='Neighbourhood_input',
                     style={'marginRight': '10px', 'width': 350, 'padding-top': 10},
                     ),

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
                step=25000,
                #value=[150000, 450000],
                value=[-1500000, 10000000],
                id='Neighbourhood_Average'),
        ], style={'padding': '0, 20, 10', 'color': '#1C6387'}),

        # html.Br(),
        # dcc.RadioItems(['Residential', 'Commercial']),

        # html.Div(children=[
        #     dcc.RadioItems(['Residential', 'Commercial']),
        # ], style={'text-align-last': 'end', 'color': '#1C6387'}),

        html.Div([
            dcc.Loading(
                dcc.Graph(id='the_graph', config={'doubleClick': 'reset', 'showTips': True, 'displayModeBar': False,
                                                  'watermark': False}))
        ], style={'padding': 0, 'flex': 1})

    ], style={'width': '55vw', 'flex': 1}),
], id='Container', style={'display': 'flex', 'flex-direction': 'row', 'height': '95vh', 'padding-right': 10})


@app.callback(
    Output('the_graph', 'figure'),
    Input('Neighbourhood_input', 'value'),
    Input('Neighbourhood_Average', 'value'),
    Input('the_graph', 'clickData'))
def update_output(neighbourhoodName, assessmentRange, clickData):
    # filters the df_neighbourhood_average based on the range in the slider
    df_neighbourhood_average_filtered = df_neighbourhood_average.loc[
        (assessmentRange[0] <= df_neighbourhood_average['Assessed Value']) & (
                df_neighbourhood_average['Assessed Value'] <= assessmentRange[1])
        ]

    df_neighbourhood_average_filtered = df_neighbourhood_average_filtered.rename(
        columns={'Neighbourhood': 'NeighbourhoodName', 'Neighbourhood ID': 'NeighbourhoodID'})
    print("=============Here===============")
    print(df_neighbourhood_average_filtered)

    df_neighbourhood_average_filtered['NeighbourhoodID'] = df_neighbourhood_average_filtered['NeighbourhoodID'].astype(
        int).astype(str)
    # print(df_neighbourhood_average_filtered['NeighbourhoodID'])

    df_neighbourhood_average_filtered['color'] = 'red'
    zoom = 9.8
    center = {"lat": 53.545883, "lon": -113.490112}

    #click on neighbourhood
    if clickData:
        click_location = clickData['points'][0]['location']
        print(click_location)
        click_filter = df_neighbourhood_average_filtered['NeighbourhoodID'] == click_location
        print(click_filter)
        df_neighbourhood_average_filtered.loc[click_filter, 'color'] = 'yellow'
        center = {"lat": clickData['points'][0]['customdata'][3], "lon": clickData['points'][0]['customdata'][2]}
        zoom = 13.3

    #highlight neighbourhood name selected.
    if neighbourhoodName:
        select_name_filter = df_neighbourhood_average_filtered['NeighbourhoodName'] == neighbourhoodName
        print(select_name_filter)
        df_neighbourhood_average_filtered.loc[select_name_filter, 'color'] = 'green'


    # =====================================================================================================================#
    # neighbourhoodID_List = []
    i = 0
    for feature in neighbourhood["features"]:
        feature['id'] = int(neighbourhood["features"][i]['properties']['neighbourhood_number'])
        i += 1

    fig = px.choropleth_mapbox(df_neighbourhood_average_filtered, geojson=neighbourhood,
                               locations=df_neighbourhood_average_filtered.NeighbourhoodID,
                               color='color',
                               mapbox_style='open-street-map',
                               zoom=zoom,
                               center=center,
                               height=800, opacity=0.25,
                               hover_name="NeighbourhoodName",
                               hover_data={'Assessed Value': True, 'color': False},
                               color_discrete_map={'green': "green", 'yellow': 'yellow', "red": 'purple'},
                               custom_data=['NeighbourhoodName', 'Assessed Value', 'Longitude', 'Latitude'],
                               )

    fig.update_geos(fitbounds="locations")
    fig.update_layout(coloraxis_showscale=False, showlegend=False, margin={"r": 0, "t": 20, "l": 20, "b": 20})
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
