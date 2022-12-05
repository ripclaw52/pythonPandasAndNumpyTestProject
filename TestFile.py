import pandas as pd
import json
import plotly.express as px
from dash import Dash, html, dcc, Input, Output

# ==================================================================================================================== #
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
# ==================================================================================================================== #
# MAIN PAGE DATAFRAMES AND DATA PREPROCESSING
# ==================================================================================================================== #
# CRIMES DATAFRAME
df_crimes = pd.read_csv('./source-files/Occurrences_Last_90_Days.csv', low_memory=False)
df_crimes_category = df_crimes.groupby(['Occurrence_Category'], as_index=False).size()


# df_crimes_property = df_crimes[(df_crimes['Occurrence_Group'] == 'Property')]
# print(df_crimes_property)

def occurence_group_controller(crime_stats):
    new_df = df_crimes[df_crimes.Occurrence_Category == crime_stats]

    dfg = new_df.groupby('Occurrence_Group').count().reset_index()

    return dfg["Occurrence_Group"].values.tolist()


def occurence_group_type_controller(occurence_group):
    new_df = df_crimes[df_crimes.Occurrence_Group == occurence_group]

    dfg = new_df.groupby('Occurrence_Type_Group').count().reset_index()

    return dfg["Occurrence_Type_Group"].values.tolist()


def mapped_crime_list():
    ret = {"Disorder": occurence_group_controller("Disorder"),
           "Non-Violent": occurence_group_controller("Non-Violent"),
           "Violent": occurence_group_controller("Violent"),
           "Traffic": occurence_group_controller("Traffic"),
           "Weapons": occurence_group_controller("Weapons"),
           "Drugs": occurence_group_controller("Drugs"),
           "Other": occurence_group_controller("Other")}

    return ret

# crimes_list = []
# for item in df_crimes_category.values.tolist():
#     crimes_list.append(item[0])
crimes_list = df_crimes['Occurrence_Category'].unique()
crimes_color_map = dict(zip(crimes_list, px.colors.qualitative.G10))

# ==================================================================================================================== #
# LANGUAGES DATAFRAME
df_languages = pd.read_csv("./source-files/2016_Census_-_Dwelling_Unit_by_Language__Neighbourhood_Ward_.csv",
                           low_memory=False)
languages_list = df_languages.columns.values[4:14]
# print(languages_list)

# ==================================================================================================================== #
# ASSESSMENT VALUE DATAFRAME
df_assessments = pd.read_csv('./source-files/Property_Assessment_Data_2022.csv', low_memory=False)
df_assessments = df_assessments[(df_assessments['Assessment Class 1'] == 'RESIDENTIAL')]
df_neighbourhood_average = df_assessments.groupby(['Neighbourhood', 'Neighbourhood ID'], as_index=False)[
        ['Assessed Value', 'Latitude', 'Longitude']].mean()

min_value = df_neighbourhood_average.min()[1]
max_value = df_neighbourhood_average.max()[1]

neighbourhood_list = df_assessments['Neighbourhood'].unique()

# ==================================================================================================================== #
# NEIGHBOURHOOD GEOJSON FOR CHOROPLETH MAP
# set 'neighbourhood' as a global value to avoid loading same data everytime
with open('./source-files/City of Edmonton - Neighbourhoods.geojson', 'r') as f:
    neighbourhood = json.load(f)

# ==================================================================================================================== #
# COMPARISON PAGE DATAFRAMES AND SETUP
# ==================================================================================================================== #
# colours
bg_assessedValue = "#1C6387"
fg_assessedValue = "white"

assessment_file = "./source-files/Property_Assessment_Data__Current_Calendar_Year_.csv"
languages_file = "./source-files/2016_Census_-_Dwelling_Unit_by_Language__Neighbourhood_Ward_.csv"

column_header_lan = list(df_languages.columns.values)

df_neighbourhood_average_comparison = df_assessments.groupby(['Neighbourhood'],
                                                             as_index=False)[['Assessed Value']].mean().round(0)


#===================================================================================================================

def create_graph_languages(value):
    df = pd.read_csv(languages_file)
    dff = df.loc[df['Neighbourhood Name'] == value]
    headers = list(dff.columns.values)[4:14]
    values = [
        dff.iloc[0,  4], dff.iloc[0,  5], dff.iloc[0,  6], dff.iloc[0,  7],
        dff.iloc[0,  8], dff.iloc[0,  9], dff.iloc[0, 10], dff.iloc[0, 11],
        dff.iloc[0, 12], dff.iloc[0, 13],
    ]
    column_headers = headers[::-1]
    value_list = values[::-1]
    #print(f"{len(column_headers)} & {len(value_list)}")

    fig = go.Figure(
        data=[go.Bar(
            x=value_list,
            y=column_headers,
            orientation="h",)
        ],
        layout=go.Layout(margin=dict(l=5, r=5, t=35, b=5)),
    )
    config = dict({'displayModeBar': False})

    return fig

