import pandas as pd
import json
import plotly.express as px
from dash import Dash, html, dcc, Input, Output

# =================================================================================================================
pd.set_option('display.max_columns', 500)
# create Pandas df and lists here
df_crimes = pd.read_csv('Occurrences_Last_90_Days.csv', low_memory=False)
# df_crimes_category = df_crimes.groupby(['Occurrence_Category'], as_index=False).size()
# df_crimes_property = df_crimes[(df_crimes['Occurrence_Group'] == 'Property')]


df_assessments = pd.read_csv('Property_Assessment_Data_2022.csv', low_memory=False)
df_assessments = df_assessments[(df_assessments['Assessment Class 1'] == 'RESIDENTIAL')]
df_neighbourhood_average = \
df_assessments.groupby(['Neighbourhood', 'Neighbourhood ID'],
                       as_index=False)[
    ['Assessed Value', 'Latitude', 'Longitude']].mean()
# set 'neighbourhood' as a global value to avoid loading same data everytime
with open('City of Edmonton - Neighbourhoods.geojson', 'r') as f:
    neighbourhood = json.load(f)
# how to iterate through data frame:
# for index, row in df_neighbourhood_average.iterrows():
#     print(row['Neighbourhood'], row['Assessed Value'])
# =============================================================

min_value = df_neighbourhood_average.min()[1]
max_value = df_neighbourhood_average.max()[1]

crimes_list_map = df_crimes['Occurrence_Category'].unique()
crimes_color_map = dict(zip(crimes_list_map, px.colors.qualitative.G10))

neighbourhood_list = df_assessments['Neighbourhood'].unique()
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

        html.Label('Neighbourhoods Within Assessment Range',
                   style={'color': 'white', 'padding-bottom': 10}),

        dcc.Dropdown(options=neighbourhood_list,
                     placeholder='Enter Neighbourhood', id='Neighbourhood_input',
                     style={'marginRight': '10px', 'width': 350, 'padding-top': 10},
                     ),

        html.Br(),
        html.Br(),
        html.Label('Crime Statistics', style={'color': 'white', 'padding': 0}),
        dcc.Dropdown(crimes_list_map, id='crime_dropdown', multi=True,
                     style={'marginRight': '10px', 'width': 350, 'padding-top': 0}),

    ], style={'padding': 30, 'background': '#1C6387', 'width': '25vw'}),

    html.Div(children=[

        html.Label('Neighbourhood Assessment Average', style={'color': '#1C6387', 'padding': 25}),
        html.Div(children=[
            dcc.RangeSlider(
                min=100000,
                max=1000000,
                step=25000,
                value=[150000, 450000],
                id='Neighbourhood_Average'),
        ], style={'padding': '0, 20, 10', 'color': '#1C6387'}),


        html.Div([
            dcc.Loading(
                dcc.Graph(id='the_graph', config={'doubleClick': 'reset', 'showTips': True, 'displayModeBar': False,
                                                  'watermark': False}))
        ], style={'padding': 0, 'flex': 1})

    ], style={'width': '55vw', 'flex': 1}),
], id='Container', style={'display': 'flex', 'flex-direction': 'row', 'height': '95vh', 'padding-right': 10})


@app.callback(
    Output('the_graph', 'figure'),
    Output('Neighbourhood_input', 'options'),
    Input('Neighbourhood_input', 'value'),
    Input('Neighbourhood_Average', 'value'),
    Input('the_graph', 'clickData'),
    Input('crime_dropdown', 'value'),)
def update_output(neighbourhoodName, assessmentRange, clickData, crime_dropdown):

    # filters the df_neighbourhood_average based on the range in the slider
    df_neighbourhood_average_filtered = df_neighbourhood_average.loc[
        (assessmentRange[0] <= df_neighbourhood_average['Assessed Value']) & (
                df_neighbourhood_average['Assessed Value'] <= assessmentRange[1])
        ]

    df_neighbourhood_average_filtered = df_neighbourhood_average_filtered.rename(
        columns={'Neighbourhood': 'NeighbourhoodName', 'Neighbourhood ID': 'NeighbourhoodID',
                 'Assessed Value': 'AssessedValue'})
    df_neighbourhood_average_filtered.AssessedValue = df_neighbourhood_average_filtered.AssessedValue.round()
    # print(df_neighbourhood_average_filtered.AssessedValue)
    df_neighbourhood_average_filtered['NeighbourhoodID'] = df_neighbourhood_average_filtered['NeighbourhoodID'].astype(
        int).astype(str)

    df_neighbourhood_average_filtered['Legend'] = 'Neighbourhoods'
    zoom = 9.8
    center = {"lat": 53.545883, "lon": -113.490112}

    # on click of neighbourhood
    if clickData:
        click_location = clickData['points'][0]['location']
        click_filter = df_neighbourhood_average_filtered['NeighbourhoodID'] == click_location
        df_neighbourhood_average_filtered.loc[click_filter, 'Legend'] = 'Clicked Neighbourhood'
        center = {"lat": clickData['points'][0]['customdata'][3], "lon": clickData['points'][0]['customdata'][2]}
        zoom = 13.3

    #on select of neighbourhood search
    if neighbourhoodName:
        select_name_filter = df_neighbourhood_average_filtered['NeighbourhoodName'] == neighbourhoodName
        df_neighbourhood_average_filtered.loc[select_name_filter, 'Legend'] = 'Selected Neighbourhood'


    # ================================================================================================================#
    # neighbourhoodID_List = []
    i = 0
    for feature in neighbourhood["features"]:
        feature['id'] = int(neighbourhood["features"][i]['properties']['neighbourhood_number'])
        i += 1
    fig = px.choropleth_mapbox(df_neighbourhood_average_filtered, geojson=neighbourhood,
                               locations=df_neighbourhood_average_filtered.NeighbourhoodID,
                               color='Legend',
                               mapbox_style='open-street-map',
                               zoom=zoom,
                               center=center,
                               height=800, opacity=0.25,
                               hover_data=['NeighbourhoodName', 'AssessedValue'],
                               color_discrete_map={'Selected Neighbourhood': "green",
                                                   'Clicked Neighbourhood': 'yellow', "Neighbourhoods": 'purple'},
                               custom_data=['NeighbourhoodName', 'AssessedValue', 'Longitude', 'Latitude'],

                               )
    if crime_dropdown:
        for crime_cat in crime_dropdown:
            this_crime_df = df_crimes.loc[df_crimes['Occurrence_Category'] == crime_cat]
            fig.add_scattermapbox(
                below=False,
                lon=this_crime_df.X.values.tolist(),
                lat=this_crime_df.Y.values.tolist(),
                hovertext=crime_cat,
                marker_size=10,
                marker_color=crimes_color_map[crime_cat],
                showlegend=True,
                name=crime_cat,
                hoverinfo='text',
            )
    # fig.update_geos(fitbounds="locations")
    # fig.update_traces(cluster=dict(enabled=True))
    fig.update_layout(margin={"r": 0, "t": 20, "l": 20, "b": 20},
                      legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
    return fig, df_neighbourhood_average_filtered['NeighbourhoodName'].unique()


if __name__ == '__main__':
    app.run_server(debug=True)
