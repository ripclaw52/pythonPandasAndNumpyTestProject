import numpy as np
import pandas as pd
import plotly as po
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Display version for imported libraries
def library_version():
    print(f"numpy version: {np.__version__}\n"
          f"pandas version: {pd.__version__}\n"
          f"plotly version: {po.__version__}")

# TEMPERATURE_CHANGE data csv file as dataframe
clm_dataframe = pd.read_csv("CLIMATEDATA.csv") # abs-path
# GREENHOUSE-GAS data csv file as dataframe
ghg_dataframe = pd.read_csv("GREENHOUSEGASDATA.csv") # abs-path

# climate data base lists
df_country_list = clm_dataframe['country'].unique() # 247 unique countries
df_year_list = clm_dataframe['year'].unique() # 60 unique years
df_months_list = clm_dataframe['months'].unique() # 17 unique months (12 standard, 4 seasons, 1 meteorological year)

# ghg data base lists
df_iso_code_list = ghg_dataframe['iso_code'].dropna().unique()
df_country_ghg_list = ghg_dataframe[~ghg_dataframe['iso_code'].isnull()]
ghg_country_list = df_country_ghg_list['country'].unique() # unique country names

bool_series = ghg_dataframe[pd.isnull(ghg_dataframe['iso_code'])]
df_continents = ["Africa", "Asia", "Europe", "North America", "South America"]

# climate data; limited to meteorological month with random country as line and bar graph
def climate_data_random_single_country_in_metereological_month_over_year():
    var_size = 1
    random_country = np.random.randint((len(df_country_list) - 1), size=var_size)[0]
    #random_country = 37 #Canada
    np_country_select = df_country_list[random_country]
    df = clm_dataframe.query("`country` == @np_country_select and `months_code` == 7020")
    fig = px.line(df, x="year", y="value")
    fig.update_layout(
        hoverdistance=-1,
        hovermode="x unified",
        title=f"Overall temperature change in {np_country_select}",
        xaxis=dict(
            title="Year"
        ),
        yaxis=dict(
            title="Temperature change in degrees Celsius",
            ticksuffix=u'\N{DEGREE SIGN}'
        )
    )
    fig.show()

# climate data; all months with random country as box graph
def climate_data_in_month_over_year_as_box():
    var_size = 1
    random_country = np.random.randint((len(df_country_list) - 1), size=var_size)[0]
    #random_country = 37 #Canada
    np_country_select = df_country_list[random_country]
    df = clm_dataframe.query("`country` == @np_country_select")
    fig = px.box(df, x="year", y="value")
    fig.update_layout(
        hovermode="x unified",
        title=f"Temperature change over time in {np_country_select}",
        xaxis=dict(
            title="Year"
        ),
        yaxis=dict(
            title="Temperature change in degrees Celsius",
            ticksuffix=u'\N{DEGREE SIGN}'
        )
    )
    fig.show()

# climate data as 3d line graph with values by year and month
def climate_data_3d_line():
    m_color = ["red", "grey", "grey", "grey",
               "grey", "grey", "grey", "grey",
               "grey", "grey", "grey", "grey"]
    var_size = 1
    random_country = np.random.randint((len(df_country_list) - 1), size=var_size)[0]
    #random_country = 37 #Canada
    np_country_select = df_country_list[random_country]
    df = clm_dataframe.query("`country`==@np_country_select and `months_code`<=7012")
    fig = px.line_3d(df,
                     x='year',
                     y='months',
                     z='value',
                     line_group='months',
                     color='months',
                     color_discrete_map={
                         "January": f'{m_color[0]}',
                         "February": f'{m_color[1]}',
                         "March": f'{m_color[2]}',
                         "April": f'{m_color[3]}',
                         "May": f'{m_color[4]}',
                         "June": f'{m_color[5]}',
                         "July": f'{m_color[6]}',
                         "August": f'{m_color[7]}',
                         "September": f'{m_color[8]}',
                         "October": f'{m_color[9]}',
                         "November": f'{m_color[10]}',
                         "December": f'{m_color[11]}',
                     },
    )
    fig.update_layout(
        title=f"Temperature change for each month by year in {np_country_select}",
        scene_camera = dict(eye=dict(x=-1.35, y=-1.35, z=0.35)),
    )
    fig.update_scenes(
        xaxis=dict(
            title="Year",
        ),
        yaxis=dict(
            title="Months",
        ),
        zaxis=dict(
            title="Temperature change in degrees Celsius",
            ticksuffix=u'\N{DEGREE SIGN}',
        ),
    )
    fig.show()

# ghg data for a random country
def ghg_emissions_random_country():
    var_size = 1
    random_country = np.random.randint((len(ghg_country_list) - 1), size=var_size)[0]
    #random_country = 36 #Canada
    np_country_select = ghg_country_list[random_country]
    df = ghg_dataframe.query("`country` == @np_country_select")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['year'],
        y=df['co2'],
        mode="markers",
        name="Carbon Dioxide (CO2)"))
    fig.add_trace(go.Scatter(
        x=df['year'],
        y=df['methane'],
        mode="markers",
        name="Methane (CH4)"),
    )
    fig.add_trace(go.Scatter(
        x=df['year'],
        y=df['nitrous_oxide'],
        mode="markers",
        name="Nitrous Oxide (NO2)"),
    )
    fig.update_layout(
        hoverdistance=-1,
        hovermode="x unified",
        title=f"Greenhouse gas emissions by year in {np_country_select}",
        xaxis=dict(
            title="Year",
        ),
        yaxis=dict(
            title="Emissions per million tonnes",
            ticksuffix=" million t"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1)
    )
    fig.show()

def selection():
    input_var = (
        "Select one of these options to display the relevant graph: \n"
        "(1) - Climate data of a randomly selected country as a line graph.\n"
        "(2) - Climate data of a randomly selected country as a bar graph.\n"
        "(3) - Climate data of a randomly selected country as a 3D-line graph.\n"
        "(4) - Greenhouse gas emissions of a randomly selected country as a line graph.\n"
        "(0) - EXIT\n\n")
    while True:
        text = input(f"{input_var} Please enter a value(0-4): ")
        try:
            entry = int(text)
            if entry == 1:
                climate_data_random_single_country_in_metereological_month_over_year()
                continue
            elif entry == 2:
                climate_data_in_month_over_year_as_box()
                continue
            elif entry == 3:
                climate_data_3d_line()
                continue
            elif entry == 4:
                ghg_emissions_random_country()
                continue
            elif entry == 0:
                break
            else:
                print(f"\n({entry}) is not valid for this selection\n")
        except ValueError:
            print(f"\n({text}) is not of the correct type:(int) for this selection\n")

if __name__ == '__main__':
    library_version()

    selection()