def create_average_assessment(value):
    residential = "RESIDENTIAL"
    df = pd.read_csv(assessment_file)
    dff = df.query("`Neighbourhood`==@value & `Assessment Class % 1`==100 & `Assessment Class 1`==@residential")["Assessed Value"]
    average = dff.mean()
    currency_string = "${:,.2f}".format(average)
    return currency_string

# ==================================================================================================================== #
# DASH APP INTERFACE SETUP
# ==================================================================================================================== #

# APP LAYOUT
app = Dash(__name__)

app.layout = html.Div({

    html.Div(children=[
        dcc.RadioItems(options=['Main Page', 'Comparison'],
                       value='Main Page',
                       persistence=True,
                       style={'text-align-last': 'end', 'color': '#1C6387', 'position': 'absolute', 'right': 10},
                       id='change_page')
    ]),

    # MAIN PAGE
    html.Div(children=[

        html.Div(children=[
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

                html.Label('Neighbourhoods Within Assessment Range', style={'color': 'white', 'padding-bottom': 10}),

                dcc.Dropdown(options=neighbourhood_list,
                             placeholder='Enter Neighbourhood', id='Neighbourhood_input',
                             style={'marginRight': '10px', 'width': 350, 'padding-top': 10},
                             ),

                html.Br(),
                html.Br(),
                html.Label('Crime Statistics', style={'color': 'white', 'padding': 0}),
                dcc.Dropdown(crimes_list, id='crime_dropdown', multi=True,
                             style={'marginRight': '10px', 'width': 350, 'padding-top': 0}),

            ], id='map_filters', style={'padding': 30, 'background': '#1C6387'}),

            html.Div(children=[

                html.Label('Neighbourhood Assessment Average', style={'color': '#1C6387', 'padding': 25}),
                html.Div(children=[
                    dcc.RangeSlider(
                        min=100000,
                        max=1000000,
                        step=25000,
                        value=[150000, 450000],
                        id='Neighbourhood_Average'),
                ], style={'color': '#1C6387'}),

                # Contains Map graph and progress indicator
                html.Div([
                    dcc.Loading(
                        dcc.Graph(id='the_graph',
                                  config={'doubleClick': 'reset', 'showTips': True, 'displayModeBar': False,
                                          'watermark': False}, style={'height': 550})),

                ], id='map_container', style={'padding': 0, 'flex': 1}),

            ], id='map_slider_container', style={'width': '55vw', 'flex': 1}),
        ], id='top-container', style={'display': 'flex', 'flex-direction': 'row', 'height': '60vh'}),

        # ============================================================================================================ #
        # Bottom DIV
        html.Div(children=[

            # Filter
            html.Div(children=[
                html.Label('Greater Edmonton Crime filter',
                           style={
                               'color': 'white',
                               'width': 60,
                               'font': 'Poppins',
                               'font-size': 25,
                               'text-align': 'center',
                           }),

                html.Br(),
                html.Br(),

                dcc.RadioItems(
                    labelStyle={'display': 'block'},
                    id='general_crime',
                    options=[{'label': k, 'value': k} for k in mapped_crime_list().keys()],
                    value='Disorder',
                    style={'color': 'white', 'padding': '10, 0'}
                ),

                html.Hr(),

                dcc.RadioItems(
                    id='descriptive_crime', style={'color': 'white', 'display': 'inline-grid'}
                    # labelStyle={'display': 'block'},
                ),

                html.Hr(),

                html.Div(id='display-selected-values')

            ], id='crime_filters',
                style={'padding': 15, 'background': '#1C6387', 'position': 'relative', 'width': 390}),

            # Bottom Graphs
            html.Div(children=[

                # Crime graphs
                dcc.Loading(
                    dcc.Graph(id='crime_cat_graph', config={'doubleClick': 'reset', 'showTips': True,
                                                            'displayModeBar': False, 'watermark': False},
                              style={'flex-grow': 1})),
                dcc.Loading(
                    dcc.Graph(id='crime_occur_graph', config={'doubleClick': 'reset', 'showTips': True,
                                                              'displayModeBar': False, 'watermark': False},
                              style={'flex-grow': 1, 'margin-left': 25,
                                     'border-right': '1px solid #ccc',
                                     'padding-right': 75})),

                html.Hr(),
                # html.Hr(),

                # Language graph
                html.Div(children=[
                    dcc.Dropdown(options=languages_list,
                                 placeholder='Languages', id='Languages_dropdown', value='French',
                                 # style={'width': 250},
                                 ),
                    # html.Div([
                    dcc.Loading(
                        dcc.Graph(id='language_graph', config={'doubleClick': 'reset', 'showTips': True,
                                                               'displayModeBar': False, 'watermark': False})),
                    # style={'padding': 0, 'flex': 1, 'display': 'inline-flex', 'float': 'right'})),
                    # ], id='graphs_container', style={'padding': 0, 'flex': 1, 'display': 'inline-flex', 'float': 'right'}),
                ], id='language-dropdown-cont', style={'flex-grow': 1, 'padding-right': 10}),
            ], id='bottom_graphs',
                style={'display': 'flex', 'align-items': 'flex-end', 'width': '72vw', 'flex-wrap': 'wrap'
                    , 'flex-direction': 'row', 'justify-content': 'space-around'}),

        ], id='bottom_container', style={'display': 'flex', 'flex-direction': 'row', 'height': '33.51vh',
                                         'flex-wrap': 'wrap', 'justify-content': 'space-between', 'padding-top': 16,
                                         'padding-bottom': 10}),
    ], id='main-page-container', style={'display': 'block'}),

    # COMPARISON
    html.Div([
        html.Div([
            html.Div([
                dcc.Dropdown(
                    neighbourhood_list,
                    multi=False,
                    searchable=True,
                    placeholder="Select a neighbourhood",
                    id='dd_selection1',
                    value="CRESTWOOD",
                ),
            ], style={}),
            html.Div([
                html.Div([
                    html.Div(id='a_text1', style={'color': fg_assessedValue}),
                ], style={'margin': '25px', 'padding': '25px', 'border-radius': '10px', 'text-align': 'center',
                          'background-color': bg_assessedValue}),
                dcc.Graph(id='l_graph1'),
            ]),
        ], style={'margin': '25px', 'display': 'flex', 'flex-direction': 'column', 'width': '100%', }),

        html.Div([
            html.Div([
                dcc.Dropdown(
                    neighbourhood_list,
                    multi=False,
                    searchable=True,
                    placeholder="Select a neighbourhood",
                    id='dd_selection2',
                    value="RIVERDALE",
                ),
            ], style={}),
            html.Div([
                html.Div([
                    html.Div(id='a_text2', style={'color': fg_assessedValue})
                ], style={'margin': '25px', 'padding': '25px', 'border-radius': '10px', 'text-align': 'center',
                          'background-color': bg_assessedValue}),
                dcc.Graph(id='l_graph2'),
            ]),
        ], style={'margin': '25px', 'display': 'flex', 'flex-direction': 'column', 'width': '100%', }),

        html.Div([
            html.Div([
                dcc.Dropdown(
                    neighbourhood_list,
                    multi=False,
                    searchable=True,
                    placeholder="Select a neighbourhood",
                    id='dd_selection3',
                    value="MACEWAN",
                ),
            ], style={}),
            html.Div([
                html.Div([
                    html.Div(id='a_text3', style={'color': fg_assessedValue})
                ], style={'margin': '25px', 'padding': '25px', 'border-radius': '10px', 'text-align': 'center',
                          'background-color': bg_assessedValue}),
                dcc.Graph(id='l_graph3'),
            ]),
        ], style={'margin': '25px', 'display': 'flex', 'flex-direction': 'column', 'width': '100%', }),
    ], id='comparison-page-container', style={'margin': '25px', 'display': 'none', 'flex-direction': 'row', })

}, id='main-container', style={'display': 'block', 'padding': 4})


