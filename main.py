import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from dash import Dash, html, dcc, Input, Output

#=================================================================================================================

crime_file = "./source-files/Occurrences_Last_90_Days.csv"
assessment_file = "./source-files/Property_Assessment_Data__Current_Calendar_Year_.csv"
languages_file = "./source-files/2016_Census_-_Dwelling_Unit_by_Language__Neighbourhood_Ward_.csv"

# create Pandas df and lists here
df_crimes = pd.read_csv(crime_file)
df_category = df_crimes.groupby(['Occurrence_Category'], as_index=False).size()

df_languages = pd.read_csv(languages_file)
column_header_lan = list(df_languages.columns.values)

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

    fig = go.Figure(data=[go.Bar(x=value_list, y=column_headers, orientation="h")])
    return fig

def create_average_assessment(value):
    residential = "RESIDENTIAL"
    df = pd.read_csv(assessment_file)
    dff = df.query("`Neighbourhood`==@value & `Assessment Class % 1`==100 & `Assessment Class 1`==@residential")["Assessed Value"]
    average = dff.mean()
    return average

def create_graph_assessment(value):
    residential = "RESIDENTIAL"
    df = pd.read_csv(assessment_file)
    dff = df.query("`Neighbourhood`==@value & `Assessment Class % 1`==100 & `Assessment Class 1`==@residential")["Assessed Value"]

    intervals = ["Less than 200K", "200K - 300K", "300K - 400K", "400K - 500K",
                 "500K - 600K", "600K - 700K", "700K - 800K", "More than 800K"]
    median = [0, 0, 0, 0,
             0, 0, 0, 0]
    for key in dff:
        if ( key < 200000):
            median[0] += 1
        elif (300000 > key >= 200000):
            median[1] += 1
        elif (400000 > key >= 300000):
            median[2] += 1
        elif (500000 > key >= 400000):
            median[3] += 1
        elif (600000 > key >= 500000):
            median[4] += 1
        elif (700000 > key >= 600000):
            median[5] += 1
        elif (800000 > key >= 700000):
            median[6] += 1
        else:
            median[7] += 1

    fig = go.Figure(
        data=[go.Bar(y=intervals, x=median, orientation="h")],
    )
    #fig.update_yaxes(ticklabelposition="inside top", title=None)
    return fig

#===================================================================================================================

#APP LAYOUT
app = Dash(__name__)

app.layout = html.Div([
    # put map here

    # comparison
    html.Div([
        html.Div([
            html.Div([
            "Neighbourhood 1",
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
                dcc.Graph(id='l_graph1'),
                html.Div(id='a_text1'),
                dcc.Graph(id='a_graph1'),
            ]),
        ], style={ 'margin':'25px', 'display':'flex', 'flex-direction':'column', 'width':'100%', }),

        html.Div([
            html.Div([
            "Neighbourhood 2",
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
                dcc.Graph(id='l_graph2'),
                html.Div(id='a_text2'),
                dcc.Graph(id='a_graph2'),
            ]),
        ], style={ 'margin':'25px', 'display':'flex', 'flex-direction':'column', 'width':'100%', }),

        html.Div([
            html.Div([
            "Neighbourhood 3",
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
                dcc.Graph(id='l_graph3'),
                html.Div(id='a_text3'),
                dcc.Graph(id='a_graph3'),
            ]),
        ], style={ 'margin':'25px', 'display':'flex', 'flex-direction':'column', 'width':'100%', }),
    ], style={'margin': '25px', 'display': 'flex', 'flex-direction': 'row', })
])


@app.callback(
    [Output('l_graph1', 'figure'),
     Output('a_text1', 'children'),
     Output('a_graph1', 'figure'),],
    [Input('dd_selection1', 'value')])
def update_output(selection):
    default = "CRESTWOOD"
    if (selection == None):
        o3 = create_graph_languages(default)
        o2 = create_average_assessment(default)
        o1 = create_graph_assessment(default)
    else:
        o3 = create_graph_languages(selection)
        o2 = create_average_assessment(selection)
        o1 = create_graph_assessment(selection)

    return o1, o2, o3

@app.callback(
    [Output('l_graph2', 'figure'),
     Output('a_text2', 'children'),
     Output('a_graph2', 'figure'),],
    [Input('dd_selection2', 'value')])
def update_output(selection):
    default = "RIVERDALE"
    if (selection == None):
        o3 = create_graph_languages(default)
        o2 = create_average_assessment(default)
        o1 = create_graph_assessment(default)
    else:
        o3 = create_graph_languages(selection)
        o2 = create_average_assessment(selection)
        o1 = create_graph_assessment(selection)

    return o1, o2, o3

@app.callback(
    [Output('l_graph3', 'figure'),
     Output('a_text3', 'children'),
     Output('a_graph3', 'figure'),],
    [Input('dd_selection3', 'value')])
def update_output(selection):
    default = "MACEWAN"
    if (selection == None):
        o3 = create_graph_languages(default)
        o2 = create_average_assessment(default)
        o1 = create_graph_assessment(default)
    else:
        o3 = create_graph_languages(selection)
        o2 = create_average_assessment(selection)
        o1 = create_graph_assessment(selection)

    return o1, o2, o3

if __name__ == '__main__':
    app.run_server(debug=True)