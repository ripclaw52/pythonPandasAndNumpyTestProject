import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from dash import Dash, html, dcc, Input, Output

from modules.NeighbourhoodNameModule import findLanguagesInNeighbourhood


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

def create_leftside_graph():
    assessment = 'function'
    languages = 'function'
    crime = 'function'
    return (
        html.Div([
            dcc.Graph(),
            dcc.Graph(),
            dcc.Graph(),
        ])
    )

def create_rightside_graph():
    assessment = 'function'
    languages = 'function'
    crime = 'function'
    return (
        html.Div([
            dcc.Graph(),
            dcc.Graph(),
            dcc.Graph(),
        ])
    )

def create_languages_figure_from_value(value):
    df = pd.read_csv(languages_file)
    dff = df.loc[df['Neighbourhood Name'] == value]
    #temp_languages 3 - 15
    column_headers = list(dff.columns.values)[4:14]
    value_list = [
        dff.iloc[0,  4], dff.iloc[0,  5], dff.iloc[0,  6],
        dff.iloc[0,  7], dff.iloc[0,  8], dff.iloc[0,  9],
        dff.iloc[0, 10], dff.iloc[0, 11], dff.iloc[0, 12],
        dff.iloc[0, 13], dff.iloc[0, 14],
    ]

    fig = go.Figure(
        data=[go.Bar(x=value_list, y=column_headers, orientation="h",)],
    )

    return fig


#===================================================================================================================

#APP LAYOUT
app = Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.Div([
        "Neighbourhood 1",
        dcc.Dropdown(
            neighbourhood_list,
            multi=False,
            searchable=False,
            placeholder="Select a neighbourhood",
            id='dd_selection1',
            value="CRESTWOOD",
        ),
    ], style={}),
        html.Div([
            dcc.Graph(id='a_graph1'),
            dcc.Graph(id='l_graph1'),
        ]),
    ], style={ 'margin':'25px', 'display':'flex', 'flex-direction':'column', 'width':'25%', }),

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
            dcc.Graph(id='a_graph2'),
            dcc.Graph(id='l_graph2'),
        ]),
    ], style={ 'margin':'25px', 'display':'flex', 'flex-direction':'column', 'width':'25%', }),

    html.Div([
        html.Div([
        "Neighbourhood 3",
        dcc.Dropdown(
            neighbourhood_list,
            multi=False,
            searchable=True,
            placeholder="Select a neighbourhood",
            id='dd_selection3',
            value="RIVERDALE",
        ),
    ], style={}),
        html.Div([
            dcc.Graph(id='a_graph3'),
            dcc.Graph(id='l_graph3'),
        ]),
    ], style={ 'margin':'25px', 'display':'flex', 'flex-direction':'column', 'width':'25%', }),
], style={'margin': '50px', 'display': 'flex', 'flex-direction': 'row', }
)


@app.callback(
    [Output('a_graph1', 'figure'),
     Output('l_graph1', 'figure'),],
    [Input('dd_selection2', 'value')])
def update_output(selection):
    default = "CRESTWOOD"
    if (selection == None):
        o1 = create_languages_figure_from_value(default)
        o2 = create_languages_figure_from_value(default)
    else:
        o1 = create_languages_figure_from_value(selection)
        o2 = create_languages_figure_from_value(selection)

    return o1, o2

@app.callback(
    [Output('a_graph2', 'figure'),
     Output('l_graph2', 'figure'),],
    [Input('dd_selection2', 'value')])
def update_output(selection):
    default = "RIVERDALE"
    if (selection == None):
        o1 = create_languages_figure_from_value(default)
        o2 = create_languages_figure_from_value(default)
    else:
        o1 = create_languages_figure_from_value(selection)
        o2 = create_languages_figure_from_value(selection)

    return o1, o2

@app.callback(
    [Output('a_graph3', 'figure'),
     Output('l_graph3', 'figure'),],
    [Input('dd_selection3', 'value')])
def update_output(selection):
    default = "MACEWAN"
    if (selection == None):
        o1 = create_languages_figure_from_value(default)
        o2 = create_languages_figure_from_value(default)
    else:
        o1 = create_languages_figure_from_value(selection)
        o2 = create_languages_figure_from_value(selection)

    return o1, o2

if __name__ == '__main__':
    app.run_server(debug=True)