# ==================================================================================================================== #
# PAGES INTERFACE

@app.callback(
    Output('main-page-container', 'style'),
    [Input('change_page', 'value')])
def switch_pages(switch_to_page):
    if switch_to_page == 'Main Page':
        return {'display': 'block'}
    if switch_to_page == 'Comparison':
        return {'display': 'none'}


# ==================================================================================================================== #
# MAIN PAGE CALL BACKS
# ==================================================================================================================== #
# CRIME GRAPH INTERFACE

@app.callback(
    Output('descriptive_crime', 'options'),
    [Input('general_crime', 'value')])
def set_general_crime_options(general_crime):
    return [{'label': i, 'value': i} for i in mapped_crime_list()[general_crime]]


@app.callback(
    Output('crime_cat_graph', 'figure'),
    [Input('general_crime', 'value')])
def general_crimes(general_crime):
    dff = df_crimes
    new_df = dff[dff.Occurrence_Category == general_crime]

    dfg = new_df.groupby('Occurrence_Group').count().reset_index()
    dfg = dfg.rename(columns={"Occurrence_Type_Group": "Occurrences"})

    barchart = px.bar(
        data_frame=dfg,
        x='Occurrences',
        y='Occurrence_Group',
        title=f"{general_crime}" + " Last 90 Days",
        opacity=0.9,
        orientation="h",
        width=400,
        height=300,
    )

    barchart.update_layout(
        margin=dict(l=5, r=5, t=35, b=5),
        title_font_size=12,
        # title_y=0.8,
        xaxis=dict(
            title='Crime Category Subclass',
            titlefont_size=10,
            tickfont_size=8,
        ),
        yaxis=dict(
            title='Occurrences',
            titlefont_size=10,
            tickfont_size=8,
        ),
        barmode='group',
        bargap=0.15,  # gap between bars of adjacent location coordinates.
        bargroupgap=0.1,  # gap between bars of the same location coordinate.
        showlegend=False,
    )
    barchart.update_layout(yaxis={'categoryorder': 'total ascending'})
    barchart.update_traces(textposition='outside')
    return barchart


