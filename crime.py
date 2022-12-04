import pandas as pd
from dash import Dash, html, dcc, Input, Output
import dash
import plotly.express as px


#=================================================================================================================

# create Pandas df and lists here
df_crimes = pd.read_csv('./source-files/Occurrences_Last_90_Days.csv')
df_category = df_crimes.groupby(['Occurrence_Category'], as_index=False).size()



#=====================================================================================================
def occurence_group_controller(crime_stats):
    new_df = df_crimes[df_crimes.Occurrence_Category == crime_stats]

    dfg=new_df.groupby('Occurrence_Group').count().reset_index()

    
    return dfg["Occurrence_Group"].values.tolist()


def occurence_group_type_controller(occurence_group):
    new_df = df_crimes[df_crimes.Occurrence_Group == occurence_group]

    dfg=new_df.groupby('Occurrence_Type_Group').count().reset_index()

    return  dfg["Occurrence_Type_Group"].values.tolist()


def mapped_crime_list():
   
    ret = { "Disorder" :occurence_group_controller("Disorder"),
           "Non-Violent" :occurence_group_controller("Non-Violent"),
           "Violent" :occurence_group_controller("Violent"),
           "Traffic" :occurence_group_controller("Traffic"),
           "Weapons" :occurence_group_controller("Weapons"),
           "Drugs" :occurence_group_controller("Drugs"),
           "Other" :occurence_group_controller("Other")}

    return ret


def general_crimes(general_crime):
    dff = df_crimes
    new_df = dff[dff.Occurrence_Category == general_crime]

    dfg=new_df.groupby('Occurrence_Group').count().reset_index()
    dfg=dfg.rename(columns={"Occurrence_Type_Group": "occurences"})

    # plot structure
    fig = px.bar(dfg,
                y='Occurrence_Group',
                x='occurences',
                title=general_crime + " Last 90 Days" ,
                barmode='stack',
                text="occurences",
                orientation='h')
    
    fig.update_layout(xaxis={'categoryorder':'total descending'}) # add only this line
    fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.6)

    fig.update_layout(xaxis_title="Occurences", yaxis_title="" , )
    
    return fig



def group_type(descriptive_crime):
    dff = df_crimes
    new_df = dff[dff.Occurrence_Group == descriptive_crime]

    dfg=new_df.groupby('Occurrence_Type_Group').count().reset_index()
    dfg=dfg.rename(columns={"Occurrence_Type_Group": "occurences"})

    # plot structure
    fig = px.bar(dfg,
                x='Occurrence_Group',
                y='occurences',
                title=descriptive_crime + " Last 90 Days" ,
                barmode='stack',
                text="Occurrence_Group",
                orientation='h'
                )
    
    fig.update_layout(xaxis={'categoryorder':'total descending'}) # add only this line
    fig.update_traces(marker_color='rgb(8, 143, 143)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.6)
    
    fig.update_layout(xaxis_title="Occurences", yaxis_title="" , )

    
    return fig








#===================================================================================================================

#APP LAYOUT
app = Dash(__name__)




#radio item component 
crime_selections = html.Div([
         dcc.RadioItems(
        labelStyle={'display': 'block'},
        id='general_crime',
        options=[{'label': k, 'value': k} for k in mapped_crime_list().keys()],
        value='Disorder'
        ),

        html.Hr(),

        dcc.RadioItems(id='descriptive_crime',     labelStyle={'display': 'block'}, ),

        html.Hr(),

        html.Div(id='display-selected-values')],style={'color':'#C0C0C0', 'background': 	'#161A1D'})


#general crime catagory graph component 
crime_cat_graph = html.Div([

    dcc.Graph(id = 'crime_cat_graph')

])

#crime occurence graph componenet 
crime_occur_graph = html.Div([

    dcc.Graph(id = 'crime_occur_graph')

])

#Container for the 3 compoenents
crime_container = html.Div([

    html.Div(crime_selections,  style={"width":250, "margin": 10, 'display': 'inline-block'}),
    html.Div(crime_cat_graph,  style={"width":400, "margin": 10, 'display': 'inline-block'}),
    html.Div(crime_occur_graph,  style={"width":400, "margin": 10, 'display': 'inline-block'}),

])





app.layout = html.Div([

    crime_container
       


    ])

    

 

@app.callback(
    dash.dependencies.Output('descriptive_crime', 'options'),
    [dash.dependencies.Input('general_crime', 'value')])
def set_general_crime_options(general_crime):
    return [{'label': i, 'value': i} for i in mapped_crime_list()[general_crime]]

@app.callback(
    dash.dependencies.Output('descriptive_crime', 'value'),
    [dash.dependencies.Input('descriptive_crime', 'options')])
def set_cities_value(available_options):
    return available_options[0]['value']



@app.callback(
    dash.dependencies.Output('crime_cat_graph', 'figure'),
    [dash.dependencies.Input('general_crime', 'value')])

def update_crime_cat_graph(general_crime):
    return  general_crimes(general_crime)


@app.callback(
    dash.dependencies.Output('crime_occur_graph', 'figure'),
    [dash.dependencies.Input('descriptive_crime', 'value')])

def update_crime_occur_graph(descriptive_crime):
    return group_type(descriptive_crime)
   

if __name__ == '__crime__':
    app.run_server(debug=True)
    