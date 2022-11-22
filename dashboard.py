import pandas as pd
import plotly
import plotly.express as px
from dash import Dash, html, dcc, Input, Output


#=================================================================================================================

# create Pandas df and lists here
df_crimes = pd.read_csv('Occurrences_Last_90_Days.csv')
df_category = df_crimes.groupby(['Occurrence_Category'], as_index=False).size()

df_assessments = pd.read_csv('Property_Assessment_Data_2022.csv')
df_assessments = df_assessments[(df_assessments['Assessment Class 1'] == 'RESIDENTIAL')]
df_neighbourhood_average = df_assessments.groupby(['Neighbourhood'], as_index=False)[['Assessed Value']].mean().round(0)

#how to iterate through data frame:
# for index, row in df_neighbourhood_average.iterrows():
#     print(row['Neighbourhood'], row['Assessed Value'])
#=============================================================

min_value = df_neighbourhood_average.min()[1]
max_value = df_neighbourhood_average.max()[1]

crimes_list = []

for item in df_category.values.tolist():
    crimes_list.append(item[0])




#===================================================================================================================

#APP LAYOUT
app = Dash(__name__)

app.layout = html.Div([



    html.Div(children=[
        html.Label('Moving to Edmonton Made Easy',
                   style={
                       'color': 'white',
                       'padding': 30,
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

        dcc.Input(placeholder='Enter Neighbourhood', type='text',
                  style={'marginRight':'10px', 'width': 350, 'padding-top': 10}),

        html.Br(),
        html.Br(),
        html.Label('Crime Statistics', style={'color': 'white', 'padding': 0}),
        dcc.Dropdown(crimes_list, id= 'crime_dropdown', multi=True, style={'marginRight':'10px', 'width': 350, 'padding-top': 0}),

    ], style={'padding': 30, 'flex': 1, 'background': '#1C6387'}),

    html.Div(children=[

        html.Br(),
        html.Label('Neighbourhood Assessment Average', style={'color': '#1C6387', 'padding': 10}),
        dcc.RangeSlider(
            min= 100000,
            max= 1000000,
            value= [250000,300000],
            id='Neighbourhood_Average'),
        html.Div([
            dcc.Graph(id='the_graph')
        ])
    ], style={'padding': 10, 'flex': 1}),


    html.Div(children=[
        html.Br(),
        dcc.RadioItems(['Residential', 'Commercial']),
    ], style={'padding': 10, 'flex': 1, 'color': '#1C6387'})

], style={'display': 'flex', 'flex-direction': 'row', 'width': 1400})

@app.callback(
    Output('the_graph', 'figure'),
    [Input('Neighbourhood_Average', 'value')])

def update_output(value):
    print(value)
    df_neighbourhood_average_filtered = df_neighbourhood_average[
        (value[0] <= df_neighbourhood_average['Assessed Value']) & (df_neighbourhood_average['Assessed Value'] <= value[1])
    ]
    #print(df_neighbourhood_average_filtered[:5])

    scatterplot = px.scatter(
        data_frame = df_neighbourhood_average_filtered,
        x="Neighbourhood",
        y="Assessed Value",
        hover_data=["Neighbourhood"],
        text="Neighbourhood",
        height=550,
        width = 1100
    )

    scatterplot.update_traces(textposition='top center')

    return (scatterplot)

if __name__ == '__main__':
    app.run_server(debug=True)