@app.callback(
    Output('crime_occur_graph', 'figure'),
    [Input('descriptive_crime', 'value')])
def update_crime_occur_graph(descriptive_crime):
    dff = df_crimes
    new_df = dff[dff.Occurrence_Group == descriptive_crime]

    dfg = new_df.groupby('Occurrence_Type_Group').count().reset_index()
    dfg = dfg.rename(columns={"Occurrence_Type_Group": "occurences"})

    barchart = px.bar(
        data_frame=dfg,
        x='Occurrence_Group',
        y='occurences',
        title=f"{descriptive_crime}" + " Last 90 Days",
        opacity=0.9,
        orientation="h",
        width=400,
        height=300,
    )

    barchart.update_layout(
        margin=dict(l=5, r=5, t=35, b=5),
        title_font_size=12,
        # title_y=0.8,
        xaxis=dict(
            title='Crime Category',
            titlefont_size=10,
            tickfont_size=8,
        ),
        yaxis=dict(
            title='Occurrences',
            titlefont_size=10,
            tickfont_size=8,
        ),
        barmode='group',
        bargap=0.15,  # gap between bars of adjacent location coordinates.
        bargroupgap=0.1,  # gap between bars of the same location coordinate.
        showlegend=False,
    )
    barchart.update_layout(yaxis={'categoryorder': 'total ascending'})
    barchart.update_traces(textposition='outside')
    return barchart


# ==================================================================================================================== #
# LANGUAGE GRAPH INTERFACE
@app.callback(
    Output('language_graph', 'figure'),
    Input('Languages_dropdown', 'value'))
def language_output(language):
    df_languages = pd.read_csv("./source-files/2016_Census_-_Dwelling_Unit_by_Language__Neighbourhood_Ward_.csv")
    df_languages_sorted = df_languages.sort_values(by=[language], ascending=False)

    df_languages_sorted = df_languages_sorted.head(5)
    # print(df_languages_sorted)
    # print(df_languages_sorted[language])

    # if language == 'Tagalog (Pilipino, Filipino)':
    #     language = 'Filipino'
    # if language == 'North American Indigenous':
    #     language = 'N.A. Indigenous'

    # print(df_languages_sorted[::-1])
    # # print(language)
    # print(df_languages_sorted.French[::-1])
    barchart = px.bar(
        data_frame=df_languages_sorted,
        x=language,
        y=df_languages_sorted.Neighbourhood,
        opacity=0.9,
        orientation="h",
        width=400,
        height=300,
        title=f"Top 5 {language}-speaking Neighbourhoods",
        hover_name=language, hover_data=[language]
    )

    barchart.update_layout(
        margin=dict(l=5, r=5, t=35, b=5),
        title_font_size=12,
        # title_y=0.8,
        xaxis=dict(
            title=f'{language} Households',
            titlefont_size=10,
            tickfont_size=8,
        ),
        yaxis=dict(
            title='Neighbourhoods',
            titlefont_size=10,
            tickfont_size=8,
        ),
        barmode='group',
        bargap=0.15,  # gap between bars of adjacent location coordinates.
        bargroupgap=0.1,  # gap between bars of the same location coordinate.
        showlegend=False,
    )
    barchart.update_layout(yaxis={'categoryorder': 'total ascending'})
    barchart.update_traces(textposition='outside')
    return barchart


# ==================================================================================================================== #
# CHOROPLETH MAP INTERFACE
@app.callback(
    Output('the_graph', 'figure'),
    Output('Neighbourhood_input', 'options'),
    Input('Neighbourhood_input', 'value'),
    Input('Neighbourhood_Average', 'value'),
    Input('the_graph', 'clickData'),
    Input('crime_dropdown', 'value'))
def update_output(neighbourhoodName, assessmentRange, clickData, crime_dropdown):
    # filters the df_neighbourhood_average based on the range in the slider
    df_neighbourhood_average_filtered = df_neighbourhood_average.loc[
        (assessmentRange[0] <= df_neighbourhood_average['Assessed Value']) & (
                df_neighbourhood_average['Assessed Value'] <= assessmentRange[1])
        ]

    df_neighbourhood_average_filtered = df_neighbourhood_average_filtered.rename(
        columns={'Neighbourhood': 'NeighbourhoodName', 'Neighbourhood ID': 'NeighbourhoodID',
                 'Assessed Value': 'AssessedValue'})
    # print(df_neighbourhood_average_filtered)
    df_neighbourhood_average_filtered['NeighbourhoodID'] = df_neighbourhood_average_filtered['NeighbourhoodID'].astype(
        int).astype(str)
    # print(df_neighbourhood_average_filtered['NeighbourhoodID'])

    df_neighbourhood_average_filtered['Legend'] = 'Neighbourhoods'
    zoom = 9.2
    center = {"lat": 53.545883, "lon": -113.490112}

    # click on neighbourhood
    if clickData:
        click_location = clickData['points'][0]['location']
        print(click_location)
        click_filter = df_neighbourhood_average_filtered['NeighbourhoodID'] == click_location
        print(click_filter)
        df_neighbourhood_average_filtered.loc[click_filter, 'color'] = 'yellow'
        center = {"lat": clickData['points'][0]['customdata'][3], "lon": clickData['points'][0]['customdata'][2]}
        zoom = 13.3

    # highlight neighbourhood name selected.
    if neighbourhoodName:
        select_name_filter = df_neighbourhood_average_filtered['NeighbourhoodName'] == neighbourhoodName
        print(select_name_filter)
        df_neighbourhood_average_filtered.loc[select_name_filter, 'Legend'] = 'Selected Neighbourhood'

    # ================================================================================================================ #
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
                               height=538, opacity=0.25,
                               hover_data={'Legend': False, 'AssessedValue': True, 'NeighbourhoodID': True},
                               hover_name='NeighbourhoodName',
                               color_discrete_map={'green': "green", 'yellow': 'yellow', "red": 'purple'},
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

    fig.update_layout(margin={"r": 0, "t": 20, "l": 20, "b": 20},
                      legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
    fig.update_geos(fitbounds="locations")
    fig.update_layout(coloraxis_showscale=False, margin={"r": 0, "t": 20, "l": 20, "b": 20})
    return fig, df_neighbourhood_average_filtered['NeighbourhoodName'].unique()

# ==================================================================================================================== #
# COMPARISON PAGE CALL BACKS
# ==================================================================================================================== #

@app.callback(
    [Output('a_text1', 'children'),
     Output('l_graph1', 'figure'),],
    [Input('dd_selection1', 'value')])
def update_output(selection):
    default = "CRESTWOOD"
    if (selection == None):
        o2 = create_graph_languages(default)
        o1 = create_average_assessment(default)
    else:
        o2 = create_graph_languages(selection)
        o1 = create_average_assessment(selection)

    return o1, o2

@app.callback(
    [Output('a_text2', 'children'),
     Output('l_graph2', 'figure'),],
    [Input('dd_selection2', 'value')])
def update_output(selection):
    default = "RIVERDALE"
    if (selection == None):
        o2 = create_graph_languages(default)
        o1 = create_average_assessment(default)
    else:
        o2 = create_graph_languages(selection)
        o1 = create_average_assessment(selection)

    return o1, o2

@app.callback(
    [Output('a_text3', 'children'),
     Output('l_graph3', 'figure'),],
    [Input('dd_selection3', 'value')])
def update_output(selection):
    default = "MACEWAN"
    if (selection == None):
        o2 = create_graph_languages(default)
        o1 = create_average_assessment(default)
    else:
        o2 = create_graph_languages(selection)
        o1 = create_average_assessment(selection)

    return o1, o2



if __name__ == '__main__':
    app.run_server(debug=True